import json
import requests
import os

# Liste over kilder
urls = [
    "https://raw.githubusercontent.com/0belous/Jellyfin-Universal-Plugin-Repo/master/manifest.json"
]

combined = {"packages": []}

for url in urls:
    try:
        response = requests.get(url, timeout=10).json()
        if "packages" in response:
            combined["packages"].extend(response["packages"])
    except Exception as e:
        print(f"Fejl ved {url}: {e}")

# Sikr at vi skriver til den aktuelle mappe
output_path = os.path.join(os.getcwd(), "manifest.json")
with open(output_path, "w") as f:
    json.dump(combined, f, indent=2)

print(f"Manifest gemt til: {output_path}")
