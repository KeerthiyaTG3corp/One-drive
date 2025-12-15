# update_docx.py
from docx import Document
import io

def update_questionnaire_with_answers(original_doc_bytes, answers_json):
    """
    original_doc_bytes: raw bytes of questionnaire docx
    answers_json: dict returned from GPT, ex:
        { "answers": [ {"question_index":1, "question":"...", "answer":"..."} ] }

    Returns: updated docx bytes
    """

    # Load docx from bytes into source document
    doc_stream = io.BytesIO(original_doc_bytes)
    src = Document(doc_stream)

    # Build a map from question_index -> answer dict
    answers_list = answers_json.get("answers", [])
    answers_map = {a["question_index"]: a for a in answers_list}

    # Create a new document and copy paragraphs, inserting answers after questions
    new_doc = Document()

    question_counter = 0

    for para in src.paragraphs:
        # copy paragraph text with same style
        new_para = new_doc.add_paragraph(para.text)
        try:
            new_para.style = para.style
        except Exception:
            pass

        # detect a question line (simple heuristic: ends with '?')
        if para.text.strip().endswith("?"):
            question_counter += 1
            if question_counter in answers_map:
                answer_text = answers_map[question_counter]["answer"]
                ans_para = new_doc.add_paragraph(f"Answer: {answer_text}")
                # try to apply same style as the question paragraph (if available)
                try:
                    ans_para.style = para.style
                except Exception:
                    pass

    # Save updated DOCX to bytes and return
    out_stream = io.BytesIO()
    new_doc.save(out_stream)
    return out_stream.getvalue()
