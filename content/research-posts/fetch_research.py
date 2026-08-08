import os
import re
import json
import requests
import argparse
from datetime import datetime

# Configuration
REPO = "PaloAltoNetworks/Unit42-timely-threat-intel"
SEARCH_QUERY = f"shuang repo:{REPO}"
OUTPUT_DIR = "content/research-posts"

def fetch_search_results(token):
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"token {token}" if token else None
    }
    url = f"https://api.github.com/search/code?q={SEARCH_QUERY}"
    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        print("Error: Authentication required. Please provide a GitHub Token.")
        return []
    elif response.status_code != 200:
        print(f"Error fetching search results: {response.status_code} - {response.text}")
        return []

    return response.json().get("items", [])

def parse_file_content(content, html_url):
    # Extract Title and Date from first line or filename
    # Example First Line: 2026-03-23 [MONDAY] Device Code-based OAuth Phishing
    first_line = content.split('\n')[0].strip()
    match = re.match(r'^(\d{4}-\d{2}-\d{2})\s+\[\w+\]\s+(.*)$', first_line)

    if match:
        date_str, title = match.groups()
    else:
        # Fallback to filename pattern: 2026-03-23- Device-Code-based-OAuth-Phishing.txt
        filename = html_url.split('/')[-1]
        match = re.match(r'^(\d{4}-\d{2}-\d{2})-\s*(.*)\.txt$', filename)
        if match:
            date_str, title = match.groups()
            title = title.replace('-', ' ')
        else:
            date_str = datetime.now().strftime("%Y-%m-%d")
            title = "Untitled Research"

    # Extract Summary from NOTES: section
    summary = ""
    notes_match = re.search(r'NOTES:\s*(.*?)(?=DETAILS:|AUTHOR\(S\):|URLS:|INDICATORS:|$)', content, re.DOTALL | re.IGNORECASE)
    if notes_match:
        summary = notes_match.group(1).strip()
        # Clean up summary (remove extra whitespace/newlines)
        summary = re.sub(r'\s+', ' ', summary)

    return {
        "title": title,
        "date": date_str,
        "external_link": html_url,
        "summary": summary
    }

def save_as_markdown(data):
    # Create filename from title
    safe_title = re.sub(r'[^\w\s-]', '', data['title'].lower())
    safe_title = re.sub(r'[-\s]+', '-', safe_title).strip('-')
    file_path = os.path.join(OUTPUT_DIR, f"{safe_title}.md")

    title = json.dumps(data['title'], ensure_ascii=False)
    external_link = json.dumps(data['external_link'], ensure_ascii=False)
    summary = json.dumps(data['summary'], ensure_ascii=False)

    content = f"""---
title: {title}
date: {data['date']}
external_link: {external_link}
summary: {summary}
---

{data['summary']}

[Read the full Unit 42 report and indicators →]({data['external_link']})
"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Saved: {file_path}")

def main():
    parser = argparse.ArgumentParser(description="Fetch research posts from Unit 42 repo.")
    parser.add_argument("--token", help="GitHub Personal Access Token")
    args = parser.parse_args()

    token = args.token or os.environ.get("GITHUB_TOKEN")

    if not token:
        print("Starting without token... Note: GitHub Code Search API usually requires authentication.")

    items = fetch_search_results(token)

    if not items:
        print("No results found or search failed.")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for item in items:
        file_url = item['html_url']
        raw_url = file_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

        print(f"Processing: {item['path']}...")
        response = requests.get(raw_url)
        if response.status_code == 200:
            data = parse_file_content(response.text, file_url)
            save_as_markdown(data)
        else:
            print(f"Failed to fetch raw content for {item['path']}")

if __name__ == "__main__":
    main()
