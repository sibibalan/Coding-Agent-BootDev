import os

from google.genai import types

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file


function_map = {
    "get_files_info": get_files_info, #working_directory, directory="."
    "get_file_content": get_file_content, #working_directory, file_path
    "run_python_file": run_python_file, #working_directory, file_path, args=""
    "write_file": write_file #working_directory, file_path, content
}

working_directory = "./calculator"

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args
    
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    function = function_map.get(function_name, None)
    if function:
        function_result = function(working_directory, **function_args)

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                    )
                ],
            )

    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )


