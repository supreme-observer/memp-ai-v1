from fastapi import APIRouter
from pydantic import BaseModel
from src.common.dataclass import QueryRequest, QueryResponse

from src.modules.agents.types.wiki_explorer_agent import WikiExplorerAgent


retrival_qa_router = APIRouter(prefix='/agent')

@retrival_qa_router.get("/")
def read_root():
    return {"Hey Whatupp, this is agent task execution system"}

@retrival_qa_router.post("/lookup_from_wikipedia")
def answer_query(query_request: QueryRequest):
    query = query_request.query
    response:QueryResponse = WikiExplorerAgent().lookup_from_wikipedia(query)
    return response
