# test_gpt_autofill.py
import os
from dotenv import load_dotenv
from extract_file import extract_text

load_dotenv()

# Ensure you have 'downloaded_docx_test.docx' for questionnaire and evidence files in 'evidence/' folder
QUESTION_FILENAME = "downloaded_test.docx"
EVIDENCE_DIR = "evidence"  # put some .docx/.pdf files here

# Read questionnaire
with open(QUESTION_FILENAME, "rb") as f:
    q_bytes = f.read()
questionnaire_text = extract_text(q_bytes, QUESTION_FILENAME)

# Read and extract all evidence files in folder
evidence_texts = {}
for fname in os.listdir(EVIDENCE_DIR):
    path = os.path.join(EVIDENCE_DIR, fname)
    if not os.path.isfile(path):
        continue
    with open(path, "rb") as f:
        b = f.read()
    txt = extract_text(b, fname)
    evidence_texts[fname] = txt

from gpt_autofill import ask_questions_with_evidence

result = ask_questions_with_evidence(questionnaire_text, evidence_texts)

print("\nGPT Result:")
print(result)

