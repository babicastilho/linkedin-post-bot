from fastapi import APIRouter, HTTPException
from app.schemas.post_schema import PostResponse, PostCreate, PostUpdateStatus
from app.services.database import posts_collection
from datetime import datetime
from typing import List
from bson import ObjectId

router = APIRouter()

@router.post("/create", response_model=PostResponse)
async def create_post(post: PostCreate):
    """Creates a new post"""
    new_post = post.dict()
    new_post["created_at"] = datetime.utcnow()
    new_post["updated_at"] = None
    result = await posts_collection.insert_one(new_post)

    new_post["_id"] = str(result.inserted_id)  # Ensure ID is returned as string
    return new_post

@router.get("/", response_model=List[PostResponse])
async def get_posts():
    """Retrieves all posts"""
    posts = await posts_collection.find().to_list(length=100)

    for post in posts:
        post["_id"] = str(post["_id"])  # Convert ObjectId to string
        post["created_at"] = PostResponse.convert_datetime(post.get("created_at"))
        post["updated_at"] = PostResponse.convert_datetime(post.get("updated_at"))

    return posts

@router.put("/update-status/{post_id}")
async def update_post_status(post_id: str, update_data: dict):
    """Updates the status of a post"""

    status = update_data.get("status")  # Get status from request body

    if status not in ["backlog", "draft", "scheduled", "posted", "analyzing", "archived", "completed"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    updated_post = await posts_collection.find_one_and_update(
        {"_id": ObjectId(post_id)},
        {"$set": {"status": status, "updated_at": datetime.utcnow()}},
        return_document=True
    )

    if not updated_post:
        raise HTTPException(status_code=404, detail="Post not found")

    updated_post["_id"] = str(updated_post["_id"])
    updated_post["created_at"] = PostResponse.convert_datetime(updated_post.get("created_at"))
    updated_post["updated_at"] = PostResponse.convert_datetime(updated_post.get("updated_at"))

    return updated_post

@router.delete("/{post_id}")
async def delete_post(post_id: str):
    """Deletes a post"""
    result = await posts_collection.delete_one({"_id": ObjectId(post_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully"}
