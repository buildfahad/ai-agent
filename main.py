import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")


client = genai.Client(api_key=api_key)


def main():
    
    parser = argparse.ArgumentParser(description="AiAgent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    prompt = args.user_prompt
    verbose = args.verbose
    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages
    )

    if verbose:
        if response.usage_metadata != None:
            print(f"User prompt: {prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            print("Response: ")
            print(response.text)
        else:
            raise RuntimeError("error fetching, or no response")
    else:
        print("Response: ")
        print(response.text)

if __name__ == "__main__":
    main()
