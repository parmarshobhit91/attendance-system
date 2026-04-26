from fastapi import APIRouter
from app.db import db
from datetime import datetime

router = APIRouter(prefix="/overtime")


@router.post("/request")
def request_ot(data: dict):

    if "email" not in data or "hours" not in data:
        return {"error": "email and hours required"}

    if data["hours"] <= 0:
        return {"error": "Invalid hours"}

    db.overtime.insert_one({
        "email": data["email"],
        "hours": data["hours"],
        "status": "pending",
        "created_at": datetime.utcnow()
    })

    return {"msg": "OT requested"}


@router.get("/all")
def get_ot():
    return list(db.overtime.find({}, {"_id": 0}))


@router.post("/approve")
def approve_ot(data: dict):

    if "email" not in data or "status" not in data:
        return {"error": "email and status required"}

    db.overtime.update_one(
        {"email": data["email"], "status": "pending"},
        {"$set": {"status": data["status"], "updated_at": datetime.utcnow()}}
    )

    return {"msg": "Updated"}