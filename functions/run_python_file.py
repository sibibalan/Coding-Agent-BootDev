import os
import subprocess


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


