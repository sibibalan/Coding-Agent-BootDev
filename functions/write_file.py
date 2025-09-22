import os
from google.genai import types  

# We won't allow the LLM to specify the working_directory parameter. We're going to hard code that.
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites content to a file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)




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