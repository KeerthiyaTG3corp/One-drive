from extract_file import extract_text

# Change filename to match your downloaded file
FILENAME = "downloaded_test.pdf"  # or downloaded_test.docx

with open(FILENAME, "rb") as f:
    data = f.read()

text = extract_text(data, FILENAME)

print("---- Extracted Text Preview ----")
print(text[:500])   # preview first 500 chars
