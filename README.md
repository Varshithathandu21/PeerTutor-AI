# PeerTutor AI - LLM-Based Adaptive Academic Quiz Generator

## 📚 Project Overview

PeerTutor AI is an intelligent quiz generation system that leverages Large Language Models (LLMs) to create adaptive assessments from academic PDF documents. The system uses semantic understanding rather than rule-based heuristics to generate high-quality, exam-oriented questions.

## ✨ Key Features

### 🤖 LLM-Based Semantic Analysis
- **Generalized PDF Understanding**: Works across any academic domain (COOS, OS, DBMS, CN, AI, etc.)
- **Complete PDF Reading**: Processes entire document content
- **Semantic Topic Extraction**: Identifies meaningful concepts and subtopics

### 📊 Adaptive Question Generation
- **Dynamic Difficulty**: Progresses from easy → medium → hard
- **Contextual Questions**: Generated based on actual content understanding
- **High-Quality MCQs**: 
  - One correct answer
  - Three plausible distractors
  - Non-obvious, exam-relevant options

### 💡 Multiple Explanation Modes
- **Simple**: Detailed conceptual explanation for thorough understanding
- **One-line**: Concise summary for quick review
- **Real-world**: Practical application context for deeper learning

### 📈 User Progress Tracking
- Quiz history and statistics
- Topic-wise performance tracking
- Overall accuracy monitoring
- Learning journey visualization

### 📚 Complex PDF Support
- Handles text, tables, and structured content
- Works with various PDF formats and layouts
- Robust extraction using multiple parsing strategies

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: MongoDB (for sessions and progress)
- **PDF Processing**: PyPDF2 + pdfplumber
- **LLM Integration**: OpenAI GPT-4o-mini via emergentintegrations
- **API Key**: Emergent Universal LLM Key

### Frontend
- **Framework**: Streamlit
- **UI**: Interactive web interface
- **Port**: 3000

## 🏗️ Architecture

### Backend Components

1. **server.py**: Main FastAPI application
   - API endpoints for PDF upload, quiz generation, answer submission
   - MongoDB integration for data persistence
   - CORS configuration

2. **llm_service.py**: LLM Integration Service
   - Topic and subtopic extraction
   - Adaptive MCQ generation
   - Multi-level explanation generation
   - Uses OpenAI GPT-4o-mini

3. **pdf_service.py**: PDF Processing Service
   - Text extraction from complex PDFs
   - Table and layout handling
   - Fallback mechanisms for different PDF types

### Frontend Components

1. **streamlit_app.py**: Main Streamlit Application
   - PDF upload interface
   - Topic selection UI
   - Interactive quiz interface
   - Progress tracking dashboard

### Database Schema

**Collections:**
- `pdf_documents`: Stores uploaded PDFs and extracted content
- `quiz_sessions`: Tracks active and completed quiz sessions
- `user_progress`: Maintains user statistics and history

## 📋 API Endpoints

### POST /api/upload-pdf
- Upload and process academic PDF
- Extract topics and subtopics using LLM
- Returns: PDF ID and topic list

### POST /api/start-quiz
- Start a new quiz session
- Generate adaptive MCQs based on selected topics
- Returns: Session ID and first question

### POST /api/submit-answer
- Submit answer for current question
- Get feedback and next question
- Returns: Correctness, explanations, next question

### GET /api/user-progress/{user_id}
- Retrieve user's overall statistics
- Returns: Quiz counts, accuracy, topics covered

### GET /api/quiz-history/{user_id}
- Get user's quiz history
- Returns: List of completed sessions

## 🚀 Setup & Installation

### Prerequisites
- Python 3.11+
- MongoDB
- Emergent Universal LLM Key (pre-configured)

### Dependencies Installed
```bash
# Backend dependencies
streamlit
PyPDF2
pdfplumber
fastapi
motor (MongoDB async driver)
emergentintegrations
```

### Environment Variables
```bash
# /app/backend/.env
MONGO_URL="mongodb://localhost:27017"
DB_NAME="test_database"
CORS_ORIGINS="*"
EMERGENT_LLM_KEY=sk-emergent-51dE20884850fEbD6B
```

## 🎯 How It Works

### 1. PDF Upload
- User uploads academic PDF document
- System extracts text using PyPDF2/pdfplumber
- LLM analyzes content and identifies topics/subtopics

### 2. Quiz Generation
- User selects topic and subtopics
- LLM generates adaptive questions:
  - Easy questions (first 3): Test basic understanding
  - Medium questions (next 4): Test application
  - Hard questions (last 3): Test analysis

### 3. Quiz Taking
- User answers questions one by one
- System provides immediate feedback
- Multiple explanation styles available
- Progress tracked in real-time

### 4. Progress Tracking
- All quiz sessions stored in database
- Statistics calculated automatically
- Historical performance available

## 🔑 Key Advantages Over Traditional Systems

1. **Semantic Understanding**: Uses LLM to understand content meaning, not just keywords
2. **Domain Agnostic**: Works across all academic subjects
3. **Adaptive Difficulty**: Questions adjust based on progression
4. **Quality Explanations**: Multiple learning styles supported
5. **Robust PDF Handling**: Works with complex documents

## 📊 System Flow

```
User uploads PDF
    ↓
PDF text extraction (PyPDF2/pdfplumber)
    ↓
LLM analyzes content → Extracts topics/subtopics
    ↓
User selects topics
    ↓
LLM generates adaptive MCQs
    ↓
User takes quiz → Answers submitted
    ↓
System provides explanations
    ↓
Progress saved to MongoDB
```

## 🎓 Academic Context

### Problem Addressed
Traditional quiz systems are:
- Manual and time-consuming
- Static and not adaptive
- Limited to predefined question banks
- Unable to understand semantic meaning

### Solution Provided
LLM-based system that:
- Automatically generates questions from any document
- Adapts difficulty dynamically
- Understands concepts semantically
- Provides personalized learning experience

## 🌟 Use Cases

1. **Students**: Self-assessment from lecture notes
2. **Educators**: Quick quiz generation from materials
3. **Researchers**: Testing comprehension of papers
4. **Learners**: Adaptive study sessions

## 🔧 Running the Application

### Services Running
- **Backend**: http://localhost:8001 (FastAPI)
- **Frontend**: http://localhost:3000 (Streamlit)
- **MongoDB**: localhost:27017

### Access the Application
Open browser and navigate to the frontend URL (port 3000)

### Supervisor Status
```bash
sudo supervisorctl status
# backend: RUNNING
# streamlit: RUNNING
# mongodb: RUNNING
```

## 📝 Future Enhancements

- Support for more document formats (DOCX, PPT)
- Audio/video content processing
- Collaborative quiz sessions
- Advanced analytics and insights
- Multi-language support
- Custom difficulty algorithms

## 🏆 Project Highlights

- **LLM Integration**: Uses cutting-edge GPT-4o-mini
- **Adaptive Learning**: Dynamic difficulty progression
- **User-Centric**: Multiple explanation modes
- **Robust**: Complex PDF support with fallbacks
- **Scalable**: MongoDB for data persistence
- **Modern Stack**: FastAPI + Streamlit

---

**Built with ❤️ using OpenAI GPT-4o-mini and Emergent Universal LLM Key**
