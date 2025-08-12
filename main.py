import os
import sys
from google import genai
from dotenv import load_dotenv

if len(sys.argv) < 2:
  print("Missing prompt message")
  sys.exit(1)

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

prompt = sys.argv[1]
client = genai.Client(api_key=api_key)
resp = client.models.generate_content(model="gemini-2.0-flash-001", contents=prompt)
print(resp.text)

print(f"""Prompt tokens: {resp.usage_metadata.prompt_token_count}
Response tokens: {resp.usage_metadata.candidates_token_count}
""")

