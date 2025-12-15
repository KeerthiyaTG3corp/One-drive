# gpt_autofill.py
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_INSTRUCTIONS = """
You are a strict information extraction assistant.
You MUST answer questions using ONLY the content provided below under "QUESTIONNAIRE" and "EVIDENCE".
Do NOT use any external knowledge or the internet.

If the information is not present in the provided sources,
reply exactly: "Not found in source".

Return the final answers ONLY as a JSON object:

{
  "answers": [
    {
      "question_index": 1,
      "question": "<original question>",
      "answer": "<answer or 'Not found in source'>"
    }
  ]
}

No extra text. No explanation. Only JSON.
"""

def _build_user_prompt(questionnaire_text, evidence_texts):
    prompt = "\nQUESTIONNAIRE:\n" + questionnaire_text + "\n\nEVIDENCE:\n"

    for fname, txt in evidence_texts.items():
        prompt += f"\n--- BEGIN {fname} ---\n"
        prompt += (txt or "[EMPTY]") + "\n"
        prompt += f"--- END {fname} ---\n"

    prompt += """
TASK:
Extract ALL questions from the QUESTIONNAIRE and answer them
ONLY using the EVIDENCE. If an answer is not found, write "Not found in source".
Return ONLY the JSON.
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
