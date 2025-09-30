from pydantic import BaseModel
from typing import List

class QuestionAnalysis(BaseModel):
    question_number: int
    question_text: str
    answer_text: str
    blooms_level: str
    score: int
    pros: List[str]
    cons: List[str]
    feedback: str

class OverallAnalysis(BaseModel):
    strengths: List[str]
    weaknesses: List[str]
    final_feedback: str

class ExamAnalysis(BaseModel):
    questions: List[QuestionAnalysis]
    overall_analysis: OverallAnalysis