from dotenv import load_dotenv
import os
import sys
sys.path.append(r"./")
from models.utils import visualize, load_image_path, calculate_iou, weighted_average
import numpy as np
from models.elastic import Elastic

class OBJECTS(Elastic):
    def __init__(self):
        super().__init__()
        
        
    def create_index(self,index_name):
    
        mapping = {
        "mappings": {
            "properties": {
                "class_name": {"type": "keyword"},
                "conf": {"type": "float"},
                "bboxs": {"type": "float"}
                        }
                    }
                }
        if not self.es.indices.exists(index=index_name):
            self.es.indices.create(index=index_name, body=mapping)
            print(f"Đã tạo chỉ mục: {index_name}")
        else:
            print(f"Chỉ mục {index_name} đã tồn tại.")
            
    def get_objects(self, check_list,index_name= "objects", threshold=0.3):
        # Tạo truy vấn Elasticsearch
        objects_name_list = [item[0] for item in check_list]
        objects_name_list = list(set(objects_name_list))
        if self.es is None:
            self.connect_elasticsearch(host='localhost', port=9200, scheme='http')
            
        print(f"Đang tìm kiếm các đối tượng: {objects_name_list}")
        size_scroll = 10000
        must_clauses = [{"match": {"class_name": obj}} for obj in objects_name_list]
        query = {
            "query": {
                "bool": {
                    "must": must_clauses
                }
            },
            "size": size_scroll
        }

        # Thực hiện truy vấn đầu tiên để khởi tạo scroll
        response = self.es.search(index=index_name, body=query, scroll='2m')
        # print(response)
        # Lấy id của scroll
        scroll_id = response['_scroll_id']
        hits = response['hits']['hits']
        
        # Tạo danh sách để chứa kết quả
        results = []
        len_objects = len(objects_name_list)
        
        # Thu thập kết quả từ response
        while len(hits) > 0:
            for hit in hits:
                result = {
                    "conf": [],
                    "bboxs": [],
                    "classname": [],
                    "id": hit['_id']
                }
                
                classnames = hit['_source']["class_name"]
                confs = hit['_source']["conf"]
                boxes = hit['_source']["bboxs"]
                
                for i in range(len(classnames)):
                    if (classnames[i] in objects_name_list) and (float(confs[i]) > threshold):
                        result["conf"].append(confs[i])
                        result["bboxs"].append(boxes[i])
                        result["classname"].append(classnames[i])
                
                if len_objects == len(set(result["classname"])):
                    results.append(result)
            
            # Thực hiện truy vấn scroll tiếp theo
            response = self.es.scroll(scroll_id=scroll_id, scroll='2m')
            scroll_id = response['_scroll_id']
            hits = response['hits']['hits']
        
        
        print(f"Đã thu thập {len(results)} kết quả.")
        
        # Xóa scroll khi hoàn thành
        self.es.clear_scroll(scroll_id=scroll_id)
        
        return results
        
    
    def search_objects(self, datas, check_list, threshold=0.7):
        
        results = []
        class_chk_list = []
        bbox_chk_list = []

        for item in check_list:
            class_chk_list.append(item[0])
            bbox_chk_list.append(item[1])
            
            
        for entry in datas:
            if entry is None:
                continue
            bboxs = entry["bboxs"]
            class_name = entry["classname"]

            all_conditions_met = True

            class_rst = []
            iou_rst = []
            conf_rst = []
            score_rst = []
            for class_check, bbox_check in zip(class_chk_list, bbox_chk_list):
                condition_met = False
                for i, bbox in enumerate(bboxs):
                    iou = calculate_iou(bbox, bbox_check)
                    if class_name[i] == class_check and iou > threshold:
                        condition_met = True
                        # result["bboxs"].append(bbox)
                        class_rst.append(class_name[i])
                        iou_rst.append(iou)
                        conf_rst.append(entry["conf"][i])
                        score = float(entry["conf"][i]) * iou
                        score_rst.append(score)

                        break
                if not condition_met:
                    all_conditions_met = False
                    break

            if all_conditions_met:
                results.append(
                    {"id": entry["id"],
                    "class_name": class_rst,
                    "iou": iou_rst,
                    "conf": conf_rst,
                    "score": weighted_average(score_rst)
                    # "score": sum(score_rst)/len(score_rst)
                    }
                )

        return results

    def get_ids(self, results):
        ids = [int(entry["id"]) for entry in results]
        scores = [entry["score"] for entry in results]
        idx_sort = np.argsort(scores)[::-1]
        ids = [ids[i] for i in idx_sort]
        scr = [scores[i] for i in idx_sort]
        return ids, scr
    
    def Objects_local_retrieval(self, objects_list, K, index_name="objects", threshold_conf=0.,threshold_iou=0.2):
        candidate = self.get_objects(objects_list, index_name, threshold_conf)
        results = self.search_objects(candidate, objects_list, threshold_iou)
        ids, scr = self.get_ids(results)
        # if len(ids) > K:
        #     ids = ids[:K]
        return ids, scr
    
    


if __name__ == "__main__":

    load_dotenv()
    CHECK_SERVER = os.getenv("CHECK_SERVER")
    HOST_ELASTIC = os.getenv("HOST_ELASTIC")
    PORT_ELASTIC = int(os.getenv("PORT_ELASTIC"))
    
    
    objects = OBJECTS()
    objects.connect_elastic(check_server=CHECK_SERVER, host=HOST_ELASTIC, port=PORT_ELASTIC)
    
    id_name = "index"
    K = 40

    # check_list = [("dog", [860, 265, 1139, 459]),
    #               ("person", [1015, 99, 1228, 417])]
    
    dog_list = [948.0,304.0,1180.0,407.0]
    person_list = [1127.0,175.0,1274.0,391.0]

    check_list = [("dog", dog_list),
                ("person", person_list),
                ("dog",[427.0,310.0,753.0,469.0])]
    
    # print(calculate_iou(dog_list, [862.5035400390625,261.30242919921875,1138.609130859375,471.89324951171875]))
    # print(calculate_iou(person_list, [1020.793212890625,100.4671630859375,1232.89111328125,424.25213623046875]))

    ids,scr = objects.Objects_local_retrieval(check_list, K, threshold_iou = 0.1)
    print("ids: ", ids)
    print("score: ",np.round(scr, 4))
    img_path = load_image_path(r'D:\THANHSTAR\Projetcs\AIC\DATA\image_path.json')
    visualize(img_path, ids)