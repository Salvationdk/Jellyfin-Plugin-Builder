import json
import requests
import re
from bs4 import BeautifulSoup

AWESOME_URL = "https://github.com/awesome-jellyfin/awesome-jellyfin"

def get_repo_links():
    repos = set()
    try:
        response = requests.get(AWESOME_URL, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find alle links i README'en
        for a in soup.select('article a[href]'):
            href = a['href']
            # Filtrer for at finde GitHub repo links (excl. subpages)
            match = re.search(r'https://github\.com/([\w-]+/[\w-]+)', href)
            if match:
                repos.add(match.group(1))
    except Exception as e:
        print(f"Scraping fejl: {e}")
    return repos

def build_manifest():
    final_manifest = {"packages": []}
    repo_list = get_repo_links()
    
    print(f"Fandt {len(repo_list)} repositories. Starter validering...")

    for repo in repo_list:
        # Tjek de to mest almindelige steder for et manifest
        for branch in ["master", "main"]:
            url = f"https://raw.githubusercontent.com/{repo}/{branch}/manifest.json"
            try:
                resp = requests.get(url, timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    if "packages" in data:
                        final_manifest["packages"].extend(data["packages"])
                        print(f"Fandt plugin i: {repo}")
                        break
            except:
                continue
                
    with open("manifest.json", "w") as f:
        json.dump(final_manifest, f, indent=2)

build_manifest()
