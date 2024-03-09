import requests
import os
import sys 
from files import dir_path, move_file 

if sys.platform.startswith('win'):
    CURRENT_OS = 'win'
elif 'linux' in sys.platform:
    CURRENT_OS = 'linux'
elif sys.platform == 'darwin':
    CURRENT_OS = 'osx'

def get_artifacts():
    artifacts_url = "https://api.github.com/repos/ikemen-engine/Ikemen-GO/actions/artifacts"
    headers = {"Accept": "application/vnd.github+json"}
    response = requests.get(artifacts_url, headers=headers)
    return response.json()

def show_branches():
    branches_url = "https://api.github.com/repos/ikemen-engine/Ikemen-GO/branches"
    headers = {"Accept": "application/vnd.github+json"}
    response = requests.get(branches_url, headers=headers)
    branch_data = response.json()
    branch_list = []
    for data in branch_data:
        branch_list.append(data["name"])
    return branch_list

def download_branch(branch):
    branch_download_url = "https://api.github.com/repos/ikemen-engine/Ikemen-GO/zipball/" + branch
    headers = {"Accept":"application/json"}
    response = requests.get(branch_download_url, headers=headers)
    open('output.zip', 'wb').write(response.content)

def download_release(progress=None, directory=dir_path):
    latest_request_url ="https://api.github.com/repos/ikemen-engine/Ikemen-GO/releases/latest"
    response = requests.get(latest_request_url)
    json = response.json()
    name = json["name"]
    assets = json["assets"]
    for asset in assets:
        if CURRENT_OS not in asset["name"]:
            continue
        with requests.get(asset["url"],stream=True, allow_redirects=True, headers={'Accept':"application/octet-stream"}) as r:
            total = int(r.headers.get('content-length', 0))
            count = 0
            with open(asset["name"], 'wb') as file:
                for data in r.iter_content(chunk_size=65536):
                    size = file.write(data)
                    count += size
                    progress.update(count/total)
            progress.completed()
            move_file(asset["name"], directory)
