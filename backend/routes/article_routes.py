from fastapi import APIRouter, HTTPException
from models.article import Article
from config.db import collection_articles
from utils.helper import generate_id
from couchbase.exceptions import DocumentNotFoundException

router = APIRouter()

@router.get("/")
async def get_articles():
    query = "SELECT * FROM `techblog`.`default`.`articles`"
    articles = list(collection_articles.query(query))
    return [{"id": article["id"], **article} for article in articles]

@router.post("/")
async def create_article(article: Article):
    article_dict = article.dict()
    article_dict["id"] = generate_id()
    collection_articles.insert(article_dict["id"], article_dict)
    return {"id": article_dict["id"], **article_dict}

@router.get("/{article_id}")
async def get_article(article_id: str):
    try:
        result = collection_articles.get(article_id)
        return result.content_as[dict]
    except DocumentNotFoundException:
        raise HTTPException(status_code=404, detail="Article not found")

@router.put("/{article_id}")
async def update_article(article_id: str, article: Article):
    try:
        collection_articles.upsert(article_id, article.dict())
        return {"id": article_id, **article.dict()}
    except DocumentNotFoundException:
        raise HTTPException(status_code=404, detail="Article not found")

@router.delete("/{article_id}")
async def delete_article(article_id: str):
    try:
        collection_articles.remove(article_id)
        return {"message": "Article deleted successfully"}
    except DocumentNotFoundException:
        raise HTTPException(status_code=404, detail="Article not found")