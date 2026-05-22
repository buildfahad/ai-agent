import os
def get_files_info(working_directory: str, directory: str = ".") -> str:
    
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        else:
            file_list = os.listdir(target_dir)
            files: str = ""
            for file in file_list:
                    files += f'- {file} file_size={os.path.getsize(target_dir+"/"+file)} bytes, is_dir={os.path.isdir(target_dir+"/"+file)}\n'

            files = f'Result for currect directory:\n'+files
            return files
    except Exception as e:
        return f"Error: {e}"
