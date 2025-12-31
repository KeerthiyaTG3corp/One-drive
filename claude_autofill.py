import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


SYSTEM_INSTRUCTIONS = """
You are a strict compliance questionnaire answering assistant.
_
Rules:
- Use ONLY the provided EVIDENCE.
- Follow response_type strictly if provided.
- Answer ALL questions.
- If information is missing, answer exactly:
  "Not found in source"
- Return ONLY valid JSON.
"""

def ask_questions_with_evidence(questions, evidence_texts):
    # Combine all evidence
    evidence_block = ""
    for fname, text in evidence_texts.items():
        if text.strip():
            evidence_block += f"\n--- {fname} ---\n{text}\n"

    prompt = f"""
{SYSTEM_INSTRUCTIONS}

EVIDENCE:
{evidence_block}

QUESTIONS (JSON):
{json.dumps(questions, indent=2)}

Return ONLY this JSON:
{{
  "answers": [
    {{
      "question_index": 1,
      "question": "...",
      "description": "...",
      "response_type": "...",
      "answer": "..."
    }}
  ]
}}
"""

    response = client.messages.create(
        model="claude-3.5-pro",
        temperature=0.0,
        max_tokens=1200,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    raw = response.content[0].text.strip()

    try:
        return json.loads(raw)
    except Exception:
        return {"error": "Invalid JSON from Claude", "raw": raw}

    
