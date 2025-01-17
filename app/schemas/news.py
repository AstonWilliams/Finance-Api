from datetime import datetime
from pydantic import BaseModel

class NewsArticleBase(BaseModel):
    title: str
    source: str
    published_date: datetime
    content: str

class NewsArticleCreate(NewsArticleBase):
    pass

class NewsArticle(NewsArticleBase):
    id: int

    class Config:
        from_attributes = True
