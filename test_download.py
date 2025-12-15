import os
import requests
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
FEDAUTH = os.getenv("FEDAUTH")
RTFA = os.getenv("RTFA")
QUESTION_PATH = os.getenv("QUESTION_PATH")  # PDF path

cookies = {
    "FedAuth": FEDAUTH,
    "rtFA": RTFA
}

# Encode server-relative path safely
encoded_path = quote(QUESTION_PATH, safe="/'() ")

url = f"{BASE_URL}_api/web/GetFileByServerRelativeUrl('{encoded_path}')/$value"

print("Testing download from:", url)

response = requests.get(url, cookies=cookies, stream=True)

print("Status code:", response.status_code)

if response.status_code == 200:
    with open("downloaded_test.docx", "wb") as f:
        for chunk in response.iter_content(8192):
            f.write(chunk)
    print("SUCCESS: File downloaded as downloaded_test.docx")
else:
    print("ERROR:", response.text[:300])
