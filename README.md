# Forti-Backup

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

"Forti-Backup" is a backup script launched by Jenkins to save the configuration of the FortiGate and send the backup file into another server.

## Requirements

- Python 3.6 or higher
- Bash 4.4 or later
- FortiGate with REST API enabled
- Remote server with SSH access for storing the backups
- Jenkins (optional, for automation)


# Installation

You can either clone the repository and run the script locally.
```Bash
git clone https://github.com/ImNotIzunia/Forti-Backup.git

cd Forti-Backup
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
- **FORTI_NAME** : The name of your FortiGate
- **FORTI_IP** : The IP of your FortiGate
- **FORTI_TOKEN**: The Token given after the creation of the REST API Account

**Make sure the token you will create in the FortiGate as the least privilege, as a security reason.**

- **SERVER_IP** : The IP of the remote server used as a storage
- **SERVER_FOLDER** : The path to the storage folder
- **SERVER_USER** : The user used for the connection to the remote server
- **SERVER_KEY** : The passkey of the private key for a secure connection

For the Jenkins integration, make sure that the server and runner can just both the repository, FortiGate and remote server location.

For the execution, you can either do it manually or setup a cycle with Jenkins (1 per week or month, as you wish).

```Bash
# Every month at 2AM
0 2 1 * *
```


## Contribution

This is a personal project maintained by a single contributor.

All issues and pull requests are welcome. Please keep security and stability in mind when contributing.

You can also support the project by offering me a coffee !

<div align="center">

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/imnotizunia)
