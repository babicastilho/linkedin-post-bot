from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.posts import router as posts_router  # Import the new posts API

app = FastAPI()

# Register authentication and posts routers
app.include_router(auth_router, prefix="/auth")
app.include_router(posts_router, prefix="/posts")  # Add posts API

@app.get("/")
def home():
    """Root endpoint to check API status."""
    return {"message": "LinkedIn Post Bot API is running!"}
