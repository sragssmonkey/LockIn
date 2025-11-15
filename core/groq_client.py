# core/groq_client.py
import os
import json
from groq import Groq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise Exception("GROQ_API_KEY is not set!")

client = Groq(api_key=GROQ_API_KEY)
def generate_mcqs(text, num_questions=5):
    prompt = f"""
Generate {num_questions} MCQs based on the following text.

Return ONLY JSON in this format:

{{
  "mcqs": [
    {{
      "question": "string",
      "options": ["A", "B", "C", "D"],
      "answer": "A",
      "explanation": "string"
    }}
  ]
}}

Text:
{text}
"""
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Return valid JSON only. No explanations."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )

        raw = resp.choices[0].message.content.strip()

        print("\n===== RAW MODEL RESPONSE =====")
        print(raw)
        print("==============================\n")

        # 🔥 REMOVE CODE FENCES LIKE ```json and ```
        cleaned = raw.replace("```json", "").replace("```", "").strip()

        # Try strict JSON parse
        return json.loads(cleaned)

    except json.JSONDecodeError:
        # fallback: extract JSON with regex
        import re
        match = re.search(r"\{[\s\S]*\}", raw)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass
        return {"error": "Model returned invalid JSON"}

    except Exception as e:
        return {"error": str(e)}
