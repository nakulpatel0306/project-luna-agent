"""
command executor - safely runs shell commands
"""

import subprocess
import platform
from typing import Optional, Tuple


def execute_command(
    command: str,
    timeout: int = 300,
    require_sudo: bool = False
) -> Tuple[bool, str, str]:
    """
    execute a shell command and return results
    
    returns:
        (success: bool, stdout: str, stderr: str)
    """
    try:
        # determine shell based on OS
        shell = True
        if platform.system() == "Windows":
            shell = True
        
        # execute command
        result = subprocess.run(
            command,
            shell=shell,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        success = result.returncode == 0
        return success, result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        return False, "", f"command timed out after {timeout} seconds"
    except Exception as e:
        return False, "", str(e)


def check_tool_installed(tool: str) -> bool:
    """
    check if a command line tool is installed
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
