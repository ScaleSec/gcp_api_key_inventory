# Inventory Your GCP API Keys

[![GitHub Super-Linter](https://github.com/ScaleSec/gcp_api_key_inventory/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/marketplace/actions/super-linter)


This script will inventory your entire GCP Organization's API keys and create two files: `key_dump.json` and `keys.csv`. You can read the blog related to this repository [here](https://scalesec.com/blog/inventory-your-gcp-api-keys/).

## Prerequisites
- Python3
- The following GCP roles on the Organization level:
   - `API Keys Viewer`
   - `Organization Administrator`

## Usage

1. Clone the repository locally.

2. Create your virtual environment.
```
python3 -m venv $path_to_environment
```
3. Activate your environment
```
source $path_to_environment/bin/activate
```
4. Change directories into the newly cloned repo.

5. Install the required python packages.
```
pip install -r requirements.txt
```
6. Execute the script.
```
python3 apiInventory.py
```
7. Two files will be created:
- `key_dump.json`
- `keys.csv`

## Feedback

Feedback is welcome and encouraged via a GitHub issue. Please open an issue for any bugs, feature requests, or general improvements you would like to see. Thank you in advance!
