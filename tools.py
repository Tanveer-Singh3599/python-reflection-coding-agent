import os
import tempfile
import subprocess
from tavily import TavilyClient
from dotenv import load_dotenv
from langchain.tools import tool

load_dotenv() # load environment variables (api key(s)) from the .env file

# web searching tool
@tool(parse_docstring=True)
def web_search(query: str) -> dict:
    """
    Executes a web search based on the provided query and aggregates the results.
    
    This function collects information from various online sources and compiles 
    the data into a structured JSON-formatted dictionary containing metadata, 
    response times, and ranked search results.

    Args:
        query (str): The search string used to query the web.

    Returns:
        dict: A dictionary containing the combined search results and metadata.
    """
    tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
    response = tavily_client.search(query)
    return response


# coding environment
@tool(parse_docstring=True)
def coding_environment(code: str, mode: str, timeout: int) -> dict:
    """
    Execute Python or shell code inside an isolated Docker container.

    Args:
        code (str): Source code or shell commands.
        mode (str): "python" or "shell".
        timeout (int): Max execution time in seconds.

    Returns:
        dict: Execution results.
    """

    with tempfile.TemporaryDirectory() as tmpdir:

        if mode == "python":
            filename = "script.py"

        elif mode == "shell":
            filename = "script.sh"

        else:
            return {
                "success": False,
                "error": "Invalid mode. Use 'python' or 'shell'."
            }

        file_path = os.path.join(tmpdir, filename)

        with open(file_path, "w") as f:
            f.write(code)

        # Make shell script executable
        if mode == "shell":
            os.chmod(file_path, 0o755)

        # Command selection
        if mode == "python":
            exec_cmd = ["python", f"/app/{filename}"]

        else:
            exec_cmd = ["sh", f"/app/{filename}"]

        cmd = [
            "docker", "run",
            "--rm",

            # Resource limits
            "--memory", "100m",
            "--cpus", "0.5",
            "--pids-limit", "64",

            # Better process handling
            "--init",

            # Mount workspace
            "-v", f"{tmpdir}:/app",

            # Image
            "agent-python:3.13",

            *exec_cmd
        ]

        try:

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode
            }

        except subprocess.TimeoutExpired:

            return {
                "success": False,
                "stdout": "",
                "stderr": "Execution timed out",
                "exit_code": None
            }

        except Exception as e:

            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "exit_code": None
            }