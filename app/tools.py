from __future__ import annotations

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