from fastapi import APIRouter
from app.db import db
from app.services.face_service import get_face_encodings
from datetime import datetime
import numpy as np
import face_recognition

router = APIRouter(prefix="/attendance")


@router.post("/punch")
def punch_attendance(data: dict):

    # 1️⃣ Get face encoding
    encodings = get_face_encodings(data["image"])

    if len(encodings) == 0:
        return {"error": "No face detected"}

    unknown_encoding = encodings[0]

    # 2️⃣ Get all users
    users = list(db.users.find({"face_encoding": {"$exists": True}}))

    if len(users) == 0:
        return {"error": "No registered users"}

    known_encodings = [np.array(user["face_encoding"]) for user in users]

    # 3️⃣ Match face
    distances = face_recognition.face_distance(known_encodings, unknown_encoding)

    best_match_index = np.argmin(distances)
    best_distance = distances[best_match_index]

    if best_distance > 0.5:
        return {"error": "Face not recognized"}

    matched_user = users[best_match_index]

    today = datetime.utcnow().date()

    existing = db.attendance.find_one({
        "email": matched_user["email"],
        "date": str(today)
    })

    # 🟢 PUNCH IN
    if not existing:
        db.attendance.insert_one({
            "user_id": str(matched_user["_id"]),
            "email": matched_user["email"],
            "date": str(today),
            "punch_in": datetime.utcnow(),
            "punch_out": None,
            "hours": 0,
            "status": "incomplete"
        })

        return {
            "msg": "Punch in recorded",
            "user": matched_user["email"]
        }

    # 🔴 PUNCH OUT
    if existing and not existing.get("punch_out"):
        punch_out = datetime.utcnow()
        punch_in = existing["punch_in"]

        hours = (punch_out - punch_in).total_seconds() / 3600
        status = "present" if hours >= 8 else "incomplete"

        db.attendance.update_one(
            {"_id": existing["_id"]},
            {
                "$set": {
                    "punch_out": punch_out,
                    "hours": round(hours, 2),
                    "status": status
                }
            }
        )

        return {
            "msg": "Punch out recorded",
            "user": matched_user["email"],
            "hours": round(hours, 2),
            "status": status
        }

    return {
        "msg": "Attendance already completed",
        "user": matched_user["email"]
    }