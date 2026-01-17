# architecture

luna is a desktop application with a tauri/react frontend and a python backend. the two communicate over http.

## system overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        tauri desktop app                        │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    react frontend                         │  │
│  │  ┌─────────────┐    ┌─────────────┐    ┌──────────────┐   │  │
│  │  │  Spotlight  │───▶│   api.ts    │───▶│   display    │   │  │
│  │  │   input     │    │   client    │    │   results    │   │  │
│  │  └─────────────┘    └─────────────┘    └──────────────┘   │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ http (localhost:8000)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       python backend                            │
│  ┌─────────────┐    ┌─────────────┐    ┌──────────────────┐    │
│  │   fastapi   │───▶│  llm parser │───▶│    executor      │    │
│  │   routes    │    │  (openai)   │    │  (subprocess)    │    │
│  └─────────────┘    └─────────────┘    └──────────────────┘    │
│                              │                    │             │
│                              ▼                    ▼             │
│                     ┌─────────────┐    ┌──────────────────┐    │
│                     │  hardcoded  │    │   sudo handler   │    │
│                     │  fallback   │    │   (osascript)    │    │
│                     └─────────────┘    └──────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## components

### frontend (src/frontend/)

**technology:** tauri 2.0, react 18, typescript, tailwind css

**key files:**

| file | purpose |
|------|---------|
| `src/components/Spotlight.tsx` | main ui component - input, plan display, execution status |
| `src/utils/api.ts` | http client for backend communication |
| `src/App.tsx` | root component |
| `src/App.css` | tailwind configuration and custom styles |

**data flow:**

1. user types command in spotlight input
2. `executeCommand()` sends POST to `/api/execute`
3. response contains execution plan (steps with commands and risk levels)
4. user reviews plan and clicks "execute"
5. `executeAllSteps()` sends POST to `/api/execute/run`
6. ui updates status for each step as results arrive

### backend (src/backend/)

**technology:** python 3.11+, fastapi, uvicorn, openai

**key files:**

| file | purpose |
|------|---------|
| `main.py` | fastapi app, routes, command parsing logic |
| `utils/executor.py` | command execution, sudo handling, safety validation |

**command parsing:**

the backend uses a two-tier parsing strategy:

1. **llm parsing (primary)** - sends command to gpt-4o-mini with system prompt
   - detects os and available package managers
   - generates appropriate shell commands
   - assigns risk levels
   - returns structured json

2. **hardcoded fallback** - if no api key or llm fails
   - supports: install chrome, install vscode, install slack, check docker
   - pattern matching on command string

**execution:**

commands run via `subprocess.run()` with:
- 5 minute default timeout
- shell mode via `/bin/bash`
- environment variables for non-interactive mode
- safety validation before execution

### sudo handling (macos)

luna uses a seamless sudo approach that avoids terminal password prompts:

```
┌────────────────────────────────────────────────────┐
│  command needs sudo?                               │
│         │                                          │
│         ▼                                          │
│  ┌─────────────────┐                               │
│  │ check cached    │ ───yes──▶ execute directly   │
│  │ credentials     │                               │
│  └─────────────────┘                               │
│         │ no                                       │
│         ▼                                          │
│  ┌─────────────────┐                               │
│  │ osascript:      │                               │
│  │ "do shell       │ ◀──── native macos           │
│  │ script with     │       password dialog         │
│  │ administrator   │                               │
│  │ privileges"     │                               │
│  └─────────────────┘                               │
│         │                                          │
│         ▼                                          │
│  credentials cached (~5 min)                       │
└────────────────────────────────────────────────────┘
```

key points:
- uses `osascript` to trigger macos native password dialog
- credentials cached for ~5 minutes (macos default)
- subsequent sudo commands use cached credentials automatically
- no terminal interaction required

### safety validation

commands are validated before execution:

**blocked patterns:**
- `rm -rf /` - filesystem destruction
- `dd if=` - direct disk writes
- `mkfs` - filesystem formatting
- fork bombs
- reverse shells

**risk levels:**
- `safe` - read-only operations (ls, cat, which, version checks)
- `moderate` - installations, file writes
- `dangerous` - sudo, deletions, system modifications

## data models

### ExecuteResponse

```json
{
  "task_id": "task_001",
  "steps": [
    {
      "id": 1,
      "description": "check if homebrew is installed",
      "command": "which brew",
      "risk": "safe"
    },
    {
      "id": 2,
      "description": "install google chrome",
      "command": "brew install --cask google-chrome",
      "risk": "moderate"
    }
  ],
  "requires_confirmation": true,
  "estimated_time": "2-3 minutes"
}
```

### ExecuteAllResponse

```json
{
  "task_id": "task_001",
  "results": [
    {
      "step_id": 1,
      "status": "completed",
      "output": "/opt/homebrew/bin/brew",
      "error": null
    },
    {
      "step_id": 2,
      "status": "completed",
      "output": "==> Installing Cask google-chrome...",
      "error": null
    }
  ],
  "overall_status": "completed"
}
```

## llm integration

the system prompt instructs gpt-4o-mini to:

1. generate atomic, directly-executable shell commands
2. use correct package manager for detected os
3. assign appropriate risk levels
4. add verification steps when useful
5. avoid interactive flags (-i, --interactive)
6. use -y or equivalent for package managers

**context provided to llm:**
- operating system (darwin/linux/windows)
- available package managers (brew, apt, npm, pip, etc.)
- sudo handling note (native dialog, no terminal prompts)

## future considerations

areas not yet implemented:

- global hotkey activation (app must be focused)
- windows/linux sudo handling
- persistent command history
- context awareness (project detection)
- task decomposition (breaking complex tasks into subtasks)
- learning from user corrections
