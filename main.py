import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types  

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

# global variables:
epoch = 10

load_dotenv()  # Load environment variables from .env file
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


if not GOOGLE_API_KEY:
    print("Error: GOOGLE_API_KEY not found in environment variables.")
    sys.exit(1)

client = genai.Client(api_key=GOOGLE_API_KEY)

def main():
    if len(sys.argv) < 2:
        print("Usage: uv run main.py '<User Prompt>' [optional| --verbose]")
        sys.exit(1)
    
    user_prompt = sys.argv[1] # get the user prompt from command line argument
    verbose = '--verbose' in sys.argv  # Check if --verbose flag is present
    print('verbose:', verbose)
    
    messages = [
        types.Content(
            role='user',
            parts=[
                types.Part(text=user_prompt)
            ]
        )
    ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    When the user asks about the code project - they are referring to 
    the working directory. So, you should typically start by looking at 
    the project's files, and figuring out how to run the project and how 
    to run its tests, you'll always want to test the tests and the actual project 
    to verify that behavior is working.

    All paths you provide should be relative to the working directory.
    You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """


    text_parts = []
    for _ in range(epoch):
        # print('iter:', _)
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=messages,
                config=types.GenerateContentConfig(
                    tools = [available_functions],
                    system_instruction=system_prompt
                ),
            )
            # print(response)
            # print('-'*50)
            # print(response.text)

            for candidate in response.candidates:
                messages.append(candidate.content)


            
            for candidate in response.candidates:
                for part in candidate.content.parts:
                    if part.text and not part.function_call:  # Only collect plain text
                        text_parts.append(part.text.strip())
            

            if response.function_calls:
                for function_call_part in response.function_calls:
                    function_call_result = call_function(
                                function_call_part,
                                verbose=verbose)
                    messages.append(function_call_result)
               
                    
            else:
                print('Final Response:')
                print("\n\n".join(text_parts))
                return 

                

            #     func_call = False
            #     if candidate.content and candidate.content.parts:
                    
            #         for part in candidate.content.parts:

            #             if part.function_call: # if its a function call, execute it.
            #                 func_call = True
            #                 print('inside function call')
            #                 function_call_result = call_function(
            #                     part.function_call,
            #                     verbose=verbose
            #                 )
                            
            #                 function_response = function_call_result.parts[0].function_response.response
                            
            #                 if function_response and "result" in function_response:
            #                     messages.append(types.Content(
            #                         role='user',
            #                         parts=[types.Part(text=function_response['result'])]
            #                     ))
                            
            #                     if verbose:
            #                         pass
            #                         # print(f"Function call response: {function_response}")
                            
            #         if response.text and not func_call:
            #             #if it's a plain text then its final response.
            #             print(f"Final Response: {part.text}")
            #             return
                        

        except Exception as e:
                print(f"Error during API call: {e}")
                sys.exit(1)
            
    print(f"No final text response after max iterations - {epoch}.")

if __name__ == "__main__":
    main()