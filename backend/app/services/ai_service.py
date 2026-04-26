from app.db import db
from datetime import datetime, time


def process_query(query: str):

    query = query.lower().strip()
    today = str(datetime.utcnow().date())

    # -------------------------
    # 🔴 LATE EMPLOYEES
    # -------------------------
    if "late" in query:

        cutoff = datetime.combine(datetime.utcnow().date(), time(10, 0))

        records = db.attendance.find({
            "date": today,
            "punch_in": {"$exists": True}
        })

        late_users = []

        for r in records:
            if r.get("punch_in") and r["punch_in"] > cutoff:
                late_users.append(r["email"])

        return {
            "type": "late",
            "count": len(late_users),
            "data": late_users
        }

    # -------------------------
    # 🟡 LESS THAN 8 HOURS
    # -------------------------
    if "less than 8" in query or "short hours" in query:

        records = db.attendance.find({
            "date": today,
            "hours": {"$exists": True}
        })

        users = [r["email"] for r in records if r.get("hours", 0) < 8]

        return {
            "type": "underworked",
            "count": len(users),
            "data": users
        }

    # -------------------------
    # 🟢 SUMMARY
    # -------------------------
    if "summary" in query:

        total = db.attendance.count_documents({"date": today})
        present = db.attendance.count_documents({
            "date": today,
            "status": "present"
        })

        return {
            "type": "summary",
            "total": total,
            "present": present,
            "absent": total - present
        }

    # -------------------------
    # ❌ DEFAULT
    # -------------------------
    return {
        "type": "fallback",
        "message": "Try: late, less than 8 hours, or summary"
    }