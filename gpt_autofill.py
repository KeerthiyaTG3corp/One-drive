# gpt_autofill.py
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_INSTRUCTIONS = """
You are a strict compliance questionnaire answering assistant.

Each question appears as a BLOCK with:
1) Question
2) Description / Clarification
3) Response Type

You MUST:
- Answer ONLY using the provided EVIDENCE.
- Use the Description / Clarification to decide what details to include.
- Follow the Response Type strictly.

Response Type rules:
- Yes/No: Answer ONLY "Yes" or "No".
- Free text: Answer in descriptive text.
- Yes/No + Free text: Start with Yes or No, followed by a brief explanation.
- Yes/No + URL: Start with Yes or No, followed by a URL if present in evidence.

If the information is NOT found in the EVIDENCE:
- Return "Not found in source" as the answer.

Return ONLY valid JSON in the EXACT format specified.
No explanations. No assumptions. No external knowledge.
"""

def _build_user_prompt(questionnaire_text, evidence_texts):
    prompt = """
QUESTIONNAIRE:
The questionnaire consists of repeated BLOCKS in the following order:

Question
Description / Clarification
Response Type
"""

    prompt += "\n" + questionnaire_text + "\n\n"

    prompt += "EVIDENCE:\n"

    for fname, txt in evidence_texts.items():
        prompt += f"\n--- BEGIN {fname} ---\n"
        prompt += (txt or "[EMPTY]") + "\n"
        prompt += f"--- END {fname} ---\n"

    prompt += """
TASK:
For EACH question block in the QUESTIONNAIRE:

1. Identify:
   - Question
   - Description / Clarification
   - Response Type

2. Use the Description to understand WHAT information is required.

3. Answer strictly using ONLY the EVIDENCE.

4. Format the answer strictly according to the Response Type rules.

5. If the answer is not found in the evidence, write:
   "Not found in source"

Return ONLY the following JSON structure:

{
  "answers": [
    {
      "question_index": 1,
      "question": "<question text>",
      "description": "<description / clarification text>",
      "response_type": "<response type>",
      "answer": "<final formatted answer>"
    }
  ]
}

Return ONLY valid JSON. No extra text.
"""
    return prompt


def ask_questions_with_evidence(questionnaire_text, evidence_texts):
    user_prompt = _build_user_prompt(questionnaire_text, evidence_texts)

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
    except:
        # attempt to extract JSON
        start = content.find("{")
        end = content.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(content[start:end+1])
            except Exception:
                return {"error": "Failed to parse JSON", "raw": content}
        return {"error": "No JSON found", "raw": content}
