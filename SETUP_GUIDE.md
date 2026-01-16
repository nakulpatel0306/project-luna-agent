# 🚀 luna setup guide - step by step

this guide will walk you through setting up luna for development from scratch.

---

## prerequisites checklist

before starting, make sure you have:

- [ ] **node.js 18+** - `node --version`
- [ ] **npm 9+** - `npm --version`
- [ ] **rust + cargo** - `cargo --version`
- [ ] **python 3.11+** - `python3 --version`
- [ ] **git** - `git --version`

### installing prerequisites

**if you don't have rust:**
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

**if you don't have node:**
```bash
# on mac with homebrew
brew install node

# or download from nodejs.org
```

**if you don't have python 3.11+:**
```bash
# on mac with homebrew
brew install python@3.11
```

---

## step 1: initial project setup

### 1.1 navigate to project directory
```bash
cd '/Users/nakulpatel/Desktop/career/github projects/luma-desktop-agent'
```

### 1.2 copy setup files
you should have these files in your project root:
- `setup_project_structure.sh` - creates folder structure
- `.gitignore` - ignores unnecessary files
- `README.md` - project overview
- `package.json` - root package file
- `project_luna_notion_structure.md` - detailed specs

### 1.3 initialize git
```bash
git init
git branch -M main
```

### 1.4 create directory structure
```bash
chmod +x setup_project_structure.sh
./setup_project_structure.sh
```

### 1.5 initial commit
```bash
git add .
git commit -m "initial commit: project structure"
```

---

## step 2: frontend setup (tauri + react)

### 2.1 navigate to frontend directory
```bash
cd src/frontend
```

### 2.2 initialize tauri project
```bash
# create tauri app with react template
npm create tauri-app@latest . -- --manager npm

# when prompted:
# - app name: luma
# - identifier: com.luma.agent
# - frontend template: react-ts
# - package manager: npm
```

### 2.3 install dependencies
```bash
npm install
```

### 2.4 install additional packages
```bash
# ui and styling
npm install tailwindcss postcss autoprefixer
npm install @tailwindcss/forms @tailwindcss/typography
npm install clsx tailwind-merge

# state management
npm install zustand

# icons
npm install lucide-react

# utilities
npm install date-fns

# development
npm install -D @types/node
npm install -D prettier prettier-plugin-tailwindcss
```

### 2.5 initialize tailwind
```bash
npx tailwindcss init -p
```

### 2.6 test frontend
```bash
npm run tauri dev
```

you should see a window open with the default tauri app!

---

## step 3: backend setup (python)

### 3.1 navigate to backend directory
```bash
cd ../../src/backend
# or from root: cd src/backend
```

### 3.2 create virtual environment
```bash
python3 -m venv venv
```

### 3.3 activate virtual environment
```bash
# on mac/linux
source venv/bin/activate

# on windows
venv\Scripts\activate
```

you should see `(venv)` in your terminal prompt

### 3.4 create requirements.txt
create a file `src/backend/requirements.txt`:
```txt
# web framework
fastapi==0.108.0
uvicorn[standard]==0.25.0

# llm and ai
openai==1.6.1
anthropic==0.8.1
langchain==0.1.0
langchain-openai==0.0.2

# local llm (optional)
ollama==0.0.9

# database
sqlalchemy==2.0.23
alembic==1.13.1

# utilities
pydantic==2.5.3
python-dotenv==1.0.0
httpx==0.26.0
psutil==5.9.7

# testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0

# code quality
black==23.12.1
ruff==0.1.9
mypy==1.7.1
```

### 3.5 install dependencies
```bash
pip install -r requirements.txt
```

### 3.6 create initial backend structure
```bash
# from backend directory
touch main.py
touch __init__.py
touch agent/__init__.py
touch api/__init__.py
```

### 3.7 create basic main.py
create `src/backend/main.py`:
```python
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
    allow_origins=["http://localhost:1420"],  # tauri default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ok", "message": "luna agent api"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
```

### 3.8 test backend
```bash
python main.py
```

visit http://localhost:8000 - you should see `{"status": "ok", "message": "luna agent api"}`

---

## step 4: cursor setup

### 4.1 open in cursor
```bash
# from project root
cursor .
# or just open cursor and select your project folder
```

### 4.2 configure cursor settings

create `.vscode/settings.json` (cursor uses vscode settings):
```json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll": true,
    "source.organizeImports": true
  },
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter"
  },
  "[rust]": {
    "editor.defaultFormatter": "rust-lang.rust-analyzer"
  },
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "black",
  "rust-analyzer.checkOnSave.command": "clippy",
  "tailwindCSS.experimental.classRegex": [
    ["clsx\\(([^)]*)\\)", "(?:'|\"|`)([^']*)(?:'|\"|`)"]
  ]
}
```

### 4.3 recommended cursor extensions
- rust-analyzer
- tauri
- prettier
- tailwind css intellisense
- python
- black formatter
- ruff

---

## step 5: github setup

### 5.1 create github repository
1. go to github.com
2. click "new repository"
3. name: `luma-desktop-agent`
4. description: "local-first ai agent for development workflows"
5. **do not** initialize with readme (you already have one)
6. create repository

### 5.2 connect local to remote
```bash
# from project root
git remote add origin https://github.com/yourusername/luma-desktop-agent.git
git push -u origin main
```

replace `yourusername` with your github username

---

## step 6: verify everything works

### 6.1 run backend
```bash
# terminal 1
cd src/backend
source venv/bin/activate
python main.py
```

you should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 6.2 run frontend
```bash
# terminal 2
cd src/frontend
npm run tauri dev
```

you should see the tauri app window open

### 6.3 test ipc (future)
we'll set up communication between frontend and backend in the next steps

---

## step 7: development workflow

### 7.1 starting development
```bash
# from project root
npm run dev
```

this runs both frontend and backend concurrently

### 7.2 making changes

**for frontend:**
- edit files in `src/frontend/src/`
- hot reload should work automatically

**for backend:**
- edit files in `src/backend/`
- uvicorn hot reload should restart automatically

### 7.3 committing changes
```bash
# check what changed
git status

# stage changes
git add .

# commit with descriptive message
git commit -m "feat: add basic agent endpoint"

# push to github
git push
```

---

## step 8: cursor ai features

### 8.1 using cursor chat
- press `cmd+l` (mac) or `ctrl+l` (windows/linux)
- ask questions about your code
- examples:
  - "how do i add a new api endpoint?"
  - "explain this rust function"
  - "write a test for this component"

### 8.2 using cursor composer
- press `cmd+i` (mac) or `ctrl+i` (windows/linux)
- make inline edits with ai
- examples:
  - "add error handling to this function"
  - "make this component responsive"
  - "refactor this to use typescript"

### 8.3 cursor rules
create `.cursorrules` in project root:
```
this is the luna desktop agent project.

code style:
- use lowercase for all ui text
- prefer functional components in react
- use type hints in python
- write clear, self-documenting code
- add comments for complex logic

architecture:
- frontend: tauri + react + typescript
- backend: python + fastapi
- communication: ipc/http
- local-first philosophy

when writing code:
- follow the project structure in README.md
- reference project_luna_notion_structure.md for specs
- write tests for new features
- keep functions small and focused
```

---

## troubleshooting

### rust installation issues
```bash
# update rust
rustup update stable

# add cargo to path
source $HOME/.cargo/env
```

### python version issues
```bash
# check version
python3 --version

# if wrong version, use specific version
python3.11 -m venv venv
```

### tauri dev not working
```bash
# clear cache and reinstall
cd src/frontend
rm -rf node_modules
rm package-lock.json
npm install
```

### port already in use
```bash
# find process using port 8000
lsof -i :8000

# kill process
kill -9 <PID>
```

---

## next steps

now you're ready to start coding! here's what to build next:

1. **spotlight ui component** (frontend)
   - create input component
   - add hotkey listener
   - style with tailwind

2. **basic agent endpoint** (backend)
   - parse natural language input
   - return structured response
   - test with curl

3. **ipc setup** (frontend ↔ rust ↔ backend)
   - tauri commands in rust
   - fetch from react to backend
   - display results

4. **first feature: "install chrome"**
   - detect os
   - generate install command
   - execute safely
   - show progress

follow the detailed specs in `project_luna_notion_structure.md` for implementation details.

---

**you're all set! start coding in cursor and build something awesome.** 🌙
