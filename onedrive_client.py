# onedrive_client.py
import requests
from urllib.parse import quote

class OneDriveClient:
    def __init__(self, base_url, fedauth, rtfa):
        """
        base_url example:
        https://g3cyberspace3-my.sharepoint.com/personal/keerthiyat_g3cyberspace_com/
        """
        self.base_url = base_url
        self.cookies = {
            "FedAuth": fedauth,
            "rtFA": rtfa
        }

    def _encode_path(self, server_relative_path):
        return quote(server_relative_path, safe="/()' ")

    def download_file(self, server_relative_path, local_filename):
        """
        Downloads a file from OneDrive
        """
        encoded = self._encode_path(server_relative_path)
        url = f"{self.base_url}_api/web/GetFileByServerRelativeUrl('{encoded}')/$value"

        print(f"Downloading from: {url}")
        response = requests.get(url, cookies=self.cookies, stream=True)

        if response.status_code != 200:
            raise Exception(f"Download failed {response.status_code}: {response.text[:300]}")

        with open(local_filename, "wb") as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)

        print(f"Downloaded -> {local_filename}")
        return True

    def upload_file(self, server_relative_path, file_bytes):
        """
        Uploads updated file BACK to OneDrive.
        Requires RequestDigest.
        """

        # Step 1: Get RequestDigest
        digest_url = f"{self.base_url}_api/contextinfo"
        digest_resp = requests.post(digest_url, cookies=self.cookies)

        if digest_resp.status_code != 200:
            raise Exception(f"Failed to get RequestDigest: {digest_resp.status_code}")

        try:
            digest_value = digest_resp.text.split("<d:FormDigestValue>")[1].split("</d:FormDigestValue>")[0]
        except Exception:
            raise Exception("Failed to parse RequestDigest.")

        # Step 2: Upload file
        encoded = self._encode_path(server_relative_path)
        upload_url = f"{self.base_url}_api/web/GetFileByServerRelativeUrl('{encoded}')/$value"

        headers = {
            "X-HTTP-Method": "PUT",
            "X-RequestDigest": digest_value,
        }

        print(f"Uploading to: {upload_url}")
        response = requests.post(upload_url, headers=headers, cookies=self.cookies, data=file_bytes)

        if response.status_code not in (200, 201, 204):
            raise Exception(f"Upload failed {response.status_code}: {response.text[:300]}")
        
        print("Upload complete.")
        return True
    def list_files(self, folder_relative_path):
        encoded = self._encode_path(folder_relative_path)
    
        url = f"{self.base_url}_api/web/GetFolderByServerRelativeUrl('{encoded}')/Files"
    
        headers = {
            "Accept": "application/json;odata=verbose"
        }
    
        response = requests.get(url, headers=headers, cookies=self.cookies)
    
        if response.status_code != 200:
            raise Exception(
                f"List failed {response.status_code}: {response.text[:300]}"
            )
    
        data = response.json()
        files = [f["ServerRelativeUrl"] for f in data["d"]["results"]]
        return files