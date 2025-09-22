import os
import subprocess
from google.genai import types  

# We won't allow the LLM to specify the working_directory parameter. We're going to hard code that.
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="The arguments to pass to the Python file being run.",
                
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=[]):

    full_path = os.path.join(working_directory, file_path)
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(full_path)

    # Ensure the target path is inside the working directory
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    # Ensure the target path exists and is a file
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'

    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        cmd = ["python", abs_file_path] + args

        completed_process = subprocess.run(
            args = cmd,
            timeout=30,  # 30 seconds timeout
            capture_output=True, # capture stdout and stderr
            text=True, # check for exit code
            cwd = abs_working_dir
        )


        stdout = completed_process.stdout.strip()
        stderr = completed_process.stderr.strip()
        exit_code = completed_process.returncode

        output_parts = []

        if stdout:
            output_parts.append(f"STDOUT:\n{stdout}")
        if stderr:
            output_parts.append(f"STDERR:\n{stderr}")
        if exit_code != 0:
            output_parts.append(f"Process exited with code {exit_code}")

        if not output_parts:
            return "No output produced."

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing file: {e}"


