from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils.rag import rag_pipeline
from utils.logger import setup_logger
import uvicorn

app = FastAPI(
    title="HR Resource Query Chatbot",
    description="AI-powered HR assistant for employee resource allocation",
    version="1.0.0"
)

logger = setup_logger()

class QueryRequest(BaseModel):
    query: str

@app.post("/chat", summary="Process natural language query and return formatted response")
async def chat_query(request: QueryRequest):
    """
    Handles natural language queries and returns employee recommendations.
    Example: {"query": "Find Python developers with 3+ years experience"}
    """
    try:
        response, employees = rag_pipeline(request.query)
        logger.info(f"Processed query: {request.query}")
        return {"response": response, "employees": employees}
    except Exception as e:
        logger.error(f"Error processing query '{request.query}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/employees/search", summary="Search employees by query")
async def search_employees(query: str):
    """
    Searches employees based on query and returns matching profiles.
    Example: /employees/search?query=Python+developers
    """
    try:
        _, employees = rag_pipeline(query)
        logger.info(f"Search query: {query}, found {len(employees)} employees")
        return {"results": employees}
    except Exception as e:
        logger.error(f"Error in search_employees: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/health", summary="Health check endpoint")
async def health_check():
    """Returns status of the API."""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
