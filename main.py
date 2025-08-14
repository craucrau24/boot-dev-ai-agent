import os
import sys
from google import genai
from dotenv import load_dotenv
from google.genai import types

from functions.get_files_info import schema_get_files_info

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

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

client = genai.Client(api_key=api_key)
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

resp = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))

print(resp.text)
function_calls = resp.function_calls if resp.function_calls is not None else []

for function_call_part in function_calls:
    print(f"Calling function: {function_call_part.name}({function_call_part.args})")



if verbose:
    print(f"""User prompt: {user_prompt}
Prompt tokens: {resp.usage_metadata.prompt_token_count}
Response tokens: {resp.usage_metadata.candidates_token_count}
""")

