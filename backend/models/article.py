# models/article.py
from pydantic import BaseModel

class Article(BaseModel):
    title: str
    content: str
    author: str
    category: str
    createdAt: str
    authorAvatar: str
