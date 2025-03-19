from fastapi import FastAPI
from app.api.auth import router as auth_router

app = FastAPI()

# Register authentication routes
app.include_router(auth_router, prefix="/auth")

@app.get("/")
def home():
    """Root endpoint to check API status."""
    return {"message": "LinkedIn Post Bot API is running!"}
