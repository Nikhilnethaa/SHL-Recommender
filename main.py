from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from vector_db import vector_db
import uvicorn

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
    uvicorn.run(app, host="0.0.0.0", port=8000)
