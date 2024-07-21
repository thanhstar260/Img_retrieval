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
        if index_name == "ocr":
            ids = [hit['_source']["id"] for hit in res['hits']['hits']]
        elif index_name == "asr":
            ids = [hit['_source']["start"] for hit in res['hits']['hits']]

        scores = [hit['_score'] for hit in res['hits']['hits']]
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
            
    
    
if __name__ == "__main__":
    
    load_dotenv()
    CHECK_SERVER = os.getenv("CHECK_SERVER")
    HOST_ELASTIC = os.getenv("HOST_ELASTIC")
    PORT_ELASTIC = int(os.getenv("PORT_ELASTIC"))
    
    es = Elastic()
    es.connect_elastic(check_server=CHECK_SERVER, host=HOST_ELASTIC, port=PORT_ELASTIC)
    ocr_check = False
    
    if ocr_check:
        # OCR
        ocr_path = r"C:\Users\admin\Projects\AIC\DATA\ocr\final_ocr_clean.json"
        index_name = "ocr"
        
        # id_name = "id"
        # es.upload_data_to_elastic(ocr_path, "ocr", id_name=id_name)
        
        K = 20
        text_query = "nguyễn phương hằng"
        ids, scr = es.Elastic_retrieval(text_query, K, index_name)
        

    else:
        # ASR
        asr_path = r"C:\Users\admin\Projects\AIC\DATA\asr\final_asr.json"

        index_name = "asr"
        # es.upload_data_to_elastic(asr_path, index_name)
        
        K = 20
        text_query = "nguyễn phương hằng"
        ids,scr = es.Elastic_retrieval(text_query, K, index_name)
        
        
        
    # VISUALIZE RESULT
    image_path_dict = r"D:\THANHSTAR\Projetcs\AIC\DATA\image_path.json"
    image_path = load_image_path(image_path_dict)
    visualize(image_path, ids, K)

    
