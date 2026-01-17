# usage guide

how to use luna to run development commands.

## basic workflow

1. **start luna** - run backend and frontend (see [setup guide](SETUP.md))
2. **enter command** - type what you want to do in plain english
3. **review plan** - luna shows you the execution steps
4. **execute** - click the button to run the commands
5. **view results** - see output and errors for each step

## entering commands

type your command in the spotlight input and press enter.

**example commands:**

```
install chrome
install vscode
install slack
check docker status
which brew
which node
```

### with openai api key

when an api key is configured, you can use any natural language:

```
setup python with pip and virtualenv
install node version manager
create a react project with typescript
check if git is configured
install the latest java development kit
```

### without api key (fallback mode)

these specific commands work without an api key:

| command | what it does |
|---------|--------------|
| `install chrome` | `brew install --cask google-chrome` |
| `install vscode` | `brew install --cask visual-studio-code` |
| `install slack` | `brew install --cask slack` |
| `check docker status` | checks docker version and daemon |
| `which <tool>` | checks if a tool is installed |

## understanding the execution plan

after entering a command, luna displays a plan:

```
┌─────────────────────────────────────────────────┐
│  execution plan                                 │
│  install chrome                     [2-3 min]  │
├─────────────────────────────────────────────────┤
│  ○  check if homebrew is installed    [safe]   │
│     $ which brew                               │
│                                                │
│  ○  install google chrome          [moderate]  │
│     $ brew install --cask google-chrome        │
│                                                │
│  ○  verify installation               [safe]   │
│     $ ls -la /Applications/Google\ Chrome.app  │
├─────────────────────────────────────────────────┤
│  [execute 3 steps]                             │
└─────────────────────────────────────────────────┘
```

### risk levels

each step has a risk indicator:

| level | color | meaning |
|-------|-------|---------|
| safe | green | read-only operations, version checks, listing files |
| moderate | amber | installations, file writes, network operations |
| dangerous | red | sudo commands, deletions, system modifications |

### viewing commands

click on any step to see the exact shell command that will run.

## executing commands

### confirmation

click "execute N steps" to run the plan. steps run sequentially.

### status indicators

during execution, each step shows its status:

| icon | status | meaning |
|------|--------|---------|
| ○ | pending | not started |
| ⟳ | running | currently executing |
| ✓ | completed | finished successfully |
| ✗ | failed | error occurred |

### viewing output

after execution, click on a step to expand and see:
- **output:** stdout from the command
- **error:** stderr if the command failed

## sudo commands

when a command requires administrator privileges:

1. luna detects the need for sudo
2. macos shows its native password dialog
3. you enter your password once
4. credentials are cached for ~5 minutes
5. subsequent sudo commands run automatically

**important:** you never type your password in the terminal or luna. always use the native macos dialog.

## canceling

- click "done" after execution completes
- this clears the plan and returns to the input
- there's no way to cancel mid-execution (commands run to completion or timeout)

## keyboard shortcuts

| shortcut | action |
|----------|--------|
| `enter` | submit command / confirm |
| `esc` | clear input |
| `cmd+k` | open luna (future feature) |

## tips

### be specific

more specific commands give better results:

```
# vague
setup python

# specific
install python 3.11 using homebrew
```

### check before installing

use "which" or "check" commands to see what's already installed:

```
which python
which node
check docker status
```

### review dangerous operations

always review steps marked as "dangerous" before executing:
- sudo commands
- deletion operations
- system modifications

### handling failures

if a step fails:
1. execution stops at that step
2. click the step to see the error
3. fix the underlying issue
4. try the command again

## limitations

### macos only

the current sudo handling uses `osascript`, which is macos-specific. windows and linux are not supported yet.

### homebrew required

package installation commands use homebrew. make sure it's installed:

```bash
brew --version
```

### no global hotkey

luna must be focused to receive input. the global hotkey feature (cmd+k from anywhere) is not yet implemented.

### 5-minute timeout

commands have a 5-minute timeout. long-running operations may fail.

## examples

### setting up a new machine

```
install chrome
install vscode
install slack
install docker
```

### checking development tools

```
which brew
which node
which python
which git
check docker status
```

### with llm (requires api key)

```
install the latest version of node using nvm
setup a python virtual environment
install postgresql and start it
configure git with my email john@example.com
```
