from sqlalchemy import Column, Integer, String, JSON
from app.database.base import BaseModel

class EvaluateResume(BaseModel):
    __tablename__ = "evaluate_resumes"
    name = Column(String)
    job_title = Column(String)
    company_name = Column(String)
    job_key_points = Column(JSON)
    overall_fit_score = Column(Integer)
    key_strengths = Column(JSON)
    gaps = Column(JSON)
    recommendation = Column(String)