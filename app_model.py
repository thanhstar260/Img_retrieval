from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class Type(str, Enum):
    scene = "scene"
    image = "image"
    text = "text"
    speech = "speech"
    sketch = "sketch"

class Object(BaseModel):
    name: str
    data: List[int]

class Stage(BaseModel):
    type: Type
    data: str
    object: Optional[Object] = None
    lang: str

class SearchRequest(BaseModel):
    stages: List[Stage]