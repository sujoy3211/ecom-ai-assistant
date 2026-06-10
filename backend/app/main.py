from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.chat import router as chat_router

app = FastAPI(
    title="E-commerce AI Assistant",
    description="RAG-based product assistant powered by Gemini",
    version="1.0.0"
)

# Allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(chat_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "E-commerce AI Assistant is running! 🚀"}