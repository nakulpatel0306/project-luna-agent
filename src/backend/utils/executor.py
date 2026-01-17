"""
command executor - seamless sudo handling for Luna

Provides:
- Native macOS password dialog for sudo (no terminal prompts)
- Credential caching (~5 minutes per macOS default)
- Auto-detection of commands needing elevated privileges
- Non-interactive mode for Homebrew and other installers
"""

import subprocess
import platform
import os
import time
from typing import Optional, Tuple

# Track when we last acquired sudo credentials
_sudo_timestamp: float = 0
_SUDO_CACHE_DURATION: int = 280  # slightly less than macOS default 5 min


def _check_sudo_cached() -> bool:
    """
    Check if sudo credentials are currently cached (non-interactive check).
    """
    try:
        result = subprocess.run(
            ["sudo", "-n", "true"],
            capture_output=True,
            timeout=2
        )
        return result.returncode == 0
    except:
        return False


def ensure_sudo_access() -> bool:
    """
    Ensure sudo access via native macOS password dialog.

    Uses osascript to show the same password dialog that macOS apps use.
    Credentials are cached for ~5 minutes by macOS, making subsequent
    commands seamless.

    Returns:
        True if sudo access granted, False otherwise
    """
    global _sudo_timestamp

    # Check if we have recent cached credentials
    if time.time() - _sudo_timestamp < _SUDO_CACHE_DURATION:
        if _check_sudo_cached():
            print("   ✅ sudo credentials cached")
            return True

    # Quick check if already cached from previous session
    if _check_sudo_cached():
        _sudo_timestamp = time.time()
        print("   ✅ sudo credentials already available")
        return True

    print("   🔐 requesting sudo access via macOS dialog...")

    try:
        # Use osascript to show native macOS password dialog
        # This is the standard way macOS apps request admin privileges
        script = '''
        do shell script "sudo -v" with administrator privileges
        '''

        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            timeout=120  # 2 minutes for user to respond
        )

        if result.returncode == 0:
            _sudo_timestamp = time.time()

            # Extend sudo timeout to maximum (keeps credentials for longer)
            subprocess.run(
                ["sudo", "-v"],
                capture_output=True,
                timeout=5
            )

            print("   ✅ sudo access granted - session authenticated")
            return True
        else:
            error_msg = result.stderr.strip() if result.stderr else "user cancelled"
            print(f"   ❌ sudo access denied: {error_msg}")
            return False

    except subprocess.TimeoutExpired:
        print("   ⏱️  password dialog timed out")
        return False
    except Exception as e:
        print(f"   ❌ failed to request sudo: {e}")
        return False


def needs_sudo(command: str) -> bool:
    """
    Detect if a command needs sudo/admin access.

    Checks for:
    - Explicit sudo prefix
    - System-level package manager operations
    - Global package installations
    - System directory modifications

    Returns:
        True if command needs sudo, False otherwise
    """
    command_lower = command.lower()

    # Explicit sudo commands
    if command.strip().startswith("sudo "):
        return True

    # System package managers that typically need sudo
    sudo_patterns = [
        # Linux package managers
        "apt-get install", "apt-get update", "apt-get upgrade", "apt-get remove",
        "apt install", "apt update", "apt upgrade", "apt remove",
        "yum install", "yum update", "yum remove",
        "dnf install", "dnf update", "dnf remove",
        "pacman -S", "pacman -U", "pacman -R",
        "zypper install", "zypper update",

        # Global npm (may need sudo on some systems)
        "npm install -g", "npm i -g", "npm uninstall -g",

        # System modifications
        "/usr/local/bin", "/usr/bin", "/usr/sbin",
        "systemctl", "service ",
        "launchctl",

        # Homebrew install script (first-time install)
        "raw.githubusercontent.com/Homebrew/install",
    ]

    for pattern in sudo_patterns:
        if pattern.lower() in command_lower:
            return True

    return False


def needs_homebrew_noninteractive(command: str) -> bool:
    """
    Detect if command is a Homebrew operation that should run non-interactively.
    """
    homebrew_patterns = [
        "brew install", "brew upgrade", "brew update",
        "brew cask install", "brew reinstall",
        "brew tap", "brew untap",
        "/Homebrew/install",  # Homebrew installation script
    ]

    command_lower = command.lower()
    for pattern in homebrew_patterns:
        if pattern.lower() in command_lower:
            return True

    return False


def get_execution_env(command: str) -> dict:
    """
    Get environment variables for command execution.
    Adds non-interactive flags for installers that support them.
    """
    env = os.environ.copy()

    # Homebrew non-interactive mode
    if needs_homebrew_noninteractive(command):
        env['NONINTERACTIVE'] = '1'
        env['HOMEBREW_NO_AUTO_UPDATE'] = '1'  # Skip auto-update for faster installs
        env['CI'] = '1'  # CI mode = non-interactive
        print("   ⚙️  homebrew: non-interactive mode enabled")

    # Node.js installers
    if "nvm" in command.lower() or "fnm" in command.lower():
        env['NONINTERACTIVE'] = '1'

    # Python installers
    if "pyenv" in command.lower():
        env['PYENV_ROOT'] = env.get('PYENV_ROOT', os.path.expanduser('~/.pyenv'))

    return env


def execute_command(
    command: str,
    timeout: int = 300,
    require_sudo: bool = False
) -> Tuple[bool, str, str]:
    """
    Execute a shell command with seamless sudo handling.

    If the command needs sudo, we request it via native macOS dialog ONCE,
    then all subsequent commands use cached credentials.

    Args:
        command: Shell command to execute
        timeout: Max execution time in seconds (default 5 minutes)
        require_sudo: Force sudo access request

    Returns:
        Tuple of (success: bool, stdout: str, stderr: str)
    """
    # Validate command safety first
    is_safe, reason = validate_command_safety(command)
    if not is_safe:
        return False, "", f"command blocked: {reason}"

    try:
        # Check if command needs sudo
        if require_sudo or needs_sudo(command):
            print(f"   🔒 elevated privileges required")
            if not ensure_sudo_access():
                return False, "", "sudo access denied - user cancelled authentication"

        # Get appropriate environment
        env = get_execution_env(command)

        # Platform-specific shell handling
        if platform.system() == "Windows":
            shell = True
            executable = None
        else:
            # Unix: use bash for better compatibility
            shell = True
            executable = "/bin/bash"

        print(f"   ▶ executing: {command[:80]}{'...' if len(command) > 80 else ''}")

        # Execute the command
        result = subprocess.run(
            command,
            shell=shell,
            executable=executable,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env
        )

        success = result.returncode == 0

        if success:
            print(f"   ✅ command completed successfully")
        else:
            print(f"   ❌ command failed (exit code: {result.returncode})")

        return success, result.stdout, result.stderr

    except subprocess.TimeoutExpired:
        return False, "", f"command timed out after {timeout} seconds"
    except Exception as e:
        return False, "", f"execution error: {str(e)}"


def check_tool_installed(tool: str) -> bool:
    """
    Check if a command line tool is installed and accessible.

    Args:
        tool: Name of the tool to check (e.g., 'brew', 'node', 'python')

    Returns:
        True if tool is found in PATH, False otherwise
    """
    try:
        if platform.system() == "Windows":
            command = f"where {tool}"
        else:
            command = f"which {tool}"

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except:
        return False


def validate_command_safety(command: str) -> Tuple[bool, Optional[str]]:
    """
    Validate that a command is safe to execute.

    Blocks commands that could cause catastrophic system damage.

    Returns:
        Tuple of (is_safe: bool, reason_if_unsafe: Optional[str])
    """
    # Dangerous patterns that could destroy the system
    dangerous_patterns = [
        # Filesystem destruction
        ("rm -rf /", "recursive deletion of root filesystem"),
        ("rm -rf /*", "recursive deletion of all root directories"),
        ("rm -rf ~", "recursive deletion of home directory"),
        ("rm -rf $HOME", "recursive deletion of home directory"),

        # Disk operations
        ("dd if=", "direct disk write operation"),
        ("mkfs", "filesystem format operation"),
        ("> /dev/sd", "direct write to disk device"),
        ("> /dev/nvme", "direct write to disk device"),

        # Fork bomb
        (":(){ :|:& };:", "fork bomb"),

        # Network attacks
        ("nc -e", "potential reverse shell"),

        # Credential theft patterns
        ("curl | sh", None),  # We allow this, it's common for installers
        ("wget | sh", None),  # We allow this too
    ]

    command_lower = command.lower()

    for pattern, reason in dangerous_patterns:
        if reason and pattern.lower() in command_lower:
            return False, reason

    # Additional check: prevent rm with both -r and / at root level
    if "rm " in command_lower and "-r" in command_lower:
        # Check if targeting root or home without specificity
        parts = command.split()
        for part in parts:
            if part in ["/", "/*", "~", "$HOME", "~/*"]:
                return False, "recursive deletion of critical directory"

    return True, None


def get_risk_level(command: str) -> str:
    """
    Assess the risk level of a command.

    Returns:
        'safe' - read-only operations
        'moderate' - installs, modifications
        'dangerous' - sudo, system changes, deletions
    """
    command_lower = command.lower()

    # Safe: read-only operations
    safe_patterns = [
        "which ", "where ", "ls ", "cat ", "echo ", "pwd",
        "docker ps", "docker images", "docker --version",
        "git status", "git log", "git branch", "git diff",
        "node --version", "npm --version", "python --version",
        "brew --version", "brew list", "brew info",
    ]

    for pattern in safe_patterns:
        if command_lower.startswith(pattern) or f" {pattern}" in command_lower:
            return "safe"

    # Dangerous: sudo, rm, system modifications
    dangerous_patterns = [
        "sudo ", "rm ", "rmdir ", "uninstall", "remove",
        "chmod ", "chown ", "kill ", "pkill ",
        "systemctl", "launchctl",
    ]

    for pattern in dangerous_patterns:
        if pattern in command_lower:
            return "dangerous"

    # Moderate: installs, writes, network
    return "moderate"

