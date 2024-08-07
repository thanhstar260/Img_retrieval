from dotenv import load_dotenv
import os
import torch
import numpy as np
import sys
sys.path.append(r"./")

from models.beit3_model import BEIT3
from models.elastic import Elastic
from models.sketch import SKETCH
from models.object import OBJECTS
from models.utils import visualize, load_image_path, translate, rrf
import time
import math
import pandas as pd


class Event_retrieval():
    def __init__(self):
        self.beit3 = BEIT3()
        self.elastic = Elastic()
        self.sketch = SKETCH()
        self.objects = OBJECTS()
        self.mapdata = None
    
    def load_model(self, device, type_model = "all", beit3_model_path = None, tokenizer_path = None, sket_model_path = "None"):
        if type_model == "beit3":
            if beit3_model_path is None or tokenizer_path is None:
                raise ValueError("For type_model='beit3', both 'beit3_model_path' and 'tokenizer_path' must be provided.")
            
            self.beit3.load_model(device, beit3_model_path, tokenizer_path)
            
        elif type_model == "sket":
            if sket_model_path is None:
                raise ValueError("For type_model='sket', 'sket_model_path' must be provided.")
            
            self.sketch.load_model(device, sket_model_path)
            
        elif type_model == "all":
            if beit3_model_path is None or tokenizer_path is None or sket_model_path is None:
                raise ValueError("For type_model='all', 'beit3_model_path', 'tokenizer_path', and 'sket_model_path' must all be provided.")

            self.beit3.load_model(device, beit3_model_path, tokenizer_path)
            self.sketch.load_model(device, sket_model_path)
        else:
            raise ValueError("Invalid type_model. Accepted values are 'beit3', 'sket', or 'all'.")

        self.device = device

    def load_feature(self, type_fea = "all", beit3_fea_path = None, sket_fea_path = None, distance_metric="cosine"):
        if type_fea == "beit3":
            if beit3_fea_path is None:
                raise ValueError("For type_model='beit3', 'beit3_fea_path' must be provided.")
            
            self.beit3.load_feature(beit3_fea_path, distance_metric)
            
        elif type_fea == "sket":
            if sket_fea_path is None:
                raise ValueError("For type_model='sket', 'sket_fea_path' must be provided.")
            
            self.sketch.load_feature(sket_fea_path, distance_metric)
            
        elif type_fea == "all":
            if beit3_fea_path is None or sket_fea_path is None:
                raise ValueError("For type_model='all', 'beit3_fea_path', 'tokenizer_path', and 'sket_fea_path' must all be provided.")

            self.beit3.load_feature(beit3_fea_path, distance_metric)
            self.sketch.load_feature(sket_fea_path, distance_metric)
        else:
            raise ValueError("Invalid type_model. Accepted values are 'beit3', 'sket', or 'all'.")

    def connect_elastic(self, check_server, host='localhost', port=9200, scheme='http'):
        self.elastic.connect_elastic(check_server, host, port, scheme)
        self.objects.connect_elastic(check_server, host, port, scheme)
        
    
    def object_filter(self, ids_first, scr_first, objects_list, K, index_name="objects", threshold_conf=0.,threshold_iou=0.2):
        ids, scr = self.objects.Objects_local_retrieval(objects_list, K, index_name, threshold_conf, threshold_iou)
        
        # visualize(load_image_path(r".\DATA\image_path.json"), ids, len(ids), 8)
        # print("position: ",ids,scr,find_positions(ids, ids_first.tolist()))
        # visualize(load_image_path(r'D:\THANHSTAR\Projetcs\AIC\DATA\image_path.json'), ids)
        # print("objects local retrieval: ", scr, ids)
        
        # print("objects local sigmoid: ", 1 / (1 + np.exp(-np.array(scr))))
        
        scr_first_dict = {ids_first[i]: scr_first[i] for i in range(len(ids_first))}

        # Kiểm tra và cập nhật giá trị tương ứng
        for i in range(len(ids)):
            if ids[i] in scr_first_dict:
                scr_first_dict[ids[i]] += scr[i]

        # Cập nhật lại mảng scr_first
        scr_sec = [scr_first_dict[id_first] for id_first in ids_first]
        scr_sec = np.array(scr_sec)
        
        scr_result = 1 / (1 + np.exp(-scr_sec))
        scr_result = scr_result.tolist()

        # Kết hợp hai danh sách lại với nhau thành một danh sách các tuple
        combined = list(zip(scr_result, ids_first))

        # Sắp xếp danh sách các tuple dựa trên giá trị của scr_result (phần tử đầu tiên của mỗi tuple)
        sorted_combined = sorted(combined, key=lambda x: x[0], reverse=True)

        # Tách lại thành hai danh sách
        scr_result_sorted, ids_first_sorted = zip(*sorted_combined)

        # Chuyển đổi tuple trở lại thành danh sách nếu cần thiết
        scr_result_sorted = list(scr_result_sorted)
        ids_result_sorted = list(ids_first_sorted)
        
        
        return ids_result_sorted, scr_result_sorted
    
    def rerank(self, curr_sim, curr_index, positive_list, negative_list, features= None):
        if features is None:
            features = self.beit3.features
        start_time = time.time()
        orig_top_features = features[curr_index] # (5000, 768)

        positive_features = features[positive_list] # (4, 768)
        negative_features = features[negative_list] # (2, 768)

        positive_sim = positive_features @ orig_top_features.T # (4, 5000)
        negative_sim = negative_features @ orig_top_features.T # (2, 5000)

        positive_sim = positive_sim.sum(axis=0) # (5000,)
        negative_sim = negative_sim.sum(axis=0) # (5000,)

        new_sim = curr_sim + positive_sim - negative_sim # (5000,)

        # Combine the lists
        combined = list(zip(new_sim, curr_index)) # (5000, 2)

        # Sort the combined list by similarities in descending order
        sorted_combined = sorted(combined, key=lambda x: x[0], reverse=True) # (5000, 2)

        # Unzip the sorted list back into two lists
        sorted_similarities, sorted_indexes = zip(*sorted_combined) # (5000,), (5000,)

        # Convert tuples back to lists (if needed)
        new_similarities = list(sorted_similarities) # (5000,)
        new_indexes = list(sorted_indexes) # (5000,)

        end_time = time.time()
        print("Reranking time: ", end_time - start_time)  

        return new_indexes, new_similarities

    
    def temporal_search(self, ids, scores, df_path = r".\DATA\data1.csv"):
        if self.mapdata is None:
            self.mapdata = pd.read_csv(df_path)
            
        stages = []

        next = ids[0]
        new_score = scores[0]

        for stage in range(len(ids)):
            if stage == len(ids)-1:
                break
            id_curr = next
            id_next = ids[stage+1]
            score_curr = new_score
            score_next = scores[stage+1]
            new_score = []
            curr = []
            next = []
            for i in range(len(id_curr)):
                max_score = -1
                id1_max = -1
                id2_max = -1
                if id_curr[i] == -1:
                    curr.append(id1_max)
                    next.append(id2_max)
                    new_score.append(max_score)
                    continue
                for j in range(len(id_next)):
                    id1 = int(id_curr[i])
                    id2 = int(id_next[j])
                    # print(mapdata['file_name'].index)
                    if (self.mapdata['file_name'][id1] == self.mapdata['file_name'][id2]) and id2 > id1:
                        score = score_curr[i] + score_next[j]
                        t = (self.mapdata['frame_idx'][id2]-self.mapdata['frame_idx'][id1])/25
                        score = score*math.exp(-abs(0.1*(t-5)))
                        if score > max_score:
                            max_score = score
                            id1_max = id1
                            id2_max = id2
                    else:
                        continue

                curr.append(id1_max)
                next.append(id2_max)
                new_score.append(max_score)

            if stage == 0:
                stages.append(curr)
            stages.append(next)

        # Transpose the indexes list to align corresponding pairs
        indexes_transposed = list(zip(*stages))

        # Combine the transposed indexes and scores
        combined = list(zip(indexes_transposed, new_score))

        # Sort the combined list by scores in descending order
        sorted_combined = sorted(combined, key=lambda x: x[1], reverse=True)

        # Unzip the sorted list back into separate lists
        sorted_indexes_transposed, sorted_scores = zip(*sorted_combined)

        # Transpose back to the original shape for indexes
        sorted_indexes = list(map(list, zip(*sorted_indexes_transposed)))

        num_results = sorted_scores.index(-1)
        sorted_indexes = [sorted_indexes[i][:num_results] for i in range(len(sorted_indexes))]
        sorted_scores = sorted_scores[:num_results]

        # Output the sorted lists
        # print("Sorted indexes:", sorted_indexes)
        # print("Sorted scores:", sorted_scores)
        
        return sorted_indexes, sorted_scores



  
if __name__ == "__main__":
    load_dotenv()
    CHECK_SERVER = os.getenv("CHECK_SERVER")
    HOST_ELASTIC = os.getenv("HOST_ELASTIC")
    PORT_ELASTIC = int(os.getenv("PORT_ELASTIC"))
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    K = 20
    
    
    # BEIT3 PARAMETER
    beit3_model_path = r".\models\weights\beit3_base_itc_patch16_224.pth"
    tokenizer_path = r".\models\weights\beit3.spm"
    beit3_fea_path = r".\DATA\beit3_features"
    
    # SKETCH PARAMETER
    sket_model_path = r".\ZSE_SBIR\checkpoints\sketchy_ext\best_checkpoint.pth"
    sket_fea_path = r".\DATA\sketch_features"
    
        
    model = Event_retrieval()
    
    # Load full model
    model.load_model(device=device, type_model="all", beit3_model_path=beit3_model_path, tokenizer_path=tokenizer_path, sket_model_path=sket_model_path)
    
    # only load beit3 model --> type_model="beit3"
    # only load sketch model --> type_model="sket"
    
    
    # Load full feature
    model.load_feature(type_fea="all", beit3_fea_path=beit3_fea_path, sket_fea_path=sket_fea_path)
    
    # only load beit3 feature --> type_fea="beit3"
    # only load sketch feature --> type_fea="sket"
    
    
    # Connect to elasticsearch
    model.connect_elastic(check_server = CHECK_SERVER, host=HOST_ELASTIC, port=PORT_ELASTIC)
    
    
    # # RUN BEIT3 TEXT QUERY
    
    # text_query = "một người phụ nữ đang cho bầy chó ăn trong công viên"
    # text_query = translate(text_query)

    # ids, dis = model.beit3.Text_retrieval(text_query, K, device)
    
    # print("beit3 text query results: ", ids)
    
    
    # # RUN BEIT3 IMAGE QUERY
    # img_query_path = r".\static\images\Keyframes_L01\L01_V001\0010.jpg"
    
    # ids, dis = model.beit3.Image_retrieval(img_query_path, K, device)
    
    # print("beit3 image query results: ", ids)
    
    
    # # RUN SKETCH QUERY
    # sket_query_path = r"C:\Users\admin\Downloads\test_sket\duck.jpg"
    
    # ids, dis = model.sketch.Sket_retrieval(sket_query_path, K, device)
    
    # print("sketch query results: ", ids)
    # print(dis[0])
    
    
    # # RUN OCR QUERY
    # ocr_query = "nguyễn phương hằng"
    # index_name = "ocr"
    
    # ids, dis = model.elastic.Elastic_retrieval(ocr_query, K, index_name=index_name)
    
    # print("ocr query results: ", dis)
    # visualize(load_image_path(r".\DATA\image_path.json"), ids, K, 8, (10,5))
    
    
    # # RUN ASR QUERY
    # asr_query = "nguyễn phương hằng"
    # index_name = "asr"
    
    # ids, dis = model.elastic.Elastic_retrieval(asr_query, K, index_name=index_name)
    
    # print("asr query results: ", dis)
    
    
    # # WHEN USE OBJECT OR RERANKING => USE 10*k for (beit3, sketch, ocr, asr) query
    # # RUN BEIT3 TEXT RETRIEVAL + OBJECT FILTER QUERY AFTER USING RANKING
    
    # # RUN from line 315 - 343 -> 
    # # visualize1 is the result of beit3 text query
    # # visualize2 is the result of objects local
    # # visualize3 is the result of beit3 text query + object filter
    # # visualize4 is the result of beit3 text query + object filter + reranking
    
    # text_query = "1 người đang trượt băng với những chú chó"
    # text_query = translate(text_query)
    # print("text translate query: ", text_query)
    # K = 20
    # check_list = [
    #             ("dog", [948.0,304.0,1180.0,407.0]),
    #             ("person", [1127.0,175.0,1274.0,391.0]),
    #             # ("dog",[427.0,310.0,753.0,469.0])
    #             ]
    
    # img_path = load_image_path(r".\DATA\image_path.json")
    
    # # first query
    # ids, dis = model.beit3.Text_retrieval(text_query, 10*K, device)
    # visualize(load_image_path(r".\DATA\image_path.json"), ids[:K], K, 8, (10,5))
        
    # # object filter
    # ids, dis = model.object_filter(ids, dis, check_list, K)
    # print("beit3 text query + objects filter results: ", ids[:K])
    # visualize(img_path, ids[:K], K, 8, (10,5))
    
    
    # # USE RERANKING
    
    # ids, dis = model.rerank(dis, ids, positive_list=[55438,19397], negative_list=[])
    
    # print("beit3 text query + objects filter + reranking results: ", ids[:K])
    # visualize(img_path, ids[:K], K, 8, (10,5))
    
    
    
    # # TEMPORAL QUERY
    # # visualize1 is the result of stage1
    # # visualize2 is the result of stage2
    
    # text_stage1 = "group of students are exercising in the yard"
    # text_stage2 = "The teacher is teaching in class."
    
    # ids1, scr1 = model.beit3.Text_retrieval(text_stage1, 10*K, device)
    # ids2, scr2 = model.beit3.Text_retrieval(text_stage2, 10*K, device)
    
    # list_ids = [ids1, ids2]
    # list_scr = [scr1, scr2]
    # ids, scr = model.temporal_search(list_ids, list_scr)
    
    # # result stage1 = ids[0], scr[0]
    # # result stage2 = ids[1], scr[1]
    # print("temporal search stage1 results: ", ids[0][:K])
    # visualize(load_image_path(r".\DATA\image_path.json"), ids[0][:K], K, 8, (10,5))
    # print("temporal search stage2 results: ", ids[1][:K])
    # visualize(load_image_path(r".\DATA\image_path.json"), ids[1][:K], K, 8, (10,5))
    
    
    
    
    
    
    
    