import json
import requests
import re
from bs4 import BeautifulSoup

# URL til Awesome Jellyfin (hvor vi henter listen fra)
AWESOME_JELLYFIN_URL = "https://github.com/awesome-jellyfin/awesome-jellyfin"
# Dette er et eksempel på et plugin, vi VED virker
PLUGIN_REPO = "https://raw.githubusercontent.com/0belous/Jellyfin-Universal-Plugin-Repo/master/manifest.json"

def get_manifests():
    manifests = [PLUGIN_REPO] # Vi starter altid med det sikre repository
    
    # Hent Awesome Jellyfin siden
    try:
        page = requests.get(AWESOME_JELLYFIN_URL)
        soup = BeautifulSoup(page.text, 'html.parser')
        
        # Find alle links der ligner plugin-repos (dette er et forenklet eksempel)
        for link in soup.find_all('a', href=True):
            if "github.com" in link['href'] and "/jellyfin-" in link['href']:
                # Vi antager her en standard-struktur for manifest-filer
                manifest_url = f"{link['href'].replace('github.com', 'raw.githubusercontent.com')}/master/manifest.json"
                manifests.append(manifest_url)
    except Exception as e:
        print(f"Kunne ikke scrape: {e}")
        
    return manifests

# [Koden fortsætter med at samle JSON-data fra alle fundne links...]
