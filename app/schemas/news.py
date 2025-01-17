from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ValidationError(BaseModel):
    loc: List[str]
    msg: str
    type: str

class HTTPValidationError(BaseModel):
    detail: Optional[List[ValidationError]]

class NewsArticle(BaseModel):
    id: int
    title: str
    source: str
    published_date: datetime
    content: str

    class Config:
        from_attributes = True  # Updated to reflect Pydantic v2 changes

class NewsArticleCreate(BaseModel):
    title: str
    source: str
    published_date: datetime
    content: str
