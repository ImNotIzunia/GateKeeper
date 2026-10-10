import os
import json
import requests
import urllib3

from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

Path("backup").mkdir(exist_ok=True)

with open("fortigate.json", encoding="utf-8") as fichier:
    forti = json.load(fichier)

errors = []

for f in forti:
    name = os.getenv(f["name"])
    ip = os.getenv(f["ip"])
    token = os.getenv(f["token"])

    if not all([name, ip, token]):
        print(f"Missing Variables: {f}")
        errors.append(f["name"])
        continue

    url = f"https://{ip}/api/v2/monitor/system/config/backup"

    try:
        # FortiOS 6.2 : l'endpoint de backup utilise GET (POST = 405)
        response = requests.get(
            url,
            headers={"Authorization": f"Bearer {token}"},
            params={"destination": "file", "scope": "global"},
            verify=False,
            timeout=60,
        )

        if response.status_code == 200:
            filename = f"backup/{name}.conf"

            with open(filename, "wb") as file:
                file.write(response.content)

            print(f"Backup for {name} saved to {filename}")
        else:
            print(f"{name} : erreur HTTP {response.status_code}")
            print(response.text)
            errors.append(name)

    except requests.exceptions.RequestException as e:
        print(f"Error for {name} : {e}")
        errors.append(name)

if errors:
    print(f"Failed for: {', '.join(errors)}")
    raise SystemExit(1)