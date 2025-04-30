import base64
import json
import requests
from datetime import datetime

# GitHub repo settings
GITHUB_USER = "87712"
REPO_NAME = "GeoRSS_Feeds"
FILE_NAME = "live_feed.xml"
BRANCH = "main"
GITHUB_TOKEN = "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"
# GitHub API endpoint
url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/contents/{FILE_NAME}"

# Read and encode the file content
with open(FILE_NAME, "rb") as file:
    content = base64.b64encode(file.read()).decode("utf-8")

# Set request headers
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

# Check if file exists to get its SHA
response = requests.get(url, headers=headers)
sha = response.json().get("sha", None)

# Prepare commit payload
data = {
    "message": f"Auto-update GeoRSS at {datetime.utcnow().isoformat()}",
    "content": content,
    "branch": BRANCH,
}

if sha:
    data["sha"] = sha

# Upload the file
put_response = requests.put(url, headers=headers, data=json.dumps(data))

# Status message
if put_response.status_code in [200, 201]:
    print("✅ GeoRSS file successfully updated on GitHub!")
else:
    print("❌ Failed to upload file.")
    print("Status Code:", put_response.status_code)
    print(put_response.json())
