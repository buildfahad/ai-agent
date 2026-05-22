import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_path = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs

        if not valid_target_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        elif os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        else:
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            with open(target_path, "w") as f:
                f.write(content)
                
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'  
    except Exception as e:
        return f"Error: {e}"
    


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the given content to the specified file on a given file_path. Then returns a string mentioning the file_path (the given parameter), and length of the content written in characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            #this is the file path parametere info
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to file that we want to write to, relative to the working directory (default is the working directory itself)",
            ),
            #this is the content parameter info
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content that we want to write to the specified file."
            )
        },
    ),
    
)