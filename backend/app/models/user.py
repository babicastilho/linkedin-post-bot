from datetime import datetime
from typing import Optional

class UserModel:
    def __init__(self, email: str, hashed_password: str, username: Optional[str] = None):
        self.email = email
        self.username = username
        self.hashed_password = hashed_password
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            "email": self.email,
            "username": self.username,
            "hashed_password": self.hashed_password,
            "created_at": self.created_at
        }
