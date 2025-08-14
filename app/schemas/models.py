from __future__ import annotations

from typing import Any, Dict, List, Optional
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict


class ResumeSchema(BaseModel):
    name: str = Field(description="The name of the resume")
    content: str = Field(description="The content of the resume in markdown format")

    # Garante que o JSON Schema inclua additionalProperties: false
    # e rejeite campos não declarados
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "additionalProperties": False,
        },
    )

class EvaluateResumeSchema(BaseModel):
    name: str = Field(description="The name of the resume")
    job_title: str = Field(description="The job title of the resume")
    company_name: str = Field(description="The company name of the resume")
    job_key_points: List[str] = Field(description="The most important key points from the job description")
    overall_fit_score: int = Field(description="The overall fit score of the resume")
    key_strengths: List[str] = Field(description="The key strengths of the resume")
    gaps: List[str] = Field(description="The gaps of the resume")
    recommendation: str = Field(description="The recommendation of the resume")

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "additionalProperties": False,
        },
    )