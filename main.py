import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types  

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

    # verbose = False
    # if len(sys.argv) > 2:
    #     if sys.argv[2] == '--verbose':
    #         verbose = True
    
    user_prompt = sys.argv[1] # get the user prompt from command line argument
    verbose = '--verbose' in sys.argv  # Check if --verbose flag is present

    messages = [
        types.Content(
            role='user',
            parts=[types.Part(text=user_prompt)]
            )
            ]
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages
        )
        
    
    except Exception as e:
        print(f"Error during API call: {e}")
        sys.exit(1)

    

    if verbose:
        # print(response.text)
        # prompt_tokens = response.usage_metadata.prompt_token_count
        # response_tokens = response.usage_metadata.candidates_token_count
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        pass

if __name__ == "__main__":
    main()


# Notes:
# response = client.models.generate_content()
# The generate_content method returns a GenerateContentResponse object.
# Print the .text property of the response to see the model's answer.
# You can access token usage details via the .usage_metadata property of the response.