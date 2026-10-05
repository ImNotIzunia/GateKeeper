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

    url = f"https://{ip}:8443/api/v2/monitor/system/config/backup"

    try:
        response = requests.post(
            url,
            headers={"Authorization": f"Bearer {token}"},
            json={
                "destination": "file",
                "scope": "global",
                "password_mask": False,
                "file_format": "fos"
            },
            verify=False,
            timeout=60
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
        print(f"Error : {e}")

