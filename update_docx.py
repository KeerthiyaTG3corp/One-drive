# update_docx.py
from docx import Document
import io

def update_questionnaire_with_answers(original_doc_bytes, answers_json):
    """
    Updates answers directly inside the questionnaire table.

    Assumes table columns:
    0 = Question
    1 = Description / Clarification
    2 = Response Type
    3 = Answer (added if missing)
    """

    doc = Document(io.BytesIO(original_doc_bytes))

    if not doc.tables:
        raise Exception("No tables found in questionnaire")

    table = doc.tables[0]

    answers_map = {
        a["question_index"]: a["answer"]
        for a in answers_json.get("answers", [])
    }

    # 🔹 Ensure Answer column exists
    current_cols = len(table.columns)
    if current_cols < 4:
        table.add_column(table.columns[0].width)

        # Set header text
        table.rows[0].cells[3].text = "Answer"

    question_index = 0

    for row_idx, row in enumerate(table.rows):
        if row_idx == 0:
            continue  # skip header row

        question_index += 1
        answer = answers_map.get(question_index, "Not found in source")

        # Safe write
        row.cells[3].text = answer

    out_stream = io.BytesIO()
    doc.save(out_stream)
    return out_stream.getvalue()
