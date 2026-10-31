# PeerTutor AI - Quick Start Guide

## 🚀 Accessing the Application

**Frontend (Streamlit)**: Open your browser and go to port 3000
- If running locally: http://localhost:3000
- If on Emergent: Your preview URL on port 3000

## 📱 Using PeerTutor AI

### Step 1: Upload PDF 📄
1. On home page, click "Choose a PDF file"
2. Select any academic PDF (notes, textbooks, papers)
3. Wait while AI extracts topics (~10-30 seconds)

### Step 2: Select Topics 🎯
1. Choose a main topic from dropdown
2. Select subtopics you want to study
3. Set number of questions (5-20)
4. Click "Start Quiz"

### Step 3: Take Quiz 📝
1. Read each question carefully
2. Click on your answer (A, B, C, or D)
3. Get instant feedback
4. Choose explanation style:
   - **Simple** 📚: Detailed explanation
   - **One-line** ⚡: Quick summary  
   - **Real-world** 🌍: Practical example
5. Click "Next Question"

### Step 4: Track Progress 📊
1. View your score after each question
2. Complete the quiz to see final results
3. Click "My Progress" in sidebar to see:
   - Total quizzes taken
   - Overall accuracy
   - Topics covered
   - Quiz history

## 🎓 Features

- **Any Academic Subject**: Works with OS, DBMS, Networks, AI, etc.
- **Adaptive Difficulty**: Starts easy, gets harder
- **Smart Questions**: AI understands content, not just keywords
- **Complex PDFs**: Handles tables, layouts, and formatting
- **Learn Your Way**: Three explanation styles
- **Track Growth**: See your improvement over time

## ⚙️ System Architecture

```
Frontend (Streamlit - Port 3000)
         ↓
Backend API (FastAPI - Port 8001)
         ↓
MongoDB (Data Storage - Port 27017)
         ↓
OpenAI GPT-4o-mini (via Emergent Key)
```

## 🔧 Technical Details

**Backend**: Python FastAPI
**Frontend**: Streamlit
**Database**: MongoDB
**LLM**: OpenAI GPT-4o-mini
**PDF Parser**: PyPDF2 + pdfplumber

## 📂 Project Structure

```
/app/
├── backend/
│   ├── server.py           # Main API
│   ├── llm_service.py      # LLM integration
│   ├── pdf_service.py      # PDF processing
│   └── .env                # Config
├── streamlit_app.py        # Streamlit UI
├── README.md               # Full documentation
└── TESTING_GUIDE.md        # Testing instructions
```

## 🎯 Best Practices

1. **PDF Quality**: Use clear, text-based PDFs for best results
2. **Quiz Length**: Start with 10 questions, adjust as needed
3. **Topics**: Select 2-3 subtopics for focused learning
4. **Explanations**: Try all three modes to understand concepts fully
5. **Progress**: Take multiple quizzes to build comprehensive stats

## 💡 Tips

- Upload lecture notes for targeted study sessions
- Use "Real-world" explanations to understand practical applications
- Check "My Progress" to identify weak areas
- Take quizzes on same topic to reinforce learning
- The system adapts: more correct answers = harder questions

## 🐛 Troubleshooting

**Problem**: PDF upload fails
- **Solution**: Ensure PDF is not password-protected or corrupted

**Problem**: No topics extracted
- **Solution**: PDF may not have enough text content

**Problem**: Quiz generation slow
- **Solution**: Normal for first-time generation, subsequent quizzes faster

**Problem**: Page not loading
- **Solution**: Check if services are running: `sudo supervisorctl status`

## 📊 What Makes This Different?

Traditional Systems:
- ❌ Manual question creation
- ❌ Static difficulty
- ❌ Pre-defined question banks
- ❌ No adaptation

PeerTutor AI:
- ✅ AI generates questions automatically
- ✅ Adapts to your performance
- ✅ Works with any content
- ✅ Semantic understanding

## 🎉 Success Metrics

After using PeerTutor AI, you'll have:
- ✅ Better understanding of topics
- ✅ Identified knowledge gaps
- ✅ Tracked learning progress
- ✅ Practiced with exam-style questions

---

**Start Learning Now!** 🚀 Upload your first PDF and experience adaptive learning powered by AI!
