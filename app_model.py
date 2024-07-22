from pydantic import BaseModel
from typing import List, Optional, Dict
from enum import Enum

class Type(str, Enum):
    scene = "scene"
    image = "image"
    text = "text"
    speech = "speech"
    sketch = "sketch"


class Stage(BaseModel):
    type: Type
    data: str
    object: Optional[Dict[str, List[List[int]]]] = None
    lang: str

class SearchRequest(BaseModel):
    stages: List[Stage]
    K: int

class SearchResult(BaseModel):
    ids: List[int]
    distances: List[float]

class StageRerank(BaseModel):
    ids: List[int]
    dis: List[int]
    positive_list: List[int]
    negative_list: List[int]
    
class RerankRequest(BaseModel):
    stages: List[StageRerank]
    
