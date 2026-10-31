"""
PeerTutor AI - Streamlit Frontend
LLM-Based Adaptive Academic Quiz Generator
"""

import streamlit as st
import requests
import uuid
from datetime import datetime
import time

# Backend API URL
BACKEND_URL = "http://localhost:8001/api"

# Page configuration
st.set_page_config(
    page_title="PeerTutor AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        text-align: center;
        color: #555;
        margin-bottom: 2rem;
    }
    .question-card {
        background-color: #ffffff !important;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid #cccccc;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .question-card h3 {
        color: #000000 !important;
        font-weight: 600;
        margin: 0;
        padding: 0;
    }
    .question-card * {
        color: #000000 !important;
    }
    .correct-answer {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 5px;
        color: #155724;
    }
    .wrong-answer {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 5px;
        color: #721c24;
    }
    .stats-box {
        background-color: #e7f3ff;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'pdf_id' not in st.session_state:
    st.session_state.pdf_id = None
if 'topics' not in st.session_state:
    st.session_state.topics = []
if 'quiz_session_id' not in st.session_state:
    st.session_state.quiz_session_id = None
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'quiz_total' not in st.session_state:
    st.session_state.quiz_total = 0
if 'selected_answer' not in st.session_state:
    st.session_state.selected_answer = None
if 'show_explanation' not in st.session_state:
    st.session_state.show_explanation = False
if 'explanation_type' not in st.session_state:
    st.session_state.explanation_type = 'simple'

def home_page():
    """Landing page with upload functionality"""
    st.markdown('<p class="main-header">📚 PeerTutor AI</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">LLM-Based Adaptive Academic Quiz Generator</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("Upload Your Academic PDF")
        st.write("Upload any academic document and let AI generate adaptive quizzes for you!")
        
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=['pdf'],
            help="Upload lecture notes, textbooks, research papers, or any academic content"
        )
        
        if uploaded_file is not None:
            with st.spinner("🔄 Processing PDF and extracting topics... This may take a moment."):
                try:
                    files = {'file': (uploaded_file.name, uploaded_file.getvalue(), 'application/pdf')}
                    response = requests.post(f"{BACKEND_URL}/upload-pdf", files=files, timeout=120)
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.pdf_id = data['pdf_id']
                        st.session_state.topics = data['topics']
                        st.session_state.page = 'topic_selection'
                        st.success(f"✅ Successfully processed {data['filename']}!")
                        st.rerun()
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Error uploading PDF: {str(e)}")
        
        st.markdown("---")
        
        # Features section
        st.subheader("✨ Features")
        feature_col1, feature_col2 = st.columns(2)
        
        with feature_col1:
            st.markdown("**🤖 AI-Powered Analysis**")
            st.write("Semantic understanding of content")
            st.markdown("**📊 Adaptive Difficulty**")
            st.write("Questions adjust to your level")
            st.markdown("**📈 Progress Tracking**")
            st.write("Monitor your learning journey")
        
        with feature_col2:
            st.markdown("**🎯 Topic-wise Quizzes**")
            st.write("Focus on specific concepts")
            st.markdown("**💡 Multiple Explanations**")
            st.write("Learn in your preferred style")
            st.markdown("**📚 Complex PDF Support**")
            st.write("Handles tables, images, and more")

def topic_selection_page():
    """Page to select topic and subtopics for quiz"""
    st.markdown('<p class="main-header">📋 Select Quiz Topics</p>', unsafe_allow_html=True)
    
    if not st.session_state.topics:
        st.error("No topics found. Please upload a PDF first.")
        if st.button("← Back to Home"):
            st.session_state.page = 'home'
            st.rerun()
        return
    
    st.markdown("---")
    
    # Topic selection
    st.subheader("1️⃣ Choose Main Topic")
    topic_names = [topic['topic_name'] for topic in st.session_state.topics]
    selected_topic_name = st.selectbox("Select a topic:", topic_names)
    
    # Find selected topic
    selected_topic = next(t for t in st.session_state.topics if t['topic_name'] == selected_topic_name)
    
    # Subtopic selection
    st.subheader("2️⃣ Choose Subtopics")
    if selected_topic['subtopics']:
        selected_subtopics = st.multiselect(
            "Select subtopics to focus on:",
            selected_topic['subtopics'],
            default=selected_topic['subtopics'][:3] if len(selected_topic['subtopics']) >= 3 else selected_topic['subtopics']
        )
    else:
        st.warning("No subtopics found for this topic.")
        selected_subtopics = [selected_topic_name]
    
    # Number of questions
    st.subheader("3️⃣ Quiz Settings")
    num_questions = st.slider("Number of questions:", 5, 20, 10)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
    
    with col3:
        if st.button("Start Quiz →", type="primary", use_container_width=True):
            if not selected_subtopics:
                st.error("Please select at least one subtopic!")
            else:
                with st.spinner("🎯 Generating adaptive quiz questions..."):
                    try:
                        payload = {
                            "pdf_id": st.session_state.pdf_id,
                            "topic": selected_topic_name,
                            "subtopics": selected_subtopics,
                            "user_id": st.session_state.user_id,
                            "num_questions": num_questions
                        }
                        response = requests.post(f"{BACKEND_URL}/start-quiz", json=payload, timeout=1200)
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.quiz_session_id = data['session_id']
                            st.session_state.current_question = data['current_question']
                            st.session_state.quiz_total = data['total_questions']
                            st.session_state.quiz_score = 0
                            st.session_state.selected_answer = None
                            st.session_state.show_explanation = False
                            st.session_state.page = 'quiz'
                            st.rerun()
                        else:
                            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"Error starting quiz: {str(e)}")

def quiz_page():
    """Quiz taking interface"""
    if not st.session_state.current_question:
        st.error("No active quiz. Please start a new quiz.")
        if st.button("← Back to Topics"):
            st.session_state.page = 'topic_selection'
            st.rerun()
        return
    
    question = st.session_state.current_question
    
    # Header
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"### Question {question['question_number']}/{st.session_state.quiz_total}")
    with col2:
        st.metric("Score", f"{st.session_state.quiz_score}/{st.session_state.quiz_total}")
    with col3:
        difficulty = question.get('difficulty', 'medium')
        color = {'easy': '🟢', 'medium': '🟡', 'hard': '🔴'}.get(difficulty, '🟡')
        st.metric("Difficulty", f"{color} {difficulty.upper()}")
    
    st.markdown("---")
    
    # Question
    st.markdown(f'<div class="question-card"><h3>{question["question"]}</h3></div>', unsafe_allow_html=True)
    
    # Options
    if not st.session_state.show_explanation:
        st.subheader("Choose your answer:")
        options = question['options']
        
        for key, value in options.items():
            if st.button(f"**{key}. {value}**", key=f"option_{key}", use_container_width=True):
                st.session_state.selected_answer = key
                st.session_state.show_explanation = True
                
                # Submit answer
                with st.spinner("Submitting answer..."):
                    try:
                        payload = {
                            "session_id": st.session_state.quiz_session_id,
                            "question_number": question['question_number'],
                            "selected_answer": key,
                            "user_id": st.session_state.user_id
                        }
                        response = requests.post(f"{BACKEND_URL}/submit-answer", json=payload, timeout=60)
                        
                        if response.status_code == 200:
                            st.session_state.answer_response = response.json()
                            if st.session_state.answer_response['is_correct']:
                                st.session_state.quiz_score += 1
                            st.rerun()
                        else:
                            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"Error submitting answer: {str(e)}")
    
    else:
        # Show explanation
        answer_data = st.session_state.answer_response
        
        if answer_data['is_correct']:
            st.markdown(f'<div class="correct-answer">✅ Correct! Well done!</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="wrong-answer">❌ Incorrect. The correct answer is: {answer_data["correct_answer"]}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Explanation type selector
        st.subheader("📖 Explanation")
        explanation_type = st.radio(
            "Choose explanation style:",
            ['Simple', 'One-line', 'Real-world'],
            horizontal=True,
            key="explanation_radio"
        )
        
        explanation_map = {
            'Simple': answer_data.get('explanation_simple', ''),
            'One-line': answer_data.get('explanation_oneline', ''),
            'Real-world': answer_data.get('explanation_realworld', '')
        }
        
        st.info(explanation_map[explanation_type])
        
        st.markdown("---")
        
        # Next question or finish
        if answer_data['is_complete']:
            st.balloons()
            st.success(f"🎉 Quiz Complete! Final Score: {answer_data['current_score']}/{answer_data['total_questions']}")
            accuracy = (answer_data['current_score'] / answer_data['total_questions']) * 100
            st.metric("Accuracy", f"{accuracy:.1f}%")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("View Progress", use_container_width=True):
                    st.session_state.page = 'progress'
                    st.rerun()
            with col2:
                if st.button("New Quiz", type="primary", use_container_width=True):
                    st.session_state.page = 'topic_selection'
                    st.session_state.show_explanation = False
                    st.rerun()
        else:
            if st.button("Next Question →", type="primary", use_container_width=True):
                st.session_state.current_question = answer_data['next_question']
                st.session_state.selected_answer = None
                st.session_state.show_explanation = False
                st.rerun()

def progress_page():
    """User progress tracking page"""
    st.markdown('<p class="main-header">📈 Your Progress</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    with st.spinner("Loading progress data..."):
        try:
            response = requests.get(f"{BACKEND_URL}/user-progress/{st.session_state.user_id}", timeout=30)
            
            if response.status_code == 200:
                progress = response.json()
                
                # Statistics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown('<div class="stats-box">', unsafe_allow_html=True)
                    st.metric("Total Quizzes", progress['total_quizzes'])
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown('<div class="stats-box">', unsafe_allow_html=True)
                    st.metric("Questions Answered", progress['total_questions_answered'])
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col3:
                    st.markdown('<div class="stats-box">', unsafe_allow_html=True)
                    st.metric("Correct Answers", progress['correct_answers'])
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col4:
                    st.markdown('<div class="stats-box">', unsafe_allow_html=True)
                    st.metric("Accuracy", f"{progress['accuracy']:.1f}%")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Topics covered
                if progress['topics_covered']:
                    st.subheader("📚 Topics Covered")
                    st.write(", ".join(progress['topics_covered']))
                
                # Quiz history
                st.markdown("---")
                st.subheader("📜 Quiz History")
                
                history_response = requests.get(f"{BACKEND_URL}/quiz-history/{st.session_state.user_id}", timeout=30)
                if history_response.status_code == 200:
                    history = history_response.json()['quiz_history']
                    
                    if history:
                        for session in history[:10]:  # Show last 10
                            with st.expander(f"{session['topic']} - {session['score']}/{session['total_questions']} - {session.get('started_at', 'N/A')}"):
                                st.write(f"**Subtopics:** {', '.join(session['subtopics'])}")
                                st.write(f"**Score:** {session['score']}/{session['total_questions']}")
                                accuracy = (session['score'] / session['total_questions'] * 100) if session['total_questions'] > 0 else 0
                                st.write(f"**Accuracy:** {accuracy:.1f}%")
                    else:
                        st.info("No quiz history yet. Start taking quizzes!")
                
            else:
                st.error("Could not load progress data")
        except Exception as e:
            st.error(f"Error loading progress: {str(e)}")
    
    st.markdown("---")
    if st.button("← Back to Home"):
        st.session_state.page = 'home'
        st.rerun()

# Sidebar
with st.sidebar:
    st.title("🎯 Navigation")
    st.markdown("---")
    
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = 'home'
        st.rerun()
    
    if st.session_state.pdf_id:
        if st.button("📋 Select Topics", use_container_width=True):
            st.session_state.page = 'topic_selection'
            st.rerun()
    
    if st.button("📈 My Progress", use_container_width=True):
        st.session_state.page = 'progress'
        st.rerun()
    
    st.markdown("---")
    st.markdown("### About")
    st.info("**PeerTutor AI** uses advanced LLM technology to create adaptive quizzes from your academic materials.")
    
    st.markdown("### User ID")
    st.code(st.session_state.user_id[:8] + "...")

# Main page routing
if st.session_state.page == 'home':
    home_page()
elif st.session_state.page == 'topic_selection':
    topic_selection_page()
elif st.session_state.page == 'quiz':
    quiz_page()
elif st.session_state.page == 'progress':
    progress_page()
