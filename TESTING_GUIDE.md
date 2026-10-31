# PeerTutor AI - Testing Guide

## System Status ✅

All services are running successfully:

### Backend (FastAPI)
- **URL**: http://localhost:8001
- **Status**: RUNNING
- **Health Check**: /api/ endpoint returns {"message": "PeerTutor AI Backend", "status": "running"}

### Frontend (Streamlit)
- **URL**: http://localhost:3000  
- **Status**: RUNNING
- **Port**: 3000 (replacing React frontend)

### Database (MongoDB)
- **URL**: mongodb://localhost:27017
- **Database**: test_database
- **Status**: RUNNING

## Testing the Application

### 1. Access the Frontend
Navigate to: **http://localhost:3000** (or your preview URL on port 3000)

### 2. Test Flow

#### Step 1: Upload PDF
1. Click on "Choose a PDF file"
2. Upload any academic PDF (lecture notes, textbook, research paper)
3. Wait for processing (LLM extracts topics automatically)

#### Step 2: Select Topics
1. Choose a main topic from dropdown
2. Select subtopics to focus on
3. Choose number of questions (5-20)
4. Click "Start Quiz"

#### Step 3: Take Quiz
1. Read the question carefully
2. Select an answer (A, B, C, or D)
3. View immediate feedback
4. Choose explanation style:
   - **Simple**: Detailed explanation
   - **One-line**: Quick summary
   - **Real-world**: Practical application
5. Click "Next Question" to continue

#### Step 4: View Progress
1. Complete the quiz
2. View your score and accuracy
3. Navigate to "My Progress" in sidebar
4. See quiz history and statistics

## API Testing with curl

### 1. Health Check
```bash
curl http://localhost:8001/api/
```

### 2. Upload PDF (with actual PDF file)
```bash
curl -X POST "http://localhost:8001/api/upload-pdf" \
  -F "file=@/path/to/your/document.pdf"
```

### 3. Get User Progress
```bash
curl "http://localhost:8001/api/user-progress/test-user-123"
```

## Component Tests

### LLM Service Test
```bash
cd /app/backend
python3 -c "
import asyncio
from llm_service import LLMService

async def test():
    service = LLMService()
    sample = 'Operating Systems manage hardware. Key topics: Process Management, Memory Management.'
    result = await service.extract_topics_and_subtopics(sample)
    print(result)

asyncio.run(test())
"
```

### PDF Service Test
```bash
cd /app/backend
python3 -c "
from pdf_service import PDFService
service = PDFService()
print('PDF Service OK:', service)
"
```

## Expected Behavior

### PDF Upload
- ✅ Accepts PDF files
- ✅ Extracts text content
- ✅ LLM identifies topics and subtopics
- ✅ Returns structured topic data

### Quiz Generation
- ✅ Generates 5-20 questions
- ✅ Adaptive difficulty (easy → medium → hard)
- ✅ High-quality MCQs with 4 options
- ✅ Plausible distractors

### Quiz Taking
- ✅ One question at a time
- ✅ Immediate feedback
- ✅ Three explanation modes
- ✅ Score tracking

### Progress Tracking
- ✅ Stores all quiz sessions
- ✅ Calculates accuracy
- ✅ Tracks topics covered
- ✅ Shows history

## Troubleshooting

### Backend not responding
```bash
sudo supervisorctl restart backend
tail -f /var/log/supervisor/backend.err.log
```

### Streamlit not loading
```bash
sudo supervisorctl restart streamlit
tail -f /var/log/supervisor/streamlit.out.log
```

### MongoDB connection issues
```bash
sudo supervisorctl restart mongodb
mongo --eval "db.runCommand({ connectionStatus: 1 })"
```

### Check all services
```bash
sudo supervisorctl status
```

## Log Files

- **Backend Logs**: /var/log/supervisor/backend.{out,err}.log
- **Streamlit Logs**: /var/log/supervisor/streamlit.{out,err}.log
- **MongoDB Logs**: /var/log/mongodb.{out,err}.log

## Performance Notes

### PDF Processing
- Small PDFs (<10 pages): ~5-15 seconds
- Medium PDFs (10-50 pages): ~15-30 seconds
- Large PDFs (>50 pages): ~30-60 seconds

### Quiz Generation
- 10 questions: ~20-40 seconds
- 20 questions: ~40-80 seconds
- Depends on LLM API response time

## Features Implemented ✅

- [x] PDF upload and processing
- [x] Complex PDF support (tables, layouts)
- [x] LLM-based topic extraction
- [x] Adaptive MCQ generation
- [x] Three difficulty levels
- [x] Multiple explanation modes
- [x] User progress tracking
- [x] Quiz history
- [x] Interactive Streamlit UI
- [x] FastAPI backend
- [x] MongoDB persistence
- [x] CORS configuration

## Sample Test Scenarios

### Scenario 1: Operating Systems Quiz
1. Upload OS textbook chapter PDF
2. Topics extracted: Process Management, Memory Management, File Systems
3. Select "Process Management" topic
4. Take 10-question quiz
5. View explanations in different modes

### Scenario 2: Database Management Quiz
1. Upload DBMS notes PDF
2. Topics extracted: SQL, Normalization, Transactions
3. Select multiple subtopics
4. Complete adaptive quiz
5. Check progress dashboard

### Scenario 3: Progress Tracking
1. Complete multiple quizzes
2. Navigate to "My Progress"
3. View statistics:
   - Total quizzes taken
   - Questions answered
   - Overall accuracy
   - Topics covered
4. Review quiz history

## Known Limitations

1. **LLM Token Limits**: Very large PDFs (>100 pages) may be truncated
2. **Processing Time**: Complex PDFs take longer to process
3. **Question Quality**: Depends on PDF content quality
4. **Network Dependency**: Requires LLM API availability

## Success Criteria ✅

- ✅ Backend API responds correctly
- ✅ Streamlit UI loads and is interactive
- ✅ PDF upload works
- ✅ Topics are extracted using LLM
- ✅ Quizzes are generated adaptively
- ✅ Answers are validated correctly
- ✅ Explanations are provided
- ✅ Progress is tracked in MongoDB
- ✅ All services run via supervisor

---

**System Status**: All components operational ✅
**LLM Integration**: Working with Emergent Universal Key ✅
**Database**: MongoDB connected ✅
**Frontend**: Streamlit running on port 3000 ✅
