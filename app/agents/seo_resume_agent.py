from __future__ import annotations

import os

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.postgres import PostgresStorage

from app.agents.promts.seo_resume_promt import SYSTEM_PROMPT
from app.tools.resume_tools import save_resume, list_resumes, get_resume, delete_resume, edit_resume

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://resume:resume@localhost:5452/resume_db")
tools = [save_resume, list_resumes, get_resume, delete_resume, edit_resume]


def create_seo_agent(session_id: str) -> Agent:
    seo_agent = Agent(
        name="Professional Resume Agent",
        role="Specialist in developing professional resumes.",
        description="Specialist in developing professional resumes, have access to the user resumos, for listing, editing, deleting and creating new resumes.",
        model=OpenAIChat(id="gpt-4.1-2025-04-14"),
        tools=tools,
        session_id=session_id,
        storage=PostgresStorage(table_name="agent_sessions", db_url=DATABASE_URL),
        add_history_to_messages=True,
        instructions=SYSTEM_PROMPT,
        markdown=True,
    )
    return seo_agent