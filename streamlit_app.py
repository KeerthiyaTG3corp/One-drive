import streamlit as st
import os
import time
from dotenv import load_dotenv
from onedrive_client import OneDriveClient
from extract_file import extract_text
from gpt_autofill import ask_questions_with_evidence
from update_docx import update_questionnaire_with_answers
from questionnaire_parser import extract_questions

def run_autofill_process():
    """Run the questionnaire autofill process"""
    load_dotenv()

    BASE_URL = os.getenv("BASE_URL")
    FEDAUTH = os.getenv("FEDAUTH")
    RTFA = os.getenv("RTFA")
    QUESTION_PATH = os.getenv("QUESTION_PATH")
    EVIDENCE_PATH = os.getenv("EVIDENCE_PATH")

    client = OneDriveClient(BASE_URL, FEDAUTH, RTFA)

    # Progress updates
    progress_bar = st.progress(0)
    status_text = st.empty()

    status_text.text("STEP 1: Downloading questionnaire from OneDrive...")
    client.download_file(QUESTION_PATH, "Questionnaire.docx")
    progress_bar.progress(10)

    with open("Questionnaire.docx", "rb") as f:
        questionnaire_bytes = f.read()

    status_text.text("STEP 2: Extracting questions from questionnaire...")
    questions = extract_questions(questionnaire_bytes)
    st.write(f"✔ Extracted {len(questions)} questions")
    progress_bar.progress(20)

    status_text.text("STEP 3: Loading evidence files from OneDrive...")
    file_paths = client.list_files(EVIDENCE_PATH)

    evidence_texts = {}

    for i, file_path in enumerate(file_paths):
        local_name = file_path.split("/")[-1]
        st.write(f"Downloading evidence: {local_name}")

        client.download_file(file_path, local_name)

        with open(local_name, "rb") as f:
            b = f.read()

        evidence_texts[local_name] = extract_text(b, local_name)
        progress_bar.progress(20 + int(30 * (i+1) / len(file_paths)))

    status_text.text("STEP 4: Asking GPT to autofill answers using ONLY the evidence...")

    all_answers = {"answers": []}
    BATCH_SIZE = 4   # Reduced to avoid rate limits

    for i in range(0, len(questions), BATCH_SIZE):
        batch = questions[i:i+BATCH_SIZE]
        st.write(f"→ Processing questions {i+1} to {i+len(batch)}")

        result = ask_questions_with_evidence(batch, evidence_texts)
        all_answers["answers"].extend(result.get("answers", []))

        # Sleep to avoid rate limits
        if i + BATCH_SIZE < len(questions):
            st.write("Sleeping 10 seconds to avoid rate limits...")
            time.sleep(10)

        progress_bar.progress(50 + int(30 * (i+len(batch)) / len(questions)))

    answers_json = all_answers
    st.write("✔ TOTAL answers collected:", len(answers_json["answers"]))

    status_text.text("STEP 5: Inserting answers into the questionnaire...")
    updated_bytes = update_questionnaire_with_answers(questionnaire_bytes, answers_json)
    progress_bar.progress(85)

    with open("updated_questionnaire.docx", "wb") as f:
        f.write(updated_bytes)

    status_text.text("STEP 6: Uploading updated questionnaire back to OneDrive...")
    updated_path = QUESTION_PATH.replace(".docx", "_AUTOFILLED.docx")
    folder_path = os.path.dirname(QUESTION_PATH)
    new_filename = os.path.basename(updated_path)

    client.upload_new_file(folder_path, new_filename, updated_bytes)
    progress_bar.progress(100)

    status_text.text("🎉 DONE! Your questionnaire has been fully autofilled.")
    st.success("Process completed successfully!")

    # Provide download link for the updated file
    st.download_button(
        label="Download Updated Questionnaire",
        data=updated_bytes,
        file_name="updated_questionnaire.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

def main():
    st.title("Questionnaire Auto-Fill Tool")
    st.markdown("""
    This tool automatically fills out questionnaires using evidence documents stored in OneDrive.
    It uses AI to analyze the evidence and provide accurate answers to questionnaire questions.
    """)

    if st.button("Start Auto-Fill Process", type="primary"):
        try:
            run_autofill_process()
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.exception(e)

if __name__ == "__main__":
    main()