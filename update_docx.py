# update_docx.py
from docx import Document
import io

def update_questionnaire_with_answers(original_doc_bytes, answers_json):
    """
    Rebuilds the questionnaire in sequential order:
    Question
    Description / Clarification
    Answer
    """

    new_doc = Document()

    answers = answers_json.get("answers", [])

    for idx, item in enumerate(answers, start=1):
        # Question
        q_para = new_doc.add_paragraph()
        q_para.add_run("Question:\n").bold = True
        q_para.add_run(item.get("question", ""))

        # Description
        d_para = new_doc.add_paragraph()
        d_para.add_run("\nDescription / Clarification:\n").bold = True
        d_para.add_run(item.get("description", ""))

        # Answer
        a_para = new_doc.add_paragraph()
        a_para.add_run("\nAnswer:\n").bold = True
        a_para.add_run(item.get("answer", "Not found in source"))

        # Spacer between questions
        new_doc.add_paragraph("\n")

    # Save DOCX to bytes
    out = io.BytesIO()
    new_doc.save(out)
    return out.getvalue()
