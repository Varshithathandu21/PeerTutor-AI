# 📚 PeerTutor AI – LLM-Based Adaptive Academic Quiz Generator

An intelligent, AI-powered quiz generation platform that transforms academic PDF documents into interactive quizzes with progressive difficulty levels and detailed explanations.

## 📖 Project Overview

PeerTutor AI is an AI-powered academic quiz generation system designed to make learning more interactive and personalized.

Instead of depending on predefined question banks, the application uses a Large Language Model (LLM) to understand uploaded academic materials, identify important topics and generate context-based multiple-choice questions.

Students can upload academic PDF documents, select topics and subtopics, and assess their understanding through interactive quizzes.

The system also provides multiple explanation formats and tracks learning progress using MongoDB.

## 🎯 Problem Statement

Traditional academic quiz systems often depend on manually created question banks and fixed assessments. This makes quiz preparation time-consuming and limits the ability to generate questions from individual study materials.

Students need a flexible assessment system that can understand their learning materials, generate relevant questions and provide explanations at different difficulty levels.

## 💡 Proposed Solution

PeerTutor AI addresses these challenges through an automated LLM-based quiz generation platform that:

- Extracts academic content from PDF documents.
- Identifies meaningful topics and subtopics using an LLM.
- Generates multiple-choice questions based on uploaded content.
- Organizes questions into progressive difficulty levels.
- Provides detailed explanations in multiple formats.
- Tracks quiz performance and learning progress.

## ✨ Key Features

### 🤖 LLM-Based Content Understanding

- Analyzes uploaded academic documents.
- Extracts meaningful topics and subtopics.
- Supports different academic subjects and technical domains.
- Generates questions using extracted document context.

### 📊 Progressive Difficulty Quiz Generation

- Generates multiple-choice questions from selected topics.
- Supports easy, medium and hard difficulty levels.
- Follows a predefined progressive difficulty sequence.
- Provides four answer options with one correct answer.
- Generates exam-oriented questions based on the uploaded material.

### 💡 Multiple Explanation Modes

Each generated question supports three explanation styles:

- **Simple Explanation:** Helps students understand the concept in detail.
- **One-Line Explanation:** Provides a concise summary for quick revision.
- **Real-World Explanation:** Connects theoretical concepts to practical applications.

### 📄 PDF Processing

- Accepts academic PDF documents.
- Extracts text using PyPDF2 and pdfplumber.
- Supports extraction of tables and structured content.
- Uses a fallback extraction strategy when necessary.

### 📈 Learning Progress Tracking

- Maintains quiz session information.
- Tracks quiz performance and statistics.
- Records completed quiz sessions.
- Maintains topic-wise learning information.
- Provides access to previous quiz history.

## 🛠️ Technology Stack

| Component | Technologies |
|---|---|
| Programming Language | Python |
| Primary Frontend | Streamlit |
| Backend Framework | FastAPI |
| Database | MongoDB |
| LLM Integration | Ollama |
| LLM Model | Gemma 3 (4B) |
| PDF Processing | PyPDF2, pdfplumber |
| Database Driver | Motor |
| API Communication | REST API, Requests |
| Additional Frontend Components | React, JavaScript, CSS |

## 🏗️ System Architecture

The application follows a frontend-backend architecture.

1. **Streamlit Frontend:** Provides the interface for PDF uploads, topic selection, quiz interaction and progress tracking.
2. **FastAPI Backend:** Handles API requests, quiz sessions, PDF processing and communication with the LLM.
3. **PDF Processing Service:** Extracts text and tables from uploaded academic documents.
4. **LLM Service:** Uses Ollama with Gemma 3 (4B) to extract topics and generate questions and explanations.
5. **MongoDB:** Stores application data, including PDF information, quiz sessions and user progress.

### System Workflow

```text
                  User
                    |
                    v
            Upload Academic PDF
                    |
                    v
            Streamlit Frontend
                    |
                    v
              FastAPI Backend
                    |
                    v
             PDF Processing
                    |
                    v
              Text Extraction
                    |
                    v
             Ollama - Gemma 3
                    |
                    v
       Topic and Subtopic Extraction
                    |
                    v
              Topic Selection
                    |
                    v
         Adaptive MCQ Generation
                    |
                    v
                 Take Quiz
                    |
                    v
          Feedback and Explanations
                    |
                    v
         MongoDB - Progress Tracking
```

## 📂 Project Structure

```text
PeerTutorAI/
│
├── backend/
│   ├── server.py
│   ├── llm_service.py
│   ├── pdf_service.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── README.md
│
├── memory/
│
├── tests/
│
├── test_reports/
│
├── streamlit_app.py
├── start_project.bat
├── start_streamlit.sh
│
├── README.md
├── PROJECT_OVERVIEW.md
├── QUICKSTART.md
└── .gitignore
```

## ⚙️ System Requirements

### Software Requirements

- Python 3.11 or later
- MongoDB (local installation or MongoDB Atlas)
- Ollama
- Gemma 3 (4B) model
- Visual Studio Code or another Python IDE
- Modern web browser

### Hardware Requirements

- Computer capable of running Python and MongoDB.
- Sufficient memory and storage to run the local LLM.
- Internet connection for initial software and model downloads.

## 🚀 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Varshithathandu21/PeerTutor-AI.git
cd PeerTutor-AI
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Python Dependencies

```bash
pip install -r backend/requirements.txt
```

Install Ollama's Python package if it is not already included:

```bash
pip install ollama
```

### 4. Install and Configure Ollama

Download and install Ollama:

https://ollama.com/

Download the required model:

```bash
ollama pull gemma3:4b
```

Make sure Ollama is running before starting the application.

### 5. Configure MongoDB

You can use either MongoDB Community Server or MongoDB Atlas.

Create an environment configuration file at `backend/.env`.

Example:

```env
MONGO_URL=your_mongodb_connection_string
DB_NAME=peertutor
CORS_ORIGINS=*
```

For a local MongoDB installation, the connection string can be:

```env
MONGO_URL=mongodb://localhost:27017
```

For MongoDB Atlas, use your own Atlas connection string.

**Important:** Never upload your actual `.env` file, database password or other credentials to GitHub.

### 6. Start the Backend

Open a terminal in the project root:

```powershell
cd backend
..\venv\Scripts\Activate.ps1
python -m uvicorn server:app --host 127.0.0.1 --port 8001
```

Backend address:

http://127.0.0.1:8001

### 7. Start the Streamlit Frontend

Open a second terminal in the project root:

```powershell
.\venv\Scripts\Activate.ps1
python -m streamlit run streamlit_app.py
```

Frontend address:

http://localhost:8501

Keep both services running while using the application.

## 🔌 API Endpoints

The FastAPI backend provides the following REST API endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/` | Check backend status |
| POST | `/api/upload-pdf` | Upload and process academic PDFs |
| GET | `/api/pdf/{pdf_id}` | Retrieve processed PDF information |
| POST | `/api/start-quiz` | Generate and start a quiz |
| POST | `/api/submit-answer` | Submit an answer and receive feedback |
| GET | `/api/user-progress/{user_id}` | Retrieve user progress and statistics |
| GET | `/api/quiz-history/{user_id}` | Retrieve previous quiz sessions |

## 🎓 How It Works

### Step 1 – Upload PDF

The user uploads an academic PDF containing study materials, lecture notes or technical content.

### Step 2 – Content Extraction

The PDF processing service extracts text and available tables using PyPDF2 and pdfplumber.

### Step 3 – Topic Identification

The LLM analyzes the extracted content and identifies relevant topics and subtopics.

### Step 4 – Topic Selection

The user selects a main topic and relevant subtopics for quiz generation.

### Step 5 – Quiz Generation

The LLM generates context-based multiple-choice questions following a progressive difficulty sequence:

- **Easy:** First 3 questions – Basic understanding and recall.
- **Medium:** Next 4 questions – Application and comprehension.
- **Hard:** Final 3 questions – Analysis and synthesis.

### Step 6 – Quiz Assessment

The user answers questions individually and receives immediate feedback, correct answers and explanations.

### Step 7 – Progress Tracking

Completed quiz information and performance statistics are stored in MongoDB for future reference.

## 🌟 Key Advantages

- **Automated Assessment:** Reduces the need to manually prepare questions.
- **Context-Based Generation:** Generates questions from uploaded study materials.
- **Domain Flexibility:** Can be used with different academic subjects.
- **Progressive Difficulty:** Organizes questions from easy to hard.
- **Conceptual Learning:** Provides multiple explanation styles.
- **Local LLM Integration:** Uses Ollama and Gemma 3 without requiring a paid LLM API key.

## 🔮 Future Enhancements

- Support for additional document formats such as DOCX and PPT.
- OCR support for scanned academic documents.
- More advanced adaptive difficulty based on student performance.
- Multilingual quiz generation.
- Collaborative quiz sessions.
- Advanced learning analytics and performance visualization.
- Improved question validation and quality evaluation.

## ⚠️ Current Limitations

- Question quality depends on the quality of extracted PDF content and LLM responses.
- Scanned PDFs may require an additional OCR component.
- Local LLM performance depends on available system resources.
- MongoDB and Ollama must be configured and running for the corresponding application features to work.
- The current difficulty progression follows a predefined sequence rather than dynamically adapting to each student's answers.

## 👩‍💻 Project Information

**Project Name:** PeerTutor AI

**Category:** Artificial Intelligence / Educational Technology

**Project Type:** LLM-Based Academic Quiz Generation System

**Primary Technologies:** Python, FastAPI, Streamlit, MongoDB, Ollama and Gemma 3 (4B)

---

**Built with ❤️ to make academic learning more interactive, accessible and effective.**
