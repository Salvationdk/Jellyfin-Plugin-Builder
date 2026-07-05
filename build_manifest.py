import json
import requests
import re

# URL til README-filen fra Awesome Jellyfin
README_URL = "https://raw.githubusercontent.com/awesome-jellyfin/awesome-jellyfin/master/README.md"

def get_plugins():
    plugins = []
    # Vi starter med det sikre universelle repo
    manifests = ["https://raw.githubusercontent.com/0belous/Jellyfin-Universal-Plugin-Repo/master/manifest.json"]
    
    # Hent README
    response = requests.get(README_URL)
    # Find alle links der ligner plugin-repos (f.eks. https://github.com/niels-b/IntroSkipper)
    links = re.findall(r'https://github\.com/([\w-]+/[\w-]+)', response.text)
    
    for repo in set(links):
        if "jellyfin-" in repo.lower():
            # Prøv at finde manifest i master eller main
            for branch in ["master", "main"]:
                url = f"https://raw.githubusercontent.com/{repo}/{branch}/manifest.json"
                if requests.get(url, timeout=5).status_code == 200:
                    manifests.append(url)
                    break
    return manifests

combined = {"packages": []}
for url in get_plugins():
    try:
        data = requests.get(url).json()
        if "packages" in data:
            combined["packages"].extend(data["packages"])
    except:
        continue

with open("manifest.json", "w") as f:
    json.dump(combined, f, indent=2)
