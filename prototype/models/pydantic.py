from pydantic import BaseModel
from typing import List, Optional

class QuestionAnalysis(BaseModel):
    question_number: Optional[int] = None
    question_text: str
    answer_text: str
    blooms_level: str
    score: int = 0
    pros: List[str] = []
    cons: List[str] = []
    feedback: str = ""

class OverallAnalysis(BaseModel):
    strengths: List[str] = []
    weaknesses: List[str] = []
    final_feedback: str = ""

class ExamAnalysis(BaseModel):
    questions: List[QuestionAnalysis]
    overall_analysis: OverallAnalysis
