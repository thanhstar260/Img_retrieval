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

class SearchResult(BaseModel):
    ids: List[int]
    distances: List[float]
