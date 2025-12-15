import tempfile
import fitz               # PyMuPDF for PDF
from docx import Document # for DOCX

def extract_text_from_pdf(pdf_bytes):
    tf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tf.write(pdf_bytes)
    tf.flush()
    tf.close()

    doc = fitz.open(tf.name)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

def extract_text_from_docx(docx_bytes):
    tf = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    tf.write(docx_bytes)
    tf.flush()
    tf.close()

    doc = Document(tf.name)
    text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    return text.strip()

def extract_text(file_bytes, filename):
    """
    Automatically detects file type by extension.
    Supports PDF and DOCX.
    """
    filename = filename.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)

    elif filename.endswith(".docx"):
        return extract_text_from_docx(file_bytes)

    else:
        raise Exception("Unsupported file type. Only PDF and DOCX are supported.")
