import os
import subprocess

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
