import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function
import sys

load_dotenv()







def main():
    api_key = os.environ.get("GEMINI_API_KEY"+"1")
    parser = argparse.ArgumentParser(description="AiAgent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    prompt = args.user_prompt
    verbose = args.verbose
    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]
    exit_code=0
    kn = 1
    for i in range(20):
        kn = (i // 5) + 1
        api_key = os.environ.get(f"GEMINI_API_KEY{kn}")
        
        client = genai.Client(api_key=api_key)
        if i == 19:
            messages.append(types.Content(role="user", parts=[types.Part(text="""hey, maximum iterations...""")]))
            response = gemini_resonse(client, messages)
            print(response.text)
            exit_code=1
            break
        else:
            response = gemini_resonse(client, messages)
            candidates = response.candidates
        
        if candidates:
            for candidate in candidates:
                messages.append(candidate.content)

        if response.function_calls:
            function_results = []
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose)
                if not function_call_result.parts:
                    raise Exception ("Error: no parts recieved")
                elif not function_call_result.parts[0].function_response:
                    raise Exception("Error: no response")
                elif not function_call_result.parts[0].function_response.response:
                    raise Exception("Error: no response")
                else:
                    function_results.append(function_call_result.parts[0])
                
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=function_results))
        else:
            print(response.text)
            break
    
    sys.exit(exit_code)
        

    
def gemini_resonse(client, messages):
    return client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
        )
    

if __name__ == "__main__":
    main()
