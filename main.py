# main.py
import os
from dotenv import load_dotenv
from onedrive_client import OneDriveClient
from extract_file import extract_text
from gpt_autofill import ask_questions_with_evidence
from update_docx import update_questionnaire_with_answers

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
FEDAUTH = os.getenv("FEDAUTH")
RTFA = os.getenv("RTFA")
QUESTION_PATH = os.getenv("QUESTION_PATH")

# Local evidence folder
EVIDENCE_DIR = "evidence"

# Initialize OneDrive Client
client = OneDriveClient(BASE_URL, FEDAUTH, RTFA)

print("\nSTEP 1: Downloading questionnaire from OneDrive...")
client.download_file(QUESTION_PATH, "questionnaire.docx")

# Read downloaded questionnaire
with open("questionnaire.docx", "rb") as f:
    questionnaire_bytes = f.read()

print("STEP 2: Extracting questionnaire text...")
questionnaire_text = extract_text(questionnaire_bytes, "questionnaire.docx")

# Load evidence files
EVIDENCE_PATH = os.getenv("EVIDENCE_PATH")

print("STEP 3: Loading evidence files from OneDrive...")

# List files in evidence folder
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
answers_json = ask_questions_with_evidence(questionnaire_text, evidence_texts)

print("GPT Answers JSON:", answers_json)

print("STEP 5: Inserting answers into the questionnaire...")
updated_bytes = update_questionnaire_with_answers(questionnaire_bytes, answers_json)

# Save local copy
with open("updated_questionnaire.docx", "wb") as f:
    f.write(updated_bytes)

print("Local updated file created: updated_questionnaire.docx")

print("STEP 6: Uploading updated questionnaire back to OneDrive...")
client.upload_file(QUESTION_PATH, updated_bytes)

print("\n🎉 DONE! Your questionnaire in OneDrive has been autofilled successfully.")
