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