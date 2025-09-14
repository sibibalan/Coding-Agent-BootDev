import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types  

load_dotenv()  # Load environment variables from .env file
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=GOOGLE_API_KEY)

# contents = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

# response = client.models.generate_content()
# The generate_content method returns a GenerateContentResponse object.
# Print the .text property of the response to see the model's answer.


def main():
    if len(sys.argv) < 2:
        print("Usage: uv run main.py '<User Prompt>'")
        sys.exit(1)

    verbose = False
    if len(sys.argv) > 2:
        if sys.argv[2] == '--verbose':
            verbose = True
    
    user_prompt = sys.argv[1] # get the user prompt from command line argument
    
    messages = [
        types.Content(
            role='user',
            parts=[types.Part(text=user_prompt)]
            )
            ]

    response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents= messages
    )
    # print(response.text)

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
    else:
        pass

    # print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    # print("Response tokens:", response.usage_metadata.candidates_token_count)

if __name__ == "__main__":
    main()
