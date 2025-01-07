
# routes/article_routes.py
from fastapi import APIRouter, HTTPException
from models.article import Article
from config.db import articles_collection
from bson import ObjectId
from utils.helper import object_id_str

router = APIRouter()

@router.get("/")
async def get_articles():
    articles = list(articles_collection.find())
    for article in articles:
        article["id"] = object_id_str(article["_id"])
        del article["_id"]
    return articles

@router.post("/")
async def create_article(article: Article):
    article_dict = article.dict()
    result = articles_collection.insert_one(article_dict)
    return {"id": object_id_str(result.inserted_id), **article_dict}

@router.get("/{article_id}")
async def get_article(article_id: str):
    article = articles_collection.find_one({"_id": ObjectId(article_id)})
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    article["id"] = object_id_str(article["_id"])
    del article["_id"]
    return article