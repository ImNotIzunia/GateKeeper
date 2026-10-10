# GateKeeper

![fortigate](https://img.shields.io/badge/FortiGate-Backup-blue.svg)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3-3776AB?logo=python)
![Bash](https://img.shields.io/badge/Bash-script-4EAA25?logo=gnubash&logoColor=white)
![Jenkins](https://img.shields.io/badge/Jenkins-Pipeline-D24939?logo=jenkins&logoColor=white)

GateKeeper is a backup script launched by Jenkins to save the configuration of the FortiGate and send the backup file into another server.


---
 
## Table of contents
 
1. [How it works](#how-it-works)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Security](#security)
6. [Contribution](#contribution)

---



## How it works
 
```
┌──────────┐   Jenkins    ┌────────────┐   REST API (GET)   ┌───────────┐
│   Git    │ ───────────► │ export.py  │ ─────────────────► │ FortiGate │
└──────────┘              └─────┬──────┘                    └───────────┘
                                │ backup/<name>.conf
                                ▼
                          ┌───────────┐   SSH/SCP (key + passphrase)   ┌────────────────┐
                          │ copy.sh   │ ─────────────────────────────► │ Storage server │
                          └───────────┘                                └────────────────┘
```
 
The Jenkins pipeline (`Jenkinsfile`) runs three stages:
 
1. **Install Dependencies**: creates a Python virtual environment and installs `requirements.txt`.
2. **Export Data**: runs `export.py`, which downloads each FortiGate configuration into `backup/`.
3. **Upload to storage server**: runs `copy.sh`, which creates `year/month` on the remote server and uploads the files.


## Requirements

**Jenkins agent**
- Python 3 with `venv`: `sudo apt-get install -y python3 python3-pip python3-venv`
- SSH client: `openssh-client` (version ≥ 8.4 recommended for `SSH_ASKPASS_REQUIRE`)
- Network access to port **443** of the FortiGates

**FortiGate**
- A **REST API** administrator with an API token
- Administrator profile with at least read access to the system configuration
- **Trusted Hosts**: the Jenkins agent IP must be allowed
- Tested with **FortiOS 6.2.15**

**Storage server**
- A dedicated user, with Jenkins' public key in `~/.ssh/authorized_keys`
- Write access to the root folder


# Installation

You can either clone the repository and run the script locally.
```Bash
git clone https://github.com/ImNotIzunia/GateKeeper.git

cd GateKeeper
pip install -r requirements.txt
chmod +x copy.sh

python export.py
./copy.sh
```

You can also use it in Jenkins, by creating a new pipeline. The Jenkinsfile is already included in the repository, you just need to configure the parameters of the pipeline.


## Usage

You can have multiple FortiGate included in the backup, you juste need to add other entries in the `JSON` file :
```JSON
[
  {
      "name": "FORTI_NAME_XXX",
      "ip": "FORTI_IP_XXX",
      "token": "FORTI_TOKEN_XXX"
  },
  {
      "name": "FORTI_NAME_XXX",
      "ip": "FORTI_IP_XXX",
      "token": "FORTI_TOKEN_XXX"
  }
]
```
Don't forget to ajust the `.env` file or `Jenkins` attributes to match your JSON configuration.

For the automation, you have to setup the `Jenkins Pipeline` with the following credentials (similar to the `.env` ) :

**Make sure the token you will create in the FortiGate as the least privilege, as a security reason.**

| Name | Default value |
|---|---|
| `FORTI_NAME` | Device name (used to name the `.conf` file) |
| `FORTI_IP` | FortiGate IP address |
| `FORTI_TOKEN` | API administrator token |
| `REMOTE_HOST` | Storage server address |
| `REMOTE_BASE_DIR` | Remote root folder (e.g. `/data/archives`) |

For the Jenkins integration, make sure that the server and runner can just both the repository, FortiGate and remote server location.

> Do not declare a `parameters { ... }` block in the `Jenkinsfile`: it would override the job configuration and put the values in Git.

For the execution, you can either do it manually or setup a cycle with Jenkins (1 per week or month, as you wish).

```Bash
# Every month at 2AM
0 2 1 * *
```


## Security
 
- **Backups contain secrets** (VPN PSKs, password hashes, etc.). Restrict permissions on the storage folder (`chmod 700` or `750`) and access to the server.

- **Limit permissions on the job**: anyone with the *Configure* permission can change the parameters, and a Jenkins administrator can decrypt their values.
- **Keep a copy of the values** in a password manager: if the job is deleted or recreated, everything has to be entered again.
- The **FortiGate API token** should be restricted to the necessary *Trusted Hosts* and a read-only profile.
- The `Jenkinsfile` only contains credential **IDs**, never their values.

- `export.py` uses `verify=False` (self-signed FortiGate certificate). To harden this, install a valid certificate on the FortiGate and enable verification.



## Contribution

This is a personal project maintained by a single contributor.

All issues and pull requests are welcome. Please keep security and stability in mind when contributing.

You can also support the project by offering me a coffee !

<div align="center">

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/imnotizunia)
