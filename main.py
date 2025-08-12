import os
import sys
from google import genai
from dotenv import load_dotenv
from google.genai import types


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

client = genai.Client(api_key=api_key)
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

resp = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)
print(resp.text)

if verbose:
    print(f"""User prompt: {user_prompt}
Prompt tokens: {resp.usage_metadata.prompt_token_count}
Response tokens: {resp.usage_metadata.candidates_token_count}
""")

