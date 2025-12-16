# gpt_autofill.py
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_INSTRUCTIONS = """
You are a strict compliance questionnaire answering assistant.

You MUST:
- Answer ONLY using the provided EVIDENCE.
- Follow the response_type strictly.
- Answer ALL questions.
- Never skip a question.

If information is NOT found in the evidence:
Return "Not found in source".

Return ONLY valid JSON.
No explanations. No assumptions.
"""

def _build_user_prompt(questions, evidence_texts):
    prompt = """
You are given a LIST of compliance questions.
Each question includes:
- question_index
- question
- description
- response_type
"""

    prompt += "\nQUESTIONS (JSON):\n"
    prompt += json.dumps(questions, indent=2)

    prompt += "\n\nEVIDENCE:\n"

    for fname, txt in evidence_texts.items():
        prompt += f"\n--- BEGIN {fname} ---\n"
        prompt += (txt or "[EMPTY]") + "\n"
        prompt += f"--- END {fname} ---\n"

    prompt += """
TASK:
Answer EVERY question using ONLY the evidence.
Follow response_type strictly.

Return ONLY this JSON structure:

{
  "answers": [
    {
      "question_index": 1,
      "question": "...",
      "description": "...",
      "response_type": "...",
      "answer": "..."
    }
  ]
}
"""
    return prompt

def ask_questions_with_evidence(questions, evidence_texts):
    user_prompt = _build_user_prompt(questions, evidence_texts)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_INSTRUCTIONS},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.0,
        max_tokens=1800
    )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except Exception:
        start = content.find("{")
        end = content.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(content[start:end+1])
            except Exception:
                return {"error": "Failed to parse JSON", "raw": content}
        return {"error": "No JSON found", "raw": content}
