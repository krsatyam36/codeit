import ast
import os
import subprocess
import tempfile
import venv
import shutil
from typing import Tuple

class SandboxEngine:
    """
    Production-grade Ephemeral Execution Environment.
    Parses AST to auto-resolve dependencies, spins up an isolated venv, runs the code, and destroys the environment.
    """
    
    # Map common import names to their actual pip package names
    PACKAGE_MAP = {
        "bs4": "beautifulsoup4",
        "cv2": "opencv-python",
        "sklearn": "scikit-learn",
        "yaml": "beautifulsoup4",
        "PIL": "pillow",
        "fitz": "pymupdf"
    }

    def extract_dependencies(self, code: str) -> list[str]:
        deps = set()
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        deps.add(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        deps.add(node.module.split('.')[0])
        except SyntaxError:
            pass # If the LLM generated broken python, let the execution step catch it

        # Filter out built-in Python modules (simplified heuristic)
        built_ins = {"os", "sys", "json", "re", "math", "time", "datetime", "collections", "itertools", "random", "typing", "ast", "subprocess"}
        return [self.PACKAGE_MAP.get(dep, dep) for dep in deps if dep not in built_ins]

    async def execute(self, code: str) -> Tuple[str, str, int]:
        """Returns: (stdout, stderr, exit_code)"""
        deps = self.extract_dependencies(code)
        
        # Create a temporary directory that self-destructs when done
        with tempfile.TemporaryDirectory() as temp_dir:
            venv_dir = os.path.join(temp_dir, "venv")
            script_path = os.path.join(temp_dir, "script.py")
            
            with open(script_path, "w") as f:
                f.write(code)

            # 1. Create Ephemeral venv
            venv.create(venv_dir, with_pip=True)
            pip_exe = os.path.join(venv_dir, "bin", "pip")
            python_exe = os.path.join(venv_dir, "bin", "python")

            # 2. Auto-Install Dependencies
            install_logs = ""
            if deps:
                install_logs += f"[SYSTEM] Auto-resolving dependencies: {', '.join(deps)}...\n"
                pip_process = subprocess.run(
                    [pip_exe, "install", "--quiet"] + deps,
                    capture_output=True, text=True
                )
                if pip_process.returncode != 0:
                    return ("", f"[SYSTEM] Failed to install dependencies.\n{pip_process.stderr}", 1)
                install_logs += "[SYSTEM] Sandbox environment primed.\n"

            # 3. Execute Code with Timeout (e.g., 30 seconds to prevent infinite loops)
            try:
                process = subprocess.run(
                    [python_exe, script_path],
                    capture_output=True, text=True, timeout=30
                )
                return (install_logs + "\n" + process.stdout, process.stderr, process.returncode)
            except subprocess.TimeoutExpired:
                return (install_logs, "[SYSTEM FATAL] Execution timed out after 30 seconds. Infinite loop detected?", 124)
