from __future__ import annotations

import os

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.storage.postgres import PostgresStorage

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://resume:resume@localhost:5452/resume_db")

def create_web_agent(session_id: str) -> Agent:
    web_agent = Agent(
        name="Web Search Agent",
        role="Handle web search requests",
        model=OpenAIChat(id="gpt-4o"),
        tools=[DuckDuckGoTools()],
        session_id=session_id,
        storage=PostgresStorage(table_name="agent_sessions", db_url=DATABASE_URL),
        add_history_to_messages=True,
        markdown=True,
        instructions=["Always include sources"],
    )
    return web_agent