# setup guide

this guide covers installing and running luna for development.

## prerequisites

### required

| tool | version | check command |
|------|---------|---------------|
| node.js | 18+ | `node --version` |
| npm | 9+ | `npm --version` |
| rust | latest stable | `cargo --version` |
| python | 3.11+ | `python3 --version` |
| homebrew | any | `brew --version` |

### installing prerequisites

**rust:**
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

**node.js (via homebrew):**
```bash
brew install node
```

**python 3.11+ (via homebrew):**
```bash
brew install python@3.11
```

**homebrew (if not installed):**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## installation

### 1. clone the repository

```bash
git clone https://github.com/yourusername/luma-desktop-agent.git
cd luma-desktop-agent
```

### 2. backend setup

```bash
cd src/backend

# create virtual environment
python3 -m venv venv

# activate virtual environment
source venv/bin/activate  # macos/linux
# or: venv\Scripts\activate  # windows

# install dependencies
pip install fastapi uvicorn openai python-dotenv pydantic

# create environment file
cp .env.example .env  # if .env.example exists
# or create manually:
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

**note:** the openai api key is optional. without it, luna falls back to hardcoded command parsing for chrome, vscode, slack, and docker commands.

### 3. frontend setup

```bash
cd ../frontend  # or cd src/frontend from root

# install node dependencies
npm install
```

## running luna

### development mode

**terminal 1 - backend:**
```bash
cd src/backend
source venv/bin/activate
python main.py
```

you should see:
```
🌙 starting luna backend...
📍 api docs: http://127.0.0.1:8000/docs
💻 os: Darwin
🤖 llm: enabled (gpt-4o-mini)  # or "disabled" if no api key
```

**terminal 2 - frontend:**
```bash
cd src/frontend
npm run tauri dev
```

this compiles the rust code and opens the tauri window.

### using the root package.json

from the project root, you can run both with:

```bash
npm run dev  # runs backend and frontend concurrently
```

requires the `concurrently` package (already in devDependencies).

## verifying installation

### backend health check

```bash
curl http://localhost:8000/health
```

expected response:
```json
{
  "status": "healthy",
  "services": {
    "api": "ok",
    "os": "Darwin",
    "python": "3.11.x",
    "llm": "enabled"
  }
}
```

### frontend verification

1. the tauri window should open automatically
2. you should see the luna spotlight interface
3. try typing "which brew" and pressing enter
4. the backend should parse the command and show an execution plan

## configuration

### environment variables

create `src/backend/.env`:

```
OPENAI_API_KEY=sk-...your-key-here
```

| variable | required | description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | no | enables llm-based command parsing. without it, falls back to hardcoded parser. |

### backend configuration

the backend runs on port 8000 by default. to change:

edit `src/backend/main.py`:
```python
uvicorn.run(
    "main:app",
    host="127.0.0.1",
    port=8000,  # change this
    reload=True
)
```

### frontend configuration

the api base url is defined in `src/frontend/src/utils/api.ts`:

```typescript
const API_BASE_URL = "http://localhost:8000";
```

change this if your backend runs on a different port.

## troubleshooting

### backend won't start

**"module not found" error:**
```bash
# make sure venv is activated
source venv/bin/activate

# reinstall dependencies
pip install fastapi uvicorn openai python-dotenv pydantic
```

**port already in use:**
```bash
# find process using port 8000
lsof -i :8000

# kill it
kill -9 <PID>
```

### frontend won't compile

**rust toolchain issues:**
```bash
rustup update stable
rustup default stable
```

**node modules issues:**
```bash
cd src/frontend
rm -rf node_modules package-lock.json
npm install
```

### connection refused

if the frontend shows "connection error":

1. check that backend is running (`python main.py`)
2. verify backend is on port 8000
3. check cors settings in `main.py` allow `http://localhost:1420`

### sudo dialog doesn't appear

the native password dialog uses `osascript`. if it doesn't appear:

1. make sure you're on macos
2. check system preferences > security & privacy > privacy
3. the terminal/app may need accessibility permissions

## development tools

### api documentation

with the backend running, visit:
- http://localhost:8000/docs - swagger ui
- http://localhost:8000/redoc - redoc interface

### hot reload

- **backend:** uvicorn watches for changes automatically
- **frontend:** vite provides hot module replacement

### code formatting

```bash
# python (from src/backend)
pip install black ruff
black .
ruff check .

# typescript (from src/frontend)
npm run format  # if configured
```
