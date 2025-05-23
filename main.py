import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from vector_db import vector_db
import uvicorn
from fastapi.responses import FileResponse

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    text: str

@app.get("/")
def serve_index():
    index_path = os.path.join(os.path.dirname(__file__), "index.html")
    return FileResponse(index_path)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/recommend")
def recommend(query: Query):
    results = vector_db.search(query.text)
    return {
        "recommendations": [
            {
                "name": r.get("name", "Unknown"),
                "url": r.get("url", "Unknown URL"),
                "remote_testing": "Yes" if r.get("remote_testing") else "No",
                "adaptive_irt": "Yes" if r.get("adaptive") else "No",
                "duration": r.get("duration", "Unknown"),
                "test_type": r.get("test_type", "Unknown")
            }
            for r in results[:10]  # Return max 10 results
        ]
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Use the port from the environment variable
    uvicorn.run(app, host="0.0.0.0", port=port)
