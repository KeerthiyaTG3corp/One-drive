from extract_file import extract_text
from gpt_autofill import ask_questions_with_evidence
from update_docx import update_questionnaire_with_answers

# 1. Load questionnaire
with open("downloaded_test.docx", "rb") as f:
    original_bytes = f.read()

questionnaire_text = extract_text(original_bytes, "downloaded_test.docx")

# 2. Load evidence folder
import os
evidence_texts = {}
for fname in os.listdir("evidence"):
    path = os.path.join("evidence", fname)
    with open(path, "rb") as f:
        b = f.read()
    evidence_texts[fname] = extract_text(b, fname)

# 3. Ask GPT
answers_json = ask_questions_with_evidence(questionnaire_text, evidence_texts)
print("GPT Answers JSON:", answers_json)

# 4. Insert answers into DOCX
updated_bytes = update_questionnaire_with_answers(original_bytes, answers_json)

# 5. Save updated DOCX
with open("updated_questionnaire.docx", "wb") as f:
    f.write(updated_bytes)

print("\n✔ Updated file created: updated_questionnaire.docx")
