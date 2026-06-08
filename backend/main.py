from fastapi import FastAPI
from pydantic import BaseModel
from .model import get_answer
from fastapi.middleware.cors import CORSMiddleware
from .database import create_table, save_chat

app = FastAPI(
    title="GlowGuide AI API",
    description="AI skincare and healthy food recommendation API powered by Hugging Face",
    version="1.0.0"
)
create_table()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    question: str
    answer: str

@app.get("/")
def root():
    return {"status": "GlowGuide AI API is running!"}

@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):
    answer = get_answer(request.question)

    return AnswerResponse(
        question=request.question,
        answer=answer
    )