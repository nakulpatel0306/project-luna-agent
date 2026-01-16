"""
luna backend - main entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="luna agent api",
    description="local-first ai agent for development workflows",
    version="0.1.0"
)

# enable cors for tauri frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:1420",  # tauri default dev
        "http://tauri.localhost",
        "tauri://localhost"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """root endpoint - health check"""
    return {
        "status": "ok",
        "message": "luna agent api",
        "version": "0.1.0"
    }


@app.get("/health")
async def health():
    """detailed health check"""
    return {
        "status": "healthy",
        "services": {
            "api": "ok",
            "database": "not implemented",
            "llm": "not implemented"
        }
    }


@app.post("/api/execute")
async def execute_command(command: dict):
    """
    execute a natural language command
    
    example request:
    {
        "command": "install chrome",
        "context": {
            "os": "macos",
            "current_dir": "/Users/user/projects"
        }
    }
    """
    # TODO: implement agent logic
    return {
        "task_id": "placeholder",
        "status": "not implemented",
        "message": "agent logic coming soon"
    }


if __name__ == "__main__":
    print("🌙 starting luna backend...")
    print("📍 api docs: http://127.0.0.1:8000/docs")
    
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
