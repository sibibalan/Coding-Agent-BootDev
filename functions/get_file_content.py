import os
from functions.config import content_config

from google.genai import types  

# We won't allow the LLM to specify the working_directory parameter. We're going to hard code that.
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the content of a file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to retrieve content from, relative to the working directory.",
            ),
        },
    ),
)

# config
character_limit = content_config.get('character_limit', 10000)
        

def count_characters(text):
    return len(text)

def get_file_content(working_directory, file_path):
        
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(full_path)

        # Ensure the target path is inside the working directory
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        # Ensure the target path exists and is a file
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(abs_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if the file_path exceeds character limit
        if count_characters(content) > character_limit:
            return content[:character_limit] + f"...File \"{file_path}\" truncated at {character_limit} characters"

        return content
    
    except Exception as e:
        return f"Error: {e}"


