from fastapi import APIRouter
from pydantic import BaseModel

from src.modules.retrival_qa.retrival_qa_router import RetrivalQA


retrival_qa_router = APIRouter(prefix='/retrival-qa')
@retrival_qa_router.get("/")
def read_root():
    return {"Hey Whatupp, this is a retrival QA system"}

class QueryRequest(BaseModel):
    query: str
class QueryResponse(BaseModel):
    answer: str
    sources: str
# Create an instance of the Bot class


# to be converted to web sockets
@retrival_qa_router.post("/answer")
def answer_query(query_request: QueryRequest):
    query = query_request.query
    response:QueryResponse = RetrivalQA().general_query(query)
    return response

@retrival_qa_router.get("/add-documents")
def create_vector_db():
    response = RetrivalQA().add_documents_to_vector_store()
    return {"message": "data ingested successfully"}
