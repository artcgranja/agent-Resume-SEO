import os
from agno.team import Team
from app.agents.seo_resume_agent import create_seo_agent
from app.agents.evaluate_resume_agent import create_evaluate_resume_agent
from agno.models.openai import OpenAIChat
from agno.storage.postgres import PostgresStorage
from app.agents.web_agent import create_web_agent
from agno.media import File

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://resume:resume@localhost:5452/resume_db")

class Orchestrator:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.storage = PostgresStorage(table_name="team_sessions", db_url=DATABASE_URL)
        self.team = Team(
            members=[
                create_seo_agent(session_id),
                create_evaluate_resume_agent(session_id),
                create_web_agent(session_id),
            ],
            mode="collaborate",
            session_id=self.session_id,
            model=OpenAIChat(id="gpt-4o"),
            add_datetime_to_instructions=True,
            enable_agentic_context=True,
            share_member_interactions=True,
            show_members_responses=True,
            storage=self.storage,
            markdown=True,
            add_history_to_messages=True,
        )

    def run(self, input_: str):
        return self.team.print_response(input_)
    
    def run_with_files(self, input_: str, files: list):
        agno_files = []
        for file_dict in files:
            file_obj = File(
                content=file_dict['content'],
                name=file_dict['name'],
                mime_type=file_dict.get('mime_type')
            )
            agno_files.append(file_obj)
        
        return self.team.print_response(input_, files=agno_files)