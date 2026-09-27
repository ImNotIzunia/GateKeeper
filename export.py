import os
import requests
import urllib3
from dotenv import load_dotenv

load_dotenv()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ip = os.getenv("FORTI_IP")
token = os.getenv("FORTI_TOKEN")

output = "backup.conf"
url  = f"https://{ip}/api/v2/monitor/system/config/backup?scope=global"


response = requests.get(
    url, headers={"Authorization": f"Bearer {token}"},
    verify=False
)

with open(output, "wb") as f:
    f.write(response.content)

