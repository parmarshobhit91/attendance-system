from jose import jwt
from datetime import datetime, timedelta
import os

SECRET = os.getenv("JWT_SECRET")

def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=10)
    return jwt.encode(payload, SECRET, algorithm="HS256")