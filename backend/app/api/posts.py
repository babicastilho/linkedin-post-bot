from fastapi import APIRouter, HTTPException
from app.models.post import Post
from app.services.database import posts_collection
from datetime import datetime
from typing import List
from bson import ObjectId

router = APIRouter()

# Define valid post statuses
VALID_STATUSES = {"backlog", "draft", "scheduled", "posted", "analyzing", "archived", "completed"}

@router.post("/create", response_model=Post)
async def create_post(post: Post):
    """Creates a new post"""
    new_post = post.dict()
    new_post["created_at"] = datetime.utcnow().isoformat()
    new_post["updated_at"] = None
    result = await posts_collection.insert_one(new_post)

    new_post["_id"] = str(result.inserted_id)  # Ensure ID is returned as a string
    return new_post

@router.get("/", response_model=List[Post])
async def get_posts():
    """Retrieves all posts"""
    posts = await posts_collection.find().to_list(length=100)
    for post in posts:
        post["_id"] = str(post["_id"])  # Convert ObjectId to string
        if isinstance(post["created_at"], datetime):  # Ensure conversion
            post["created_at"] = post["created_at"].isoformat()
        if post["updated_at"] and isinstance(post["updated_at"], datetime):
            post["updated_at"] = post["updated_at"].isoformat()
    return posts

@router.put("/update-status/{post_id}")
async def update_post_status(post_id: str, update_data: dict):
    """Updates the status of a post"""

    status = update_data.get("status")  # Get status from request body

    if status not in ["backlog", "draft", "scheduled", "posted", "analyzing", "completed"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    updated_post = await posts_collection.find_one_and_update(
        {"_id": ObjectId(post_id)},
        {"$set": {"status": status, "updated_at": datetime.utcnow()}},
        return_document=True
    )

    if not updated_post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Ensure _id is always a string and remove unnecessary fields
    updated_post["_id"] = str(updated_post["_id"])
    updated_post.pop("id", None)  # Remove 'id' if it exists

    return updated_post

@router.delete("/{post_id}")
async def delete_post(post_id: str):
    """Deletes a post"""
    result = await posts_collection.delete_one({"_id": ObjectId(post_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully"}
