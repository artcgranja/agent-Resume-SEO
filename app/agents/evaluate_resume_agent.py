from __future__ import annotations

import os

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.postgres import PostgresStorage

from app.tools.evaluate_tools import save_evaluate_resume, get_evaluate_resume, list_evaluate_resumes, delete_evaluate_resume

from app.agents.promts.evaluate_resume_promt import SYSTEM_PROMPT

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://resume:resume@localhost:5452/resume_db")
tools = [save_evaluate_resume, get_evaluate_resume, list_evaluate_resumes, delete_evaluate_resume]


def create_evaluate_resume_agent(session_id: str) -> Agent:
    evaluate_resume_agent = Agent(
        name="Evaluate Resume Agent",
        role="Especialista em Avaliação de Currículos Profissionais",
        model=OpenAIChat(id="gpt-4.1-2025-04-14"),
        tools=tools,
        session_id=session_id,
        storage=PostgresStorage(table_name="agent_sessions", db_url=DATABASE_URL),
        add_history_to_messages=True,
        description=SYSTEM_PROMPT,
        markdown=True,
    )
    return evaluate_resume_agent