from ingest import ingest
from pydantic import BaseModel
from fastapi import FastAPI
from bot import Bot


app = FastAPI()
bot = Bot()  # Create an instance of the Bot class

@app.get("/")
def read_root():
    return {"Hello": "World"}

class QueryRequest(BaseModel):
    query: str


# to be converted to web sockets
@app.post("/answer")
def answer_query(query_request: QueryRequest):
    query = query_request.query
    response = bot.answer(query)
    return {"query": query, "response": response}

@app.get("/ingest")
def create_vector_db():
    ingest()
    return {"message": "data ingested successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
