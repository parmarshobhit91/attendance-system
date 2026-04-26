from fastapi import APIRouter
from app.db import db
from app.utils.helpers import hash_password, verify_password
from app.utils.jwt_handler import create_token
from app.services.face_service import get_face_encodings

router = APIRouter(prefix="/auth")

@router.post("/signup")
def signup(user: dict):
    user["password"] = hash_password(user["password"])
    user["role"] = user.get("role", "employee")

    db.users.insert_one(user)
    return {"msg": "User created"}

@router.post("/login")
def login(data: dict):
    user = db.users.find_one({"email": data["email"]})

    if not user or not verify_password(data["password"], user["password"]):
        return {"error": "Invalid credentials"}
    
    token = create_token({
        "user_id": str(user["_id"]),
        "role": user["role"]
    })

    return {"token": token}

@router.post("/register-face")
def register_face(data: dict):
    user = db.users.find_one({"email": data["email"]})

    if not user:
        return {"error": "User not found"}
    
    encoding = get_face_encodings(data["image"])

    if encoding is None:
        return {"error": "No face detected"}
    
    db.users.update_one(
    {"email": data["email"]},     # FILTER (dict)
    {"$set": {"face_encoding": encoding}}   # UPDATE (dict)
)

    return {"msg": "Face registered successfully"}