import json
import requests
import os

# Liste over kilder
source_url = "https://raw.githubusercontent.com/0belous/Jellyfin-Universal-Plugin-Repo/master/manifest.json"

print(f"Starter manifest-bygning i: {os.getcwd()}")

try:
    response = requests.get(source_url, timeout=15)
    data = response.json()
    
    # Skriv direkte til manifest.json i roden af repository
    with open("manifest.json", "w") as f:
        json.dump(data, f, indent=2)
    
    # Tjek om filen faktisk blev oprettet
    if os.path.exists("manifest.json"):
        print("Succes: manifest.json blev oprettet/opdateret.")
    
except Exception as e:
    print(f"Fejl: {e}")
    
