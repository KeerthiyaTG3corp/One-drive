from dotenv import load_dotenv
import os
from onedrive_client import OneDriveClient

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
FEDAUTH = os.getenv("FEDAUTH")
RTFA = os.getenv("RTFA")
EVIDENCE_PATH = os.getenv("EVIDENCE_PATH")

client = OneDriveClient(BASE_URL, FEDAUTH, RTFA)

print("Listing files in:", EVIDENCE_PATH)
files = client.list_files(EVIDENCE_PATH)
print("Files found:", files)
