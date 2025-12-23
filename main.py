# main.py
import os
import time
from dotenv import load_dotenv
from onedrive_client import OneDriveClient
from extract_file import extract_text
from gpt_autofill import ask_questions_with_evidence
from update_docx import update_questionnaire_with_answers
from questionnaire_parser import extract_questions

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
FEDAUTH = os.getenv("FEDAUTH")
RTFA = os.getenv("RTFA")
QUESTION_PATH = os.getenv("QUESTION_PATH")
EVIDENCE_PATH = os.getenv("EVIDENCE_PATH")

client = OneDriveClient(BASE_URL, FEDAUTH, RTFA)

print("\nSTEP 1: Downloading questionnaire from OneDrive...")
client.download_file(QUESTION_PATH, "Questionnaire.docx")

with open("Questionnaire.docx", "rb") as f:
    questionnaire_bytes = f.read()

print("STEP 2: Extracting questions from questionnaire...")
questions = extract_questions(questionnaire_bytes)
print(f"✔ Extracted {len(questions)} questions")

print("STEP 3: Loading evidence files from OneDrive...")
file_paths = client.list_files(EVIDENCE_PATH)

evidence_texts = {}

for file_path in file_paths:
    local_name = file_path.split("/")[-1]
    print(f"Downloading evidence: {local_name}")

    client.download_file(file_path, local_name)

    with open(local_name, "rb") as f:
        b = f.read()

    evidence_texts[local_name] = extract_text(b, local_name)

print("STEP 4: Asking GPT to autofill answers using ONLY the evidence...")

all_answers = {"answers": []}
BATCH_SIZE = 4   # Reduced to avoid rate limits

for i in range(0, len(questions), BATCH_SIZE):
    batch = questions[i:i+BATCH_SIZE]
    print(f"→ Processing questions {i+1} to {i+len(batch)}")

    result = ask_questions_with_evidence(batch, evidence_texts)
    all_answers["answers"].extend(result.get("answers", []))

    # Sleep to avoid rate limits
    if i + BATCH_SIZE < len(questions):
        print("Sleeping 10 seconds to avoid rate limits...")
        time.sleep(10)

answers_json = all_answers
print("✔ TOTAL answers collected:", len(answers_json["answers"]))

print("STEP 5: Inserting answers into the questionnaire...")
updated_bytes = update_questionnaire_with_answers(questionnaire_bytes, answers_json)

with open("updated_questionnaire.docx", "wb") as f:
    f.write(updated_bytes)

print("STEP 6: Uploading updated questionnaire back to OneDrive...")
updated_path = QUESTION_PATH.replace(".docx", "_AUTOFILLED.docx")
folder_path = os.path.dirname(QUESTION_PATH)
new_filename = os.path.basename(updated_path)

client.upload_new_file(folder_path, new_filename, updated_bytes)


print("\n🎉 DONE! Your questionnaire has been fully autofilled.")
