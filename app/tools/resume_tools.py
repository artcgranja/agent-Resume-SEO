from __future__ import annotations

from typing import List
from agno.tools import tool
from app.schemas.models import ResumeSchema
from app.database.db_manager import get_db
from app.database.models.resume import Resume

@tool
def save_resume(resume: ResumeSchema) -> str:
    """
    This tool is used to save the resume in the database.
    Args:
        resume: resume schema is a pydantic model that contains the name and content of the resume {name: str, content: str}.
    Returns:
        A message indicating that the resume was saved successfully.
    """
    with get_db() as db:
        db_resume = Resume(name=resume.name, content=resume.content)
        db.add(db_resume)
        db.commit()
        db.refresh(db_resume)
    return "Resume saved successfully."

@tool
def list_resumes() -> List[str]:
    """
    This tool is used to get all the resumes from the database.
    Returns:
        A list with only the resume names.
    """
    with get_db() as db:
        db_resumes = db.query(Resume).all()
        return [resume.name for resume in db_resumes]

@tool
def get_resume(name: str) -> ResumeSchema:
    """
    This tool is used to get the resume from the database.
    Args:
        name: The name of the resume to get.
    Returns:
        The resume schema.
    """
    with get_db() as db:
        db_resume = db.query(Resume).filter(Resume.name == name).first()
        if db_resume is None:
            raise ValueError(f"Resume not found: {name}")
        return ResumeSchema(name=db_resume.name, content=db_resume.content)
    
@tool
def delete_resume(name: str) -> str:
    """
    This tool is used to delete the resume from the database.
    Args:
        name: The name of the resume to delete.
    Returns:
        A message indicating that the resume was deleted successfully.
    """
    with get_db() as db:
        db_resume = db.query(Resume).filter(Resume.name == name).first()
        if db_resume is None:
            raise ValueError(f"Resume not found: {name}")
        db.delete(db_resume)
        db.commit()
    return "Resume deleted successfully."

@tool
def edit_resume(name: str, content: str) -> str:
    """
    This tool is used to edit the resume in the database.
    Args:
        name: The name of the resume to edit.
        content: The new content of the resume.
    Returns:
        A message indicating that the resume was edited successfully.
    """
    with get_db() as db:
        db_resume = db.query(Resume).filter(Resume.name == name).first()
        if db_resume is None:
            raise ValueError(f"Resume not found: {name}")
        db_resume.content = content
        db.commit()
        db.refresh(db_resume)
    return "Resume edited successfully."