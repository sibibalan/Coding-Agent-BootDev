import os
import sys
from google.genai import types  

# We won't allow the LLM to specify the working_directory parameter. We're going to hard code that.
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)
        abs_working_dir = os.path.abspath(working_directory)
        abs_dir = os.path.abspath(full_path)

        # Ensure the target path is inside the working directory
        if not abs_dir.startswith(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        # Ensure the target path exists and is a directory
        if not os.path.isdir(abs_dir):
            return f'Error: "{directory}" is not a directory'

        content_info = []
        for content in os.listdir(abs_dir):

            content_path = os.path.join(abs_dir, content)

            try:
                is_dir = os.path.isdir(content_path)
                size = os.path.getsize(content_path)
                content_info.append(f"- {content}: file_size={size} bytes, is_dir={is_dir}")
            except Exception as e:
                content_info.append(f"- {content}: Error retrieving info ({e})")

        return "\n".join(content_info) if content_info else f'No files found in directory "{directory}"'
    
    except Exception as e:
        return f"Error: {e}"


# def main():
#     working_dir = sys.argv[1]
#     directory = sys.argv[2] if len(sys.argv) > 2 else '.'
#     result = get_files_info(working_dir, directory)
#     print(result)

# if __name__ == '__main__':
# main()


