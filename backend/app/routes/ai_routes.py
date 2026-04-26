from fastapi import APIRouter
from app.services.ai_service import process_query

router = APIRouter(prefix="/ai")


@router.post("/ask")
def ask_ai(data: dict):
    return process_query(data["query"])