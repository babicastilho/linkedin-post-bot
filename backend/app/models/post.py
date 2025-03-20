from typing import Optional
from pydantic import BaseModel, Field

class Post(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  
    title: str
    content: str
    status: str = "backlog"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
