# models/comment.py
from pydantic import BaseModel

class Comment(BaseModel):
    article_id: str
    content: str
    author: str
    createdAt: str
