# api reference

luna backend api documentation.

**base url:** `http://localhost:8000`

**interactive docs:** `http://localhost:8000/docs` (swagger ui)

## endpoints

### GET /

health check endpoint.

**response:**

```json
{
  "status": "ok",
  "message": "luna agent api",
  "version": "0.1.0"
}
```

### GET /health

detailed health check with service status.

**response:**

```json
{
  "status": "healthy",
  "services": {
    "api": "ok",
    "os": "Darwin",
    "python": "3.11.6",
    "llm": "enabled"
  }
}
```

| field | description |
|-------|-------------|
| `os` | operating system (Darwin, Linux, Windows) |
| `python` | python version |
| `llm` | "enabled" if openai api key is configured, otherwise "disabled (using fallback parser)" |

### POST /api/execute

parse a natural language command into an execution plan.

**request:**

```json
{
  "command": "install chrome",
  "context": {
    "os": "MacIntel",
    "current_dir": "~"
  }
}
```

| field | type | required | description |
|-------|------|----------|-------------|
| `command` | string | yes | natural language command |
| `context` | object | no | optional context about the environment |

**response:**

```json
{
  "task_id": "task_001",
  "steps": [
    {
      "id": 1,
      "description": "check if homebrew is installed",
      "command": "which brew",
      "risk": "safe",
      "status": "pending"
    },
    {
      "id": 2,
      "description": "install google chrome",
      "command": "brew install --cask google-chrome",
      "risk": "moderate",
      "status": "pending"
    },
    {
      "id": 3,
      "description": "verify installation",
      "command": "ls -la /Applications/Google\\ Chrome.app",
      "risk": "safe",
      "status": "pending"
    }
  ],
  "requires_confirmation": true,
  "estimated_time": "2-3 minutes"
}
```

**step object:**

| field | type | description |
|-------|------|-------------|
| `id` | integer | step identifier |
| `description` | string | human-readable description |
| `command` | string | shell command to execute |
| `risk` | string | "safe", "moderate", or "dangerous" |
| `status` | string | "pending", "running", "completed", or "failed" |

**response fields:**

| field | type | description |
|-------|------|-------------|
| `task_id` | string | unique identifier for this task |
| `steps` | array | list of execution steps |
| `requires_confirmation` | boolean | whether to prompt user before executing |
| `estimated_time` | string | estimated execution time |

**error response (500):**

```json
{
  "detail": "error message"
}
```

### POST /api/execute/run

execute all steps of a task.

**request:**

```json
{
  "task_id": "task_001",
  "steps": [
    {
      "id": 1,
      "command": "which brew",
      "description": "check if homebrew is installed"
    },
    {
      "id": 2,
      "command": "brew install --cask google-chrome",
      "description": "install google chrome"
    }
  ]
}
```

| field | type | required | description |
|-------|------|----------|-------------|
| `task_id` | string | yes | task identifier from /api/execute |
| `steps` | array | yes | list of steps to execute |

**response:**

```json
{
  "task_id": "task_001",
  "results": [
    {
      "step_id": 1,
      "status": "completed",
      "output": "/opt/homebrew/bin/brew\n",
      "error": null
    },
    {
      "step_id": 2,
      "status": "completed",
      "output": "==> Downloading https://dl.google.com/...\n==> Installing Cask google-chrome\n",
      "error": null
    }
  ],
  "overall_status": "completed"
}
```

**result object:**

| field | type | description |
|-------|------|-------------|
| `step_id` | integer | step identifier |
| `status` | string | "completed" or "failed" |
| `output` | string | stdout from the command |
| `error` | string or null | stderr if failed, null if succeeded |

**overall_status values:**

| value | meaning |
|-------|---------|
| `completed` | all steps succeeded |
| `partial` | some steps succeeded, execution stopped at failure |
| `failed` | first step failed |

**execution behavior:**

- steps execute sequentially
- execution stops at the first failure
- each step has a 5-minute timeout
- sudo commands trigger macos password dialog if needed

## data types

### ExecuteRequest

```typescript
interface ExecuteRequest {
  command: string;
  context?: {
    os?: string;
    current_dir?: string;
    project_type?: string;
  };
}
```

### ExecuteResponse

```typescript
interface ExecuteResponse {
  task_id: string;
  steps: ExecuteStep[];
  requires_confirmation: boolean;
  estimated_time?: string;
}

interface ExecuteStep {
  id: number;
  description: string;
  command: string;
  risk: "safe" | "moderate" | "dangerous";
  status?: "pending" | "running" | "completed" | "failed";
}
```

### ExecuteAllRequest

```typescript
interface ExecuteAllRequest {
  task_id: string;
  steps: Array<{
    id: number;
    command: string;
    description: string;
  }>;
}
```

### ExecuteAllResponse

```typescript
interface ExecuteAllResponse {
  task_id: string;
  results: StepResult[];
  overall_status: "completed" | "failed" | "partial";
}

interface StepResult {
  step_id: number;
  status: "completed" | "failed";
  output: string;
  error: string | null;
}
```

## risk levels

the backend assigns risk levels to commands:

| level | criteria | examples |
|-------|----------|----------|
| safe | read-only operations | `which`, `ls`, `cat`, `--version`, `git status` |
| moderate | installations, file writes | `brew install`, `npm install`, `pip install` |
| dangerous | sudo, deletions, system changes | `sudo`, `rm`, `chmod`, `systemctl` |

## safety validation

the backend blocks dangerous commands before execution:

**blocked patterns:**
- `rm -rf /` - root filesystem deletion
- `rm -rf ~` - home directory deletion
- `dd if=` - raw disk writes
- `mkfs` - filesystem formatting
- fork bombs
- `nc -e` - potential reverse shells

if a command is blocked, execution returns an error without running the command.

## cors

the backend allows requests from:
- `http://localhost:1420` (tauri dev server)
- `http://tauri.localhost`
- `tauri://localhost`

## examples

### curl: parse a command

```bash
curl -X POST http://localhost:8000/api/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "install chrome"}'
```

### curl: execute steps

```bash
curl -X POST http://localhost:8000/api/execute/run \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "task_001",
    "steps": [
      {"id": 1, "command": "which brew", "description": "check brew"}
    ]
  }'
```

### javascript: full workflow

```javascript
const API = "http://localhost:8000";

// step 1: parse command
const planResponse = await fetch(`${API}/api/execute`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ command: "install chrome" })
});
const plan = await planResponse.json();

// step 2: execute steps
const execResponse = await fetch(`${API}/api/execute/run`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    task_id: plan.task_id,
    steps: plan.steps.map(s => ({
      id: s.id,
      command: s.command,
      description: s.description
    }))
  })
});
const results = await execResponse.json();

console.log(results.overall_status);
```
