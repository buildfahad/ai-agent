import os
import subprocess
from google.genai import types

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None):
    try:
        abs_directory = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_directory, file_path))
        is_valid_directory = os.path.commonpath([abs_directory, target_path]) == abs_directory

        if not is_valid_directory:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        elif not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        else:
            command = ["python", target_path]
            if args:
                command.extend(args)
    
            result = subprocess.run(command, cwd=abs_directory, capture_output=True, text=True, timeout=30)
            output = ""
            if result.returncode != 0:
                output += f"Process exited with code {result.returncode}"
            elif not result.stdout and not result.stderr:
                output += "No output produced"
            else:
                output += f"STDOUT: {result.stdout} STDERR: {result.stderr}"
                return output
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file at the given file_path within the working directory. Optionally accepts a list of arguments to pass to the script. Returns the output or an error message.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of string arguments to pass to the Python script.",
                items=types.Schema(type=types.Type.STRING),
                nullable=True,
            ),
        },
    ),
)