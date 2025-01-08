from fastapi import APIRouter, HTTPException
from models.comment import Comment
from config.db import collection_comments
from utils.helper import generate_id
from couchbase.exceptions import DocumentNotFoundException

router = APIRouter()

@router.get("/")
async def get_comments():
    query = "SELECT * FROM `techblog`.`default`.`comments`"
    comments = list(collection_comments.query(query))
    return [{"id": comment["id"], **comment} for comment in comments]

@router.post("/")
async def create_comment(comment: Comment):
    comment_dict = comment.dict()
    comment_dict["id"] = generate_id()
    collection_comments.insert(comment_dict["id"], comment_dict)
    return {"id": comment_dict["id"], **comment_dict}

@router.get("/{comment_id}")
async def get_comment(comment_id: str):
    try:
        result = collection_comments.get(comment_id)
        return result.content_as[dict]
    except DocumentNotFoundException:
        raise HTTPException(status_code=404, detail="Comment not found")

@router.put("/{comment_id}")
async def update_comment(comment_id: str, comment: Comment):
    try:
        collection_comments.upsert(comment_id, comment.dict())
        return {"id": comment_id, **comment.dict()}
    except DocumentNotFoundException:
        raise HTTPException(status_code=404, detail="Comment not found")

@router.delete("/{comment_id}")
async def delete_comment(comment_id: str):
    try:
        collection_comments.remove(comment_id)
        return {"message": "Comment deleted successfully"}
    except DocumentNotFoundException:
        raise HTTPException(status_code=404, detail="Comment not found")