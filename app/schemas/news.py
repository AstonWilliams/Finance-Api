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
        orm_mode = True  # Ensure orm_mode is set to True to allow ORM objects

class NewsArticleCreate(BaseModel):
    title: str
    source: str
    published_date: datetime
    content: str
