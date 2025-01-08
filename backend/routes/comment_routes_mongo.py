# routes/comment_routes.py
from fastapi import APIRouter, HTTPException
from models.comment import Comment
from config.db import comments_collection
from bson import ObjectId
from utils.helper import object_id_str

router = APIRouter()

@router.get("/")
async def get_comments():
    comments = list(comments_collection.find())
    for comment in comments:
        comment["id"] = object_id_str(comment["_id"])
        del comment["_id"]
    return comments

@router.post("/")
async def create_comment(comment: Comment):
    comment_dict = comment.dict()
    result = comments_collection.insert_one(comment_dict)
    return {"id": object_id_str(result.inserted_id), **comment_dict}

@router.get("/{comment_id}")
async def get_comment(comment_id: str):
    comment = comments_collection.find_one({"_id": ObjectId(comment_id)})
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    comment["id"] = object_id_str(comment["_id"])
    del comment["_id"]
    return comment

@router.put("/{comment_id}")
async def update_comment(comment_id: str, comment: Comment):
    if not comments_collection.find_one({"_id": ObjectId(comment_id)}):
        raise HTTPException(status_code=404, detail="Comment not found")
    comments_collection.update_one({"_id": ObjectId(comment_id)}, {"$set": comment.dict()})
    return {"id": comment_id, **comment.dict()}

@router.delete("/{comment_id}")
async def delete_comment(comment_id: str):
    result = comments_collection.delete_one({"_id": ObjectId(comment_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"message": "Comment deleted successfully"}
