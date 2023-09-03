from fastapi import APIRouter
from pydantic import BaseModel

from src.modules.bot.bot import Cortex


bot_router = APIRouter(prefix='/bot')
@bot_router.get("/")
def read_root():
    return {"Hello": "World"}

class QueryRequest(BaseModel):
    query: str
class QueryResponse(BaseModel):
    answer: str
    sources: str
# Create an instance of the Bot class


# to be converted to web sockets
@bot_router.post("/answer")
def answer_query(query_request: QueryRequest):
    query = query_request.query
    response:QueryResponse = Cortex().ask(query)
    return response

@bot_router.get("/add-documents")
def create_vector_db():
    response = Cortex().add_documents_to_vector_store()
    return {"message": "data ingested successfully"}
