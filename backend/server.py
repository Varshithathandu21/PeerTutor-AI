from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime, timezone

# Import services
from llm_service import LLMService
from pdf_service import PDFService

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Initialize services
llm_service = LLMService()
pdf_service = PDFService()

# ==================== Models ====================

class PDFDocument(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    filename: str
    text_content: str
    topics: List[Dict[str, Any]] = []
    page_count: int
    uploaded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class QuizSession(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    pdf_id: str
    topic: str
    subtopics: List[str]
    questions: List[Dict[str, Any]] = []
    current_question: int = 0
    score: int = 0
    total_questions: int = 0
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    difficulty_progression: List[str] = []

class UserProgress(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    quiz_sessions: List[str] = []  # List of session IDs
    total_quizzes: int = 0
    total_questions_answered: int = 0
    correct_answers: int = 0
    accuracy: float = 0.0
    topics_covered: List[str] = []
    last_activity: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AnswerSubmission(BaseModel):
    session_id: str
    question_number: int
    selected_answer: str
    user_id: str

class QuizStartRequest(BaseModel):
    pdf_id: str
    topic: str
    subtopics: List[str]
    user_id: str
    num_questions: int = 10

# ==================== API Endpoints ====================

@api_router.get("/")
async def root():
    return {"message": "PeerTutor AI Backend", "status": "running"}

@api_router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload and process a PDF file
    Returns: PDF document ID and extracted topics
    """
    try:
        # Read PDF bytes
        pdf_bytes = await file.read()
        
        # Process PDF
        pdf_data = pdf_service.process_pdf(pdf_bytes)
        
        if not pdf_data["text"].strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        
        # Extract topics using LLM
        topics_result = await llm_service.extract_topics_and_subtopics(pdf_data["text"])
        
        # Create PDF document
        pdf_doc = PDFDocument(
            filename=file.filename,
            text_content=pdf_data["text"],
            topics=topics_result.get("topics", []),
            page_count=pdf_data.get("page_count", 0)
        )
        
        # Store in MongoDB
        doc = pdf_doc.model_dump()
        doc['uploaded_at'] = doc['uploaded_at'].isoformat()
        await db.pdf_documents.insert_one(doc)
        
        return {
            "pdf_id": pdf_doc.id,
            "filename": pdf_doc.filename,
            "topics": pdf_doc.topics,
            "page_count": pdf_doc.page_count,
            "message": "PDF processed successfully"
        }
        
    except Exception as e:
        logging.error(f"Error uploading PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/pdf/{pdf_id}")
async def get_pdf_info(pdf_id: str):
    """
    Get information about a processed PDF
    """
    pdf_doc = await db.pdf_documents.find_one({"id": pdf_id}, {"_id": 0})
    if not pdf_doc:
        raise HTTPException(status_code=404, detail="PDF not found")
    return pdf_doc

@api_router.post("/start-quiz")
async def start_quiz(request: QuizStartRequest):
    """
    Start a new quiz session
    Generates adaptive MCQs based on selected topic and subtopics
    """
    try:
        # Get PDF document
        pdf_doc = await db.pdf_documents.find_one({"id": request.pdf_id}, {"_id": 0})
        if not pdf_doc:
            raise HTTPException(status_code=404, detail="PDF not found")
        
        # Generate MCQs
        questions = await llm_service.generate_adaptive_mcqs(
            topic=request.topic,
            subtopics=request.subtopics,
            pdf_context=pdf_doc["text_content"],
            num_questions=request.num_questions
        )
        
        if not questions:
            raise HTTPException(status_code=500, detail="Could not generate questions")
        
        # Create quiz session
        quiz_session = QuizSession(
            user_id=request.user_id,
            pdf_id=request.pdf_id,
            topic=request.topic,
            subtopics=request.subtopics,
            questions=questions,
            total_questions=len(questions)
        )
        
        # Store in MongoDB
        doc = quiz_session.model_dump()
        doc['started_at'] = doc['started_at'].isoformat()
        if doc['completed_at']:
            doc['completed_at'] = doc['completed_at'].isoformat()
        await db.quiz_sessions.insert_one(doc)
        
        # Return first question (without answer)
        first_question = questions[0].copy()
        first_question.pop('correct_answer', None)
        
        return {
            "session_id": quiz_session.id,
            "total_questions": quiz_session.total_questions,
            "current_question": first_question
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error starting quiz: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/submit-answer")
async def submit_answer(submission: AnswerSubmission):
    """
    Submit an answer and get feedback with next question
    """
    try:
        # Get quiz session
        session = await db.quiz_sessions.find_one({"id": submission.session_id}, {"_id": 0})
        if not session:
            raise HTTPException(status_code=404, detail="Quiz session not found")
        
        current_q_idx = submission.question_number - 1
        if current_q_idx >= len(session["questions"]):
            raise HTTPException(status_code=400, detail="Invalid question number")
        
        current_question = session["questions"][current_q_idx]
        is_correct = submission.selected_answer == current_question["correct_answer"]
        
        # Update score
        if is_correct:
            session["score"] += 1
        
        # Update session
        session["current_question"] = submission.question_number
        session["difficulty_progression"].append(current_question.get("difficulty", "medium"))
        
        # Check if quiz is complete
        is_complete = submission.question_number >= session["total_questions"]
        
        if is_complete:
            session["completed_at"] = datetime.now(timezone.utc).isoformat()
            
            # Update user progress
            await update_user_progress(
                submission.user_id,
                session["id"],
                session["topic"],
                session["total_questions"],
                session["score"]
            )
        
        # Update session in DB
        await db.quiz_sessions.update_one(
            {"id": submission.session_id},
            {"$set": session}
        )
        
        # Prepare response
        response = {
            "is_correct": is_correct,
            "correct_answer": current_question["correct_answer"],
            "explanation_simple": current_question.get("explanation_simple", ""),
            "explanation_oneline": current_question.get("explanation_oneline", ""),
            "explanation_realworld": current_question.get("explanation_realworld", ""),
            "current_score": session["score"],
            "total_questions": session["total_questions"],
            "is_complete": is_complete
        }
        
        # If not complete, send next question
        if not is_complete:
            next_q_idx = submission.question_number
            next_question = session["questions"][next_q_idx].copy()
            next_question.pop('correct_answer', None)
            next_question.pop('explanation_simple', None)
            next_question.pop('explanation_oneline', None)
            next_question.pop('explanation_realworld', None)
            response["next_question"] = next_question
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error submitting answer: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/user-progress/{user_id}")
async def get_user_progress(user_id: str):
    """
    Get user's progress and statistics
    """
    progress = await db.user_progress.find_one({"user_id": user_id}, {"_id": 0})
    if not progress:
        return {
            "user_id": user_id,
            "total_quizzes": 0,
            "total_questions_answered": 0,
            "correct_answers": 0,
            "accuracy": 0.0,
            "topics_covered": []
        }
    return progress

@api_router.get("/quiz-history/{user_id}")
async def get_quiz_history(user_id: str):
    """
    Get user's quiz history
    """
    sessions = await db.quiz_sessions.find(
        {"user_id": user_id},
        {"_id": 0}
    ).sort("started_at", -1).to_list(100)
    
    return {"quiz_history": sessions}

# ==================== Helper Functions ====================

async def update_user_progress(
    user_id: str,
    session_id: str,
    topic: str,
    total_questions: int,
    correct_answers: int
):
    """
    Update user's progress after completing a quiz
    """
    progress = await db.user_progress.find_one({"user_id": user_id}, {"_id": 0})
    
    if not progress:
        progress = UserProgress(user_id=user_id).model_dump()
        progress['last_activity'] = progress['last_activity'].isoformat()
    
    # Update statistics
    progress["quiz_sessions"].append(session_id)
    progress["total_quizzes"] += 1
    progress["total_questions_answered"] += total_questions
    progress["correct_answers"] += correct_answers
    progress["accuracy"] = (progress["correct_answers"] / progress["total_questions_answered"]) * 100
    
    if topic not in progress["topics_covered"]:
        progress["topics_covered"].append(topic)
    
    progress["last_activity"] = datetime.now(timezone.utc).isoformat()
    
    # Upsert in MongoDB
    await db.user_progress.update_one(
        {"user_id": user_id},
        {"$set": progress},
        upsert=True
    )

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()