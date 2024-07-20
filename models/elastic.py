import json
from elasticsearch import Elasticsearch, helpers
import os
import numpy as np
import sys
sys.path.append(r"./")
from models.utils import visualize, load_image_path
from dotenv import load_dotenv

class Elastic():
    def __init__(self):
        self.es = None
    
    def connect_elastic(self, check_server, host='localhost', port=9200, scheme='http'):
        """Kết nối tới Elasticsearch.
        
        Returns:
            Elasticsearch: Đối tượng Elasticsearch.
        """
        
        # print(check_server)
        if check_server == "server":
            self.es = Elasticsearch([{'host': host, 'port': port, 'scheme': scheme}])
        else:
            self.es = Elasticsearch([host])
    
    def create_index(self,index_name):
    
        if not self.es.indices.exists(index=index_name):
            self.es.indices.create(index=index_name)
            print(f"Đã tạo chỉ mục: {index_name}")
        else:
            print(f"Chỉ mục {index_name} đã tồn tại.")
            
    def upload_data_to_elastic(self, data_path, index_name= None, id_name=None):
        """
        Đọc file JSON và thêm các phần tử vào Elasticsearch sau khi map class_name.
        
        Args:
            es (Elasticsearch): Đối tượng Elasticsearch.
            data_path (str): Đường dẫn tới file JSON chứa dữ liệu.
            class_name_path (str): Đường dẫn tới file class_name.
            index_name (str): Tên index trong Elasticsearch.
        """
        
        # Đọc toàn bộ nội dung của file JSON chứa dữ liệu
        with open(data_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        
        
        # Tạo danh sách các hành động để thêm vào Elasticsearch
        if id_name is None:
            actions = [
                {
                    "_index": index_name,
                    # "_id": item[id_name],  # Sử dụng "index" làm "_id"
                    "_source": item
                }
                for item in data
            ]
        else:
            actions = [
                {
                    "_index": index_name,
                    "_id": item[id_name],  # Sử dụng "index" làm "_id"
                    "_source": item
                }
                for item in data
            ]
        # Sử dụng helpers.bulk để thêm dữ liệu vào Elasticsearch
        helpers.bulk(self.es, actions)
        
    def Elastic_retrieval(self, text_query, k, index_name="ocr"):

        query = {
            "query": {
                "bool": {
                    "should": [
                        {
                            "multi_match": {
                                "query": text_query,
                                "fields": ["text"],
                                "type": "phrase",
                                "boost": 2  # Tăng cường độ ưu tiên cho kết quả chính xác
                            }
                        },
                        {
                            "multi_match": {
                                "query": text_query,
                                "fields": ["text"],
                                "fuzziness": "AUTO"
                            }
                        }
                    ]
                }
            },
            "size": k
        }

        # Thực hiện tìm kiếm
        res = self.es.search(index=index_name, body=query)
        # print(res)
        ids = [hit['_source']["id"] for hit in res['hits']['hits']]
        scores = [hit['_score'] for hit in res['hits']['hits']]
        # print(ids)
        # print(scores)
        scores = np.array(scores)
        scr_result = 1 / (1 + np.exp(-scores))
        scr_result = scr_result.tolist()
        
        return ids, scr_result
    
    
    def delete_index(self, index_name):
        # Kiểm tra xem index có tồn tại không
        if self.es.indices.exists(index=index_name):
            # Xóa index
            self.es.indices.delete(index=index_name)
            print(f"Index '{index_name}' đã được xóa.")
        else:
            print(f"Index '{index_name}' không tồn tại.")
            
            

# class OCR(Elastic):
#     def __init__(self):
#         super().__init__()
        
#     def upload_data_to_elastic(self, data_path, index_name="objects"):
#             """
#             Đọc file JSON và thêm các phần tử vào Elasticsearch sau khi map class_name.
            
#             Args:
#                 es (Elasticsearch): Đối tượng Elasticsearch.
#                 data_path (str): Đường dẫn tới file JSON chứa dữ liệu.
#                 class_name_path (str): Đường dẫn tới file class_name.
#                 index_name (str): Tên index trong Elasticsearch.
#             """
            
#             # Đọc toàn bộ nội dung của file JSON chứa dữ liệu
#             with open(data_path, "r", encoding="utf-8") as file:
#                 data = json.load(file)
            
            
#             # Tạo danh sách các hành động để thêm vào Elasticsearch
#             actions = [
#                 {
#                     "_index": index_name,
#                     # "_id": item["index"],  # Sử dụng "index" làm "_id"
#                     "_source": item
#                 }
#                 for item in data
#             ]
            
#             # Sử dụng helpers.bulk để thêm dữ liệu vào Elasticsearch
#             helpers.bulk(self.es, actions)
            
#     def ocr_retrieval(self, text_query, k, index_name="ocr"):

#         query = {
#             "query": {
#                 "bool": {
#                     "should": [
#                         {
#                             "multi_match": {
#                                 "query": text_query,
#                                 "fields": ["text"],
#                                 "type": "phrase",
#                                 "boost": 2  # Tăng cường độ ưu tiên cho kết quả chính xác
#                             }
#                         },
#                         {
#                             "multi_match": {
#                                 "query": text_query,
#                                 "fields": ["text"],
#                                 "fuzziness": "AUTO"
#                             }
#                         }
#                     ]
#                 }
#             },
#             "size": k
#         }

#         # Thực hiện tìm kiếm
#         res = self.es.search(index=index_name, body=query)
#         # print(res)
#         ids = [hit['_source']["id"] for hit in res['hits']['hits']]
#         scores = [hit['_score'] for hit in res['hits']['hits']]
#         # print(ids)
#         # print(scores)
#         return ids        
    
    
# class ASR(Elastic):
#     def __init__(self):
#         super().__init__()
        
#     def upload_data_to_elastic(self, data_path, index_name="objects"):
#             """
#             Đọc file JSON và thêm các phần tử vào Elasticsearch sau khi map class_name.
            
#             Args:
#                 es (Elasticsearch): Đối tượng Elasticsearch.
#                 data_path (str): Đường dẫn tới file JSON chứa dữ liệu.
#                 class_name_path (str): Đường dẫn tới file class_name.
#                 index_name (str): Tên index trong Elasticsearch.
#             """
            
#             # Đọc toàn bộ nội dung của file JSON chứa dữ liệu
#             with open(data_path, "r", encoding="utf-8") as file:
#                 data = json.load(file)
            
            
#             # Tạo danh sách các hành động để thêm vào Elasticsearch
#             actions = [
#                 {
#                     "_index": index_name,
#                     # "_id": item["index"],  # Sử dụng "index" làm "_id"
#                     "_source": item
#                 }
#                 for item in data
#             ]
            
#             # Sử dụng helpers.bulk để thêm dữ liệu vào Elasticsearch
#             helpers.bulk(self.es, actions)
            
#     def asr_retrieval(self, text_query, k, index_name="asr"):
#         query = {
#             "query": {
#                 "bool": {
#                     "should": [
#                         {
#                             "multi_match": {
#                                 "query": text_query,
#                                 "fields": ["text"],
#                                 "type": "phrase",
#                                 "boost": 2  # Tăng cường độ ưu tiên cho kết quả chính xác
#                             }
#                         },
#                         {
#                             "multi_match": {
#                                 "query": text_query,
#                                 "fields": ["text"],
#                                 "fuzziness": "AUTO"
#                             }
#                         }
#                     ]
#                 }
#             },
#             "size": k
#         }

#         # Thực hiện tìm kiếm
#         res = self.es.search(index=index_name, body=query)
#         # print(res)
#         start = [hit['_source']["start"] for hit in res['hits']['hits']]
#         end = [hit['_source']["end"] for hit in res['hits']['hits']]
#         # scores = [hit['_score'] for hit in res['hits']['hits']]
#         ids = []
#         for i in range(len(start)):
#             id = list(range(int(start[i]), int(end[i])+1))
#             ids.extend(id)
#         return ids[:k]
    
    
    
if __name__ == "__main__":
    
    load_dotenv()
    CHECK_SERVER = os.getenv("CHECK_SERVER")
    HOST_ELASTIC = os.getenv("HOST_ELASTIC")
    PORT_ELASTIC = int(os.getenv("PORT_ELASTIC"))
    
    
    ocr_check = True
    
    if ocr_check:
        # OCR
        ocr_path = r"C:\Users\admin\Projects\AIC\DATA\ocr\final_ocr_clean.json"
        ocr = OCR()
        ocr.connect_elastic(check_server=CHECK_SERVER, host=HOST_ELASTIC, port=PORT_ELASTIC)
        # ocr.create_index("ocr")
        # id_name = "id"
        # ocr.upload_data_to_elastic(ocr_path, "ocr", id_name=id_name)
        
        K = 20
        text_query = "nguyễn phương hằng"
        result = ocr.ocr_retrieval(text_query, K)
        
        # VISUALIZE RESULT
        image_path_dict = r"D:\Temporal_search\data\image_path.json"
        image_path = load_image_path(image_path_dict)
        # visualize(image_path, result, K)
        print(result)
    else:
        # ASR
        asr_path = r"C:\Users\admin\Projects\AIC\DATA\asr\final_asr.json"
        asr = ASR()
        asr.connect_elastic(check_server=CHECK_SERVER, host=HOST_ELASTIC, port=PORT_ELASTIC)
        # asr.create_index("asr")
        # asr.upload_data_to_elastic(asr_path, "asr")
        
        K = 20
        text_query = "nguyễn phương hằng"
        result = asr.asr_retrieval(text_query, K)
        
        # VISUALIZE RESULT
        image_path_dict = r"C:\Users\admin\Projects\AIC\DATA\image_path.json"
        image_path = load_image_path(image_path_dict)
        # visualize(image_path, result, K)
        print(result)
    
    
