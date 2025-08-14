from __future__ import annotations

from typing import List
from agno.tools import tool
from app.schemas.models import EvaluateResumeSchema
from app.database.db_manager import get_db
from app.database.models.evaluate import EvaluateResume

@tool
def save_evaluate_resume(evaluate_resume: EvaluateResumeSchema) -> str:
    """
    This tool is used to save the evaluate resume in the database.
    Args:
        evaluate_resume: evaluate resume schema is a pydantic model that contains the name and content of the evaluate resume {
            name: str,
            job_title: str,
            company_name: str,
            job_key_points: List[str],
            overall_fit_score: int,
            key_strengths: List[str],
            gaps: List[str],
            recommendation: str
        }.
    Returns:
        A message indicating that the evaluate resume was saved successfully.
    """
    with get_db() as db:
        db_evaluate_resume = EvaluateResume(
            name=evaluate_resume.name,
            job_title=evaluate_resume.job_title,
            company_name=evaluate_resume.company_name,
            job_key_points=evaluate_resume.job_key_points,
            overall_fit_score=evaluate_resume.overall_fit_score,
            key_strengths=evaluate_resume.key_strengths,
            gaps=evaluate_resume.gaps,
            recommendation=evaluate_resume.recommendation,
        )
        db.add(db_evaluate_resume)
        db.commit()
        db.refresh(db_evaluate_resume)
    return "Evaluate resume saved successfully."

@tool
def get_evaluate_resume(name: str) -> EvaluateResumeSchema:
    """
    This tool is used to get the evaluate resume from the database.
    Args:
        name: The name of the evaluate resume to get.
    Returns:
        The evaluate resume schema.
    """
    with get_db() as db:
        db_evaluate_resume = db.query(EvaluateResume).filter(EvaluateResume.name == name).first()
        if db_evaluate_resume is None:
            raise ValueError(f"Evaluate resume not found: {name}")
        return EvaluateResumeSchema(
            name=db_evaluate_resume.name,
            job_title=db_evaluate_resume.job_title,
            company_name=db_evaluate_resume.company_name,
            job_key_points=db_evaluate_resume.job_key_points,
            overall_fit_score=db_evaluate_resume.overall_fit_score,
            key_strengths=db_evaluate_resume.key_strengths,
            gaps=db_evaluate_resume.gaps,
            recommendation=db_evaluate_resume.recommendation,
        )
    
@tool
def list_evaluate_resumes() -> List[str]:
    """
    This tool is used to list all the evaluate resumes from the database.
    Returns:
        A list of evaluate resume names.
    """
    with get_db() as db:
        db_evaluate_resumes = db.query(EvaluateResume).all()
        return [evaluate_resume.name for evaluate_resume in db_evaluate_resumes]
    
@tool
def delete_evaluate_resume(name: str) -> str:
    """
    This tool is used to delete the evaluate resume from the database.
    Args:
        name: The name of the evaluate resume to delete.
    Returns:
        A message indicating that the evaluate resume was deleted successfully.
    """
    with get_db() as db:
        db_evaluate_resume = db.query(EvaluateResume).filter(EvaluateResume.name == name).first()
        if db_evaluate_resume is None:
            raise ValueError(f"Evaluate resume not found: {name}")
        db.delete(db_evaluate_resume)
        db.commit()
    return "Evaluate resume deleted successfully."