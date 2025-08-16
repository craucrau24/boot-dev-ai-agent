import os
import sys
from google import genai
from dotenv import load_dotenv
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

from functions.call_function import call_function

from utils import maybe

if len(sys.argv) < 2:
  print("Missing prompt message")
  sys.exit(1)

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

user_prompt = sys.argv[1]
try:
    verbose = sys.argv[2] == "--verbose"
except IndexError:
    verbose = False

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

User don't need to know why you are calling each functions, just call them. You may begin with listing content of current directory to have better understanding of the base code. When you're done make a step by step summary.
All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

client = genai.Client(api_key=api_key)
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

for _ in range(20):
    resp = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))

    for candid in maybe(resp.candidates) | []:
        messages.append(candid.content)
    
    function_calls = resp.function_calls if resp.function_calls is not None else []

    for function_call_part in function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if maybe(function_call_result).parts[0].function_response.response.is_none():
            raise RuntimeError("unexpected empty response from function call")
        elif verbose:
            print(f"-> {maybe(function_call_result).parts[0].function_response.response | ""}")
        messages.append(function_call_result)

    if resp.text is not None:
        print(resp.text)
        break



    if verbose:
        print(f"""User prompt: {user_prompt}
    Prompt tokens: {resp.usage_metadata.prompt_token_count}
    Response tokens: {resp.usage_metadata.candidates_token_count}
    """)

