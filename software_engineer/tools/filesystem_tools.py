import subprocess
import os

def create_file(path: str, content: str) -> str:
    """
    Creates a file at the specified path with the given content.
    
    Args:
        path: The absolute or relative path to the file.
        content: The text content to write to the file.
        
    Returns:
        A success message or error description.
    """
    try:
        # Ensure directory exists
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully created file at: {path}"
    except Exception as e:
        return f"Error creating file: {str(e)}"

def execute_python_file(path: str) -> str:
    """
    Executes a Python script located at the specified path.
    
    Args:
        path: The path to the Python file to execute.
        
    Returns:
        The combined stdout and stderr of the execution.
    """
    try:
        if not os.path.exists(path):
            return f"Error: File not found at {path}"
            
        result = subprocess.run(
            ["python3", path],
            capture_output=True,
            text=True,
            timeout=30  # Safety timeout
        )
        
        output = f"--- STDOUT ---\n{result.stdout}\n"
        if result.stderr:
            output += f"\n--- STDERR ---\n{result.stderr}"
            
        return output
    except subprocess.TimeoutExpired:
        return "Error: Execution timed out after 30 seconds."
    except Exception as e:
        return f"Error executing file: {str(e)}"

def run_command(command: str) -> str:
    """
    Executes a shell command.
    
    Args:
        command: The shell command to execute.
        
    Returns:
        The combined stdout and stderr of the command.
    """
    try:
        # Split command for safety if simple, but shell=True is often needed for complex commands
        # For an agent, we'll use shell=True but warn about security in a real prod env
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = f"--- STDOUT ---\n{result.stdout}\n"
        if result.stderr:
            output += f"\n--- STDERR ---\n{result.stderr}"
            
        return output
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds."
    except Exception as e:
        return f"Error running command: {str(e)}"
