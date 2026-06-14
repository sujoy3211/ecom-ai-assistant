from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.rag_service import get_ai_response

router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []

class ChatResponse(BaseModel):
    answer: str
    relevant_products: list
    best_deal: dict | None = None

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    result = get_ai_response(request.message, request.history)
    return ChatResponse(
        answer=result["answer"],
        relevant_products=result["relevant_products"],
        best_deal=result.get("best_deal")
    )