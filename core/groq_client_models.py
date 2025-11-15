import os
from groq import Groq

api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    raise Exception("GROQ_API_KEY not found in environment")

client = Groq(api_key=api_key)

print("\n=== Available Groq Models ===\n")
for m in client.models.list().data:
    print("-", m.id)
