import json
import requests
import re

README_URL = "https://raw.githubusercontent.com/awesome-jellyfin/awesome-jellyfin/master/README.md"

def scrape_awesome_jellyfin():
    # 1. Hent hele README-filen som tekst
    response = requests.get(README_URL)
    text = response.text
    
    # 2. Find alle GitHub-links der ligner plugins
    # Den finder alle links der indeholder 'github.com' og 'jellyfin-plugin-'
    raw_links = re.findall(r'https://github\.com/([\w-]+/[\w-]+)', text)
    
    # Filtrer kun dem der har 'plugin' i navnet
    plugin_repos = [repo for repo in set(raw_links) if "plugin" in repo.lower()]
    
    manifests = []
    print(f"Fandt {len(plugin_repos)} potentielle plugin-repos.")

    # 3. Tjek hver repo for en manifest.json
    for repo in plugin_repos:
        for branch in ["master", "main"]:
            url = f"https://raw.githubusercontent.com/{repo}/{branch}/manifest.json"
            try:
                # Tjek om filen eksisterer
                check = requests.head(url, timeout=5)
                if check.status_code == 200:
                    manifests.append(url)
                    print(f"Fundet manifest i: {repo}")
                    break
            except:
                continue
    return manifests

# Byg det samlede manifest
combined = {"packages": []}
for url in scrape_awesome_jellyfin():
    try:
        data = requests.get(url, timeout=10).json()
        if "packages" in data:
            combined["packages"].extend(data["packages"])
    except:
        continue

with open("manifest.json", "w") as f:
    json.dump(combined, f, indent=2)
    
