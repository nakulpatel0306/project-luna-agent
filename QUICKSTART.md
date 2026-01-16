# 🚀 quickstart - after unzipping

you've downloaded the luma-desktop-agent starter files. here's what to do next:

---

## step 1: move files to your project directory

```bash
# your project is at:
cd '/Users/nakulpatel/Desktop/career/github projects/luma-desktop-agent'

# copy all files from the unzipped folder to your project directory
# make sure to include hidden files (.gitignore, .cursorrules, etc)
```

**important:** copy ALL files including:
- hidden files (start with `.`)
- all folders (`src/`, `docs/`, `tests/`, etc)
- markdown files
- shell scripts

---

## step 2: make setup script executable

```bash
chmod +x setup_project_structure.sh
```

---

## step 3: initialize git

```bash
git init
git branch -M main
git add .
git commit -m "initial commit: project structure and setup files"
```

---

## step 4: install prerequisites (if not already installed)

### check what you have:
```bash
node --version    # need 18+
npm --version     # need 9+
cargo --version   # need rust
python3 --version # need 3.11+
```

### install what's missing:

**rust:**
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

**node (if needed):**
```bash
brew install node
```

**python 3.11+ (if needed):**
```bash
brew install python@3.11
```

---

## step 5: setup backend

```bash
cd src/backend

# create virtual environment
python3 -m venv venv

# activate it
source venv/bin/activate

# install dependencies
pip install -r requirements.txt

# copy environment file
cp .env.example .env
```

---

## step 6: setup frontend

```bash
cd ../../src/frontend  # from backend, go back up and into frontend

# initialize tauri with react-ts template
npm create tauri-app@latest . -- --manager npm

# when prompted, choose:
# - app name: luma
# - identifier: com.luma.agent  
# - frontend template: react-ts
# - package manager: npm
```

---

## step 7: install frontend dependencies

```bash
# core dependencies
npm install

# additional packages
npm install tailwindcss postcss autoprefixer
npm install @tailwindcss/forms @tailwindcss/typography
npm install clsx tailwind-merge zustand lucide-react date-fns

# dev dependencies
npm install -D @types/node prettier prettier-plugin-tailwindcss
```

---

## step 8: initialize tailwind

```bash
npx tailwindcss init -p
```

update `tailwind.config.js`:
```js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
```

---

## step 9: test backend

```bash
# in terminal 1
cd src/backend
source venv/bin/activate
python main.py
```

visit http://localhost:8000 - you should see:
```json
{"status": "ok", "message": "luna agent api", "version": "0.1.0"}
```

---

## step 10: test frontend

```bash
# in terminal 2  
cd src/frontend
npm run tauri dev
```

a window should open with the default tauri app!

---

## step 11: open in cursor

```bash
# from project root
cursor .
```

cursor will:
- detect the project
- suggest installing recommended extensions
- load your .cursorrules
- be ready for development

---

## step 12: setup github

### create repo on github:
1. go to github.com/new
2. name: `luma-desktop-agent`
3. **don't** initialize with readme
4. create repository

### connect local to remote:
```bash
# from project root
git remote add origin https://github.com/YOUR_USERNAME/luma-desktop-agent.git
git push -u origin main
```

---

## you're ready! 🎉

### development workflow:

**run both servers:**
```bash
# from project root
npm run dev
```

**or separately:**
```bash
# terminal 1 - backend
cd src/backend
source venv/bin/activate  
python main.py

# terminal 2 - frontend
cd src/frontend
npm run tauri dev
```

---

## next steps - what to build:

1. **create spotlight ui component** (src/frontend/src/components/Spotlight.tsx)
2. **add hotkey listener** (use tauri global shortcuts)
3. **build basic agent endpoint** (src/backend/agent/parser.py)
4. **connect frontend to backend** (fetch api in react)
5. **implement first command: "install chrome"**

check `project_luna_notion_structure.md` for detailed implementation specs!

---

## getting help:

- **cursor ai**: press `cmd+l` or `ctrl+l` to chat with ai
- **documentation**: see `SETUP_GUIDE.md` for detailed info
- **specs**: see `project_luna_notion_structure.md` for architecture
- **readme**: see `README.md` for project overview

---

## troubleshooting:

**backend won't start:**
```bash
# make sure venv is activated
source venv/bin/activate

# reinstall dependencies
pip install -r requirements.txt
```

**frontend won't build:**
```bash
# clear and reinstall
rm -rf node_modules package-lock.json
npm install
```

**port already in use:**
```bash
# find and kill process
lsof -i :8000
kill -9 <PID>
```

---

**happy coding! build something awesome.** 🌙
