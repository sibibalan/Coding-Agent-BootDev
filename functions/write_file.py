import os

def write_file(working_directory, file_path, content):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(full_path)

        # Ensure the target path is inside the working directory
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        # Ensure the target directory exists
        target_dir = os.path.dirname(abs_file_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)
            
        try:
            with open(abs_file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except Exception as e:
            return f'Error writing to "{file_path}": {str(e)}'
    except Exception as e:
        return f"Error: {str(e)}"