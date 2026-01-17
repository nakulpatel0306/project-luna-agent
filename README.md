# luna

a local-first ai agent for development workflows. type natural language commands and luna executes them safely on your machine.

## what it does

luna is a desktop app that lets you run development tasks using plain english:

```
"install chrome"
"install vscode"
"install slack"
"check docker status"
```

it parses your request, shows you the execution plan with risk levels, and runs the commands after confirmation.

## current status

**working features:**

- spotlight-style ui for entering commands
- command parsing via openai gpt-4o-mini (with hardcoded fallback)
- execution plan display with step-by-step breakdown
- risk level indicators (safe / moderate / dangerous)
- real command execution via subprocess
- seamless sudo handling via macos native password dialog
- output and error display per step
- command safety validation (blocks destructive patterns)

**supported commands (hardcoded fallback):**

- `install chrome` - installs via homebrew
- `install vscode` - installs via homebrew
- `install slack` - installs via homebrew
- `check docker status` - checks docker installation and status
- `which <tool>` - checks if a tool is installed

with an openai api key configured, any natural language command is supported.

## tech stack

| layer | technology |
|-------|------------|
| desktop runtime | tauri 2.0 (rust) |
| frontend | react 18, typescript |
| styling | tailwind css |
| icons | lucide-react |
| backend | python 3.11+, fastapi |
| llm | openai gpt-4o-mini |

## prerequisites

- node.js 18+
- rust / cargo
- python 3.11+
- homebrew (for macos package installations)

## quick start

### 1. backend setup

```bash
cd src/backend

# create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # windows: venv\Scripts\activate

# install dependencies
pip install fastapi uvicorn openai python-dotenv pydantic

# create .env file
echo "OPENAI_API_KEY=your_key_here" > .env

# run backend
python main.py
```

the api runs at http://127.0.0.1:8000

### 2. frontend setup

```bash
cd src/frontend

# install dependencies
npm install

# run development server
npm run tauri dev
```

### 3. use luna

1. type a command like "install chrome"
2. review the execution plan
3. click "execute" to run the steps
4. view output/errors for each step

## project structure

```
luma-desktop-agent/
├── src/
│   ├── frontend/           # tauri + react app
│   │   ├── src/
│   │   │   ├── components/
│   │   │   │   └── Spotlight.tsx   # main ui component
│   │   │   ├── utils/
│   │   │   │   └── api.ts          # backend api client
│   │   │   ├── App.tsx
│   │   │   └── main.tsx
│   │   └── src-tauri/      # rust backend for tauri
│   └── backend/            # python api server
│       ├── main.py         # fastapi app + command parsing
│       └── utils/
│           └── executor.py # command execution + sudo handling
├── docs/                   # documentation
└── package.json            # root workspace config
```

## documentation

- [architecture](docs/ARCHITECTURE.md) - technical design and data flow
- [setup guide](docs/SETUP.md) - detailed installation instructions
- [usage guide](docs/USAGE.md) - how to use luna
- [api reference](docs/API.md) - backend api documentation

## how it works

1. **user input** - you type a natural language command in the spotlight ui
2. **parsing** - backend sends your command to gpt-4o-mini (or uses hardcoded parser)
3. **plan generation** - llm returns structured steps with commands and risk levels
4. **confirmation** - ui displays the plan for your approval
5. **execution** - steps run sequentially with real-time status updates
6. **sudo handling** - if needed, macos shows native password dialog (credentials cached for ~5 min)

## limitations

- macos only (sudo handling uses osascript)
- requires homebrew for package installations
- llm features require openai api key
- no global hotkey yet (app must be focused)

## license

mit

## author

nakul patel
