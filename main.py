import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY2")


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
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )

    if response.function_calls:
        result = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose)
            if not function_call_result.parts:
                raise Exception ("Error: no parts recieved")
            elif not function_call_result.parts[0].function_response:
                raise Exception("Error: no response")
            elif not function_call_result.parts[0].function_response.response:
                raise Exception("Error: no response")
            else:
                result.append(function_call_result.parts[0])
            
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(response.text)

    

if __name__ == "__main__":
    main()
