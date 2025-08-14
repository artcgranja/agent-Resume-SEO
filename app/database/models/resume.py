from sqlalchemy import Column, Integer, String, DateTime
from app.database.base import BaseModel

class Resume(BaseModel):
    __tablename__ = "resumes"
    name = Column(String)
    content = Column(String)