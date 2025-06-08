import requests
import os
from datetime import datetime
from github import Github

# Kunin ang GitHub token mula sa environment variable
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = "tito1270/News-feed-fores"  # Palitan ito ng username/repo mo

# URL ng Forex Factory XML calendar
FF_URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.xml"

def download_ff_xml():
    print("Downloading Forex Factory XML...")
    response = requests.get(FF_URL)
    if response.status_code == 200:
        return response.content
    else:
        print("Failed to download XML:", response.status_code)
        return None

def update_github_file(content):
    print("Updating GitHub file...")
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(GITHUB_REPO)
    path = "ff_calendar_thisweek.xml"

    try:
        # Try to get the file to update
        contents = repo.get_contents(path)
        repo.update_file(contents.path, f"Update ff_calendar {datetime.now()}", content, contents.sha)
        print("File updated successfully.")
    except Exception as e:
        # If file doesn't exist, create it
        repo.create_file(path, f"Create ff_calendar {datetime.now()}", content)
        print("File created successfully.")

def main():
    xml_content = download_ff_xml()
    if xml_content:
        update_github_file(xml_content.decode("utf-8"))

if __name__ == "__main__":
    main()