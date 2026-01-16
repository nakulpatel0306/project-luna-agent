# project luna desktop agent

> democratize complex development workflows through natural language

a spotlight-style ai agent that runs locally on your machine, making development setup and system administration accessible to everyone.

## what is luna?

luna is a desktop ai agent that:
- activates with a global hotkey (like spotlight)
- understands natural language commands
- executes complex tasks safely on your machine
- works across mac, windows, and linux
- keeps everything local-first for privacy

### examples

```
"install chrome and vscode"
"setup python environment with django"
"check why docker isn't running"
"create a react project with typescript"
```

## status

🚧 **under active development** - currently in phase 0 (foundation)

- [x] project structure
- [ ] tauri frontend setup
- [ ] python backend initialization
- [ ] basic agent engine
- [ ] spotlight ui
- [ ] package manager integration

## architecture

```
┌─────────────────────────────┐
│   tauri app (rust + react)  │
│   - spotlight ui            │
│   - safe execution layer    │
└──────────┬──────────────────┘
           │
           ↓ ipc/http
┌──────────────────────────────┐
│   python backend             │
│   - agent logic              │
│   - llm integration          │
│   - knowledge graph          │
└──────────────────────────────┘
```

## tech stack

**frontend**
- tauri (rust + typescript)
- react 18
- tailwind css
- zustand (state)

**backend**
- python 3.11+
- fastapi
- ollama (local llm)
- sqlite

## prerequisites

- node.js 18+
- rust / cargo
- python 3.11+
- ollama (optional, for local llm)

## getting started

### 1. clone and setup

```bash
cd luma-desktop-agent

# run setup script
chmod +x setup_project_structure.sh
./setup_project_structure.sh
```

### 2. frontend setup

```bash
cd src/frontend

# initialize tauri
npm create tauri-app@latest . -- --manager npm

# install dependencies
npm install
```

### 3. backend setup

```bash
cd src/backend

# create virtual environment
python3 -m venv venv
source venv/bin/activate  # on windows: venv\Scripts\activate

# install dependencies (coming soon)
pip install -r requirements.txt
```

### 4. run development

```bash
# terminal 1 - backend
cd src/backend
source venv/bin/activate
python main.py

# terminal 2 - frontend
cd src/frontend
npm run tauri dev
```

## project structure

```
luma-desktop-agent/
├── src/
│   ├── frontend/        # tauri + react app
│   │   ├── src/
│   │   │   ├── components/
│   │   │   ├── hooks/
│   │   │   └── utils/
│   │   └── src-tauri/   # rust backend
│   ├── backend/         # python agent
│   │   ├── agent/       # core agent logic
│   │   ├── api/         # fastapi server
│   │   ├── integrations/# package managers, etc
│   │   └── knowledge/   # context system
│   └── shared/          # shared types/models
├── docs/                # documentation
├── tests/               # test suite
└── config/              # configuration files
```

## contributing

contributions welcome! this project is in early stages.

### development workflow

1. create a branch for your feature
2. make changes with descriptive commits
3. test thoroughly (all platforms if possible)
4. submit pr with clear description

### code style

- **lowercase aesthetic** - all ui text lowercase
- **type safe** - typescript for frontend, type hints for python
- **tested** - unit tests for core functionality
- **documented** - clear comments and docs

## roadmap

**phase 0: foundation** (weeks 1-2)
- [x] project structure
- [ ] tauri initialization
- [ ] python backend boilerplate
- [ ] basic ipc communication

**phase 1: mvp** (weeks 3-6)
- [ ] spotlight ui
- [ ] basic agent (install commands)
- [ ] package manager integration
- [ ] safety validation

**phase 2: intelligence** (weeks 7-10)
- [ ] context awareness
- [ ] task decomposition
- [ ] learning system
- [ ] command history

**phase 3: advanced** (weeks 11-14)
- [ ] vscode extension
- [ ] git integration
- [ ] docker management
- [ ] cloud sync (optional)

see [project_luna_notion_structure.md](./project_luna_notion_structure.md) for detailed specs.

## license

mit (to be finalized)

## contact

- project lead: nakul patel
- issues: [github issues](https://github.com/yourusername/luma-desktop-agent/issues)
- discussions: [github discussions](https://github.com/yourusername/luma-desktop-agent/discussions)

---

built with ❤️ for developers who hate repetitive setup tasks
