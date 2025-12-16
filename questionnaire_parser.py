from docx import Document
import io

def extract_questions_from_table(docx_bytes):
    """
    Extracts structured questions from a table-based questionnaire DOCX.

    Expected table format:
    | Question | Description / Clarification | Response Type |
    """

    doc = Document(io.BytesIO(docx_bytes))

    if not doc.tables:
        raise Exception("No tables found in questionnaire")

    table = doc.tables[0]  # assume first table contains questions

    questions = []

    for row_index, row in enumerate(table.rows):
        if row_index == 0:
            continue  # skip header row

        question = row.cells[0].text.strip()
        description = row.cells[1].text.strip() if len(row.cells) > 1 else ""
        response_type = row.cells[2].text.strip() if len(row.cells) > 2 else ""

        if question:
            questions.append({
                "question_index": len(questions) + 1,
                "question": question,
                "description": description,
                "response_type": response_type
            })

    return questions
