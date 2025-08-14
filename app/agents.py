from __future__ import annotations

import os

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.postgres import PostgresStorage

from .promts.system_promt import SYSTEM_PROMPT
from .tools import save_resume

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://resume:resume@localhost:5452/resume_db")


seo_agent = Agent(
    name="SEO Agent",
    role="Especialista em Desenvolvimento de Currículos Profissionais",
    model=OpenAIChat(id="gpt-4.1-2025-04-14"),
    tools=[save_resume],
    storage=PostgresStorage(table_name="agent_sessions", db_url=DATABASE_URL),
    add_history_to_messages=True,
    description=SYSTEM_PROMPT,
    markdown=True,
)