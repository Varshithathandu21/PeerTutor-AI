"""
LLM Service for PeerTutor AI
Handles all interactions with Ollama (Local LLM)
"""

import json
import ollama
from typing import List, Dict, Any


class LLMService:
    def __init__(self):
        self.model = "gemma3:4b"

    # ---------------------------------------------------
    # Extract Topics and Subtopics
    # ---------------------------------------------------
    async def extract_topics_and_subtopics(self, pdf_text: str) -> Dict[str, Any]:
        prompt = f"""
Analyze the following academic text and extract the main topics and their subtopics.

Text:
{pdf_text[:8000]}

Return ONLY valid JSON in this exact format:
{{
    "topics": [
        {{
            "topic_name": "Main Topic Name",
            "subtopics": ["Subtopic 1", "Subtopic 2", "Subtopic 3"]
        }}
    ]
}}
"""

        try:
            response = ollama.chat(
                model=self.model,
                format="json",  # 🔥 THIS FORCES STRICT JSON
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert academic content analyzer. Respond ONLY in valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
            )

            result = json.loads(response["message"]["content"])
            return result if "topics" in result else {"topics": []}

        except Exception as e:
            print(f"Topic extraction error: {e}")
            return {"topics": []}

    # ---------------------------------------------------
    # Generate Single MCQ
    # ---------------------------------------------------
    async def generate_mcq(
        self,
        topic: str,
        subtopic: str,
        difficulty: str,
        pdf_context: str
    ) -> Dict[str, Any]:

        difficulty_guidelines = {
            "easy": "Test basic understanding and recall.",
            "medium": "Test application and comprehension.",
            "hard": "Test analysis and synthesis."
        }

        prompt = f"""
Create ONE multiple-choice question.

Topic: {topic}
Subtopic: {subtopic}
Difficulty: {difficulty} - {difficulty_guidelines.get(difficulty, '')}

Context:
{pdf_context[:3000]}

Return ONLY valid JSON in this format:
{{
    "question": "Question text?",
    "options": {{
        "A": "Option A",
        "B": "Option B",
        "C": "Option C",
        "D": "Option D"
    }},
    "correct_answer": "A",
    "explanation_simple": "Detailed explanation",
    "explanation_oneline": "Short explanation",
    "explanation_realworld": "Real world example"
}}
"""

        try:
            response = ollama.chat(
                model=self.model,
                format="json",  # 🔥 STRICT JSON
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert quiz creator. Respond ONLY in valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
            )

            result = json.loads(response["message"]["content"])
            return result

        except Exception as e:
            print(f"MCQ generation error: {e}")
            return None

    # ---------------------------------------------------
    # Generate Adaptive MCQs (UNCHANGED LOGIC)
    # ---------------------------------------------------
    async def generate_adaptive_mcqs(
        self,
        topic: str,
        subtopics: List[str],
        pdf_context: str,
        num_questions: int = 10
    ) -> List[Dict[str, Any]]:

        questions = []
        difficulty_sequence = ["easy"] * 3 + ["medium"] * 4 + ["hard"] * 3

        for i in range(min(num_questions, len(difficulty_sequence))):
            subtopic = subtopics[i % len(subtopics)]
            difficulty = difficulty_sequence[i]

            mcq = await self.generate_mcq(topic, subtopic, difficulty, pdf_context)

            if mcq:
                mcq["difficulty"] = difficulty
                mcq["question_number"] = i + 1
                questions.append(mcq)

        return questions
