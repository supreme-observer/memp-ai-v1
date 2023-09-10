from fastapi import FastAPI

app = FastAPI()

# Import and register blueprints/modules
from src.modules.retrival_qa.retrival_qa_router import retrival_qa_router
from src.modules.agents.agent_router import agent_router

app.include_router(retrival_qa_router)
app.include_router(agent_router)