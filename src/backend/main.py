"""
luna backend - main entry point
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Literal, Dict, Any
import uvicorn
import platform
from utils.executor import execute_command as run_command, check_tool_installed

app = FastAPI(
    title="luna agent api",
    description="local-first ai agent for development workflows",
    version="0.1.0"
)

# enable cors for tauri frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:1420",
        "http://tauri.localhost",
        "tauri://localhost"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ExecuteStep(BaseModel):
    id: int
    description: str
    command: str
    risk: Literal["safe", "moderate", "dangerous"]
    status: Optional[Literal["pending", "running", "completed", "failed"]] = "pending"


class ExecuteRequest(BaseModel):
    command: str
    context: Optional[dict] = None


class ExecuteResponse(BaseModel):
    task_id: str
    steps: List[ExecuteStep]
    requires_confirmation: bool
    estimated_time: Optional[str] = None


class ExecuteAllRequest(BaseModel):
    task_id: str
    steps: List[Dict[str, Any]]


class StepResult(BaseModel):
    step_id: int
    status: Literal["completed", "failed"]
    output: str
    error: Optional[str] = None


class ExecuteAllResponse(BaseModel):
    task_id: str
    results: List[StepResult]
    overall_status: Literal["completed", "failed", "partial"]


def parse_command(command: str) -> ExecuteResponse:
    """
    basic command parser - will be replaced with llm later
    """
    command_lower = command.lower().strip()
    os_type = platform.system().lower()
    
    # detect "install chrome" command
    if "install" in command_lower and "chrome" in command_lower:
        if os_type == "darwin":  # macOS
            return ExecuteResponse(
                task_id="task_001",
                steps=[
                    ExecuteStep(
                        id=1,
                        description="check if homebrew is installed",
                        command="which brew",
                        risk="safe"
                    ),
                    ExecuteStep(
                        id=2,
                        description="install google chrome",
                        command="brew install --cask google-chrome",
                        risk="moderate"
                    ),
                    ExecuteStep(
                        id=3,
                        description="verify installation",
                        command="ls -la /Applications/Google\\ Chrome.app",
                        risk="safe"
                    )
                ],
                requires_confirmation=True,
                estimated_time="2-3 minutes"
            )
        elif os_type == "linux":
            return ExecuteResponse(
                task_id="task_001",
                steps=[
                    ExecuteStep(
                        id=1,
                        description="download google chrome",
                        command="wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb",
                        risk="safe"
                    ),
                    ExecuteStep(
                        id=2,
                        description="install google chrome",
                        command="sudo dpkg -i google-chrome-stable_current_amd64.deb",
                        risk="dangerous"
                    ),
                    ExecuteStep(
                        id=3,
                        description="fix dependencies",
                        command="sudo apt-get install -f -y",
                        risk="moderate"
                    )
                ],
                requires_confirmation=True,
                estimated_time="3-5 minutes"
            )
        elif os_type == "windows":
            return ExecuteResponse(
                task_id="task_001",
                steps=[
                    ExecuteStep(
                        id=1,
                        description="check if chocolatey is installed",
                        command="choco --version",
                        risk="safe"
                    ),
                    ExecuteStep(
                        id=2,
                        description="install google chrome",
                        command="choco install googlechrome -y",
                        risk="moderate"
                    )
                ],
                requires_confirmation=True,
                estimated_time="2-3 minutes"
            )
    
    # detect "install vscode" command
    elif "install" in command_lower and ("vscode" in command_lower or "visual studio code" in command_lower):
        if os_type == "darwin":
            return ExecuteResponse(
                task_id="task_002",
                steps=[
                    ExecuteStep(
                        id=1,
                        description="check if homebrew is installed",
                        command="which brew",
                        risk="safe"
                    ),
                    ExecuteStep(
                        id=2,
                        description="install visual studio code",
                        command="brew install --cask visual-studio-code",
                        risk="moderate"
                    ),
                    ExecuteStep(
                        id=3,
                        description="verify installation",
                        command="ls -la /Applications/Visual\\ Studio\\ Code.app",
                        risk="safe"
                    )
                ],
                requires_confirmation=True,
                estimated_time="2-3 minutes"
            )
        elif os_type == "linux":
            return ExecuteResponse(
                task_id="task_002",
                steps=[
                    ExecuteStep(
                        id=1,
                        description="add microsoft repository",
                        command="wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg",
                        risk="moderate"
                    ),
                    ExecuteStep(
                        id=2,
                        description="install vscode",
                        command="sudo apt-get install code",
                        risk="moderate"
                    )
                ],
                requires_confirmation=True,
                estimated_time="3-5 minutes"
            )
    
    # detect "check docker" command
    elif "check" in command_lower and "docker" in command_lower:
        return ExecuteResponse(
            task_id="task_003",
            steps=[
                ExecuteStep(
                    id=1,
                    description="check if docker is installed",
                    command="docker --version",
                    risk="safe"
                ),
                ExecuteStep(
                    id=2,
                    description="check if docker daemon is running",
                    command="docker ps",
                    risk="safe"
                ),
                ExecuteStep(
                    id=3,
                    description="show docker info",
                    command="docker info",
                    risk="safe"
                )
            ],
            requires_confirmation=False,
            estimated_time="5 seconds"
        )
        
    # detect "install slack" command
    elif "install" in command_lower and "slack" in command_lower:
        if os_type == "darwin":
            return ExecuteResponse(
                task_id="task_slack",
                steps=[
                    ExecuteStep(
                        id=1,
                        description="check if homebrew is installed",
                        command="which brew",
                        risk="safe"
                    ),
                    ExecuteStep(
                        id=2,
                        description="install slack",
                        command="brew install --cask slack",
                        risk="moderate"
                    ),
                    ExecuteStep(
                        id=3,
                        description="verify installation",
                        command="ls -la /Applications/Slack.app",
                        risk="safe"
                    )
                ],
                requires_confirmation=True,
                estimated_time="2-3 minutes"
            )
        elif os_type == "linux":
            return ExecuteResponse(
                task_id="task_slack",
                steps=[
                    ExecuteStep(
                        id=1,
                        description="install slack via snap",
                        command="sudo snap install slack --classic",
                        risk="moderate"
                    )
                ],
                requires_confirmation=True,
                estimated_time="2-3 minutes"
            )
    
    # detect "which brew" or similar check commands
    elif "which" in command_lower or "where" in command_lower:
        tool = command_lower.split()[-1] if len(command_lower.split()) > 1 else "unknown"
        return ExecuteResponse(
            task_id="task_check",
            steps=[
                ExecuteStep(
                    id=1,
                    description=f"check if {tool} is installed",
                    command=command,
                    risk="safe"
                )
            ],
            requires_confirmation=False,
            estimated_time="1 second"
        )
    
    # default: command not recognized
    return ExecuteResponse(
        task_id="task_unknown",
        steps=[
            ExecuteStep(
                id=1,
                description=f"command not recognized: {command}",
                command="echo 'unknown command'",
                risk="safe",
                status="failed"
            )
        ],
        requires_confirmation=False,
        estimated_time="0 seconds"
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
            "os": platform.system(),
            "python": platform.python_version()
        }
    }


@app.post("/api/execute", response_model=ExecuteResponse)
async def execute_command_endpoint(request: ExecuteRequest):
    """
    parse and plan command execution
    """
    try:
        response = parse_command(request.command)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/execute/run", response_model=ExecuteAllResponse)
async def execute_all_steps(request: ExecuteAllRequest):
    """
    execute all steps of a task
    """
    results = []
    overall_success = True
    
    for step in request.steps:
        command = step.get("command")
        step_id = step.get("id")
        
        print(f"🔄 executing step {step_id}: {command}")
        
        # execute the command
        success, stdout, stderr = run_command(command, timeout=300)
        
        print(f"{'✅' if success else '❌'} step {step_id}: {'completed' if success else 'failed'}")
        if stdout:
            print(f"   stdout: {stdout[:100]}...")
        if stderr:
            print(f"   stderr: {stderr[:100]}...")
        
        results.append(
            StepResult(
                step_id=step_id,
                status="completed" if success else "failed",
                output=stdout,
                error=stderr if not success else None
            )
        )
        
        # stop on first failure
        if not success:
            overall_success = False
            break
    
    # determine overall status
    if overall_success:
        overall_status = "completed"
    elif len(results) == 0:
        overall_status = "failed"
    elif len(results) < len(request.steps):
        overall_status = "partial"
    else:
        overall_status = "failed"
    
    return ExecuteAllResponse(
        task_id=request.task_id,
        results=results,
        overall_status=overall_status
    )


if __name__ == "__main__":
    print("🌙 starting luna backend...")
    print("📍 api docs: http://127.0.0.1:8000/docs")
    print(f"💻 os: {platform.system()}")
    
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_excludes=["venv/*", "*.pyc", "__pycache__", ".pytest_cache"]
    )