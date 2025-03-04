import requests
from dotenv import dotenv_values

config = dotenv_values(".env")
github_token = config["github_token"]
user_name = "chandureddy08"
headers = {"Authorization": f"token {github_token}"}

def list_repos(user_name):
    repos = []
    url = f"https://api.github.com/users/{user_name}/repos"
    while url:
        responce = requests.get(url, headers=headers, params={"per_page":100})
        if responce.status_code == 200:
            repos.extend(responce.json())

            if "next" in responce.links:
                url = responce.links["next"]["url"]
            else:
                url = None

        else:
            print("Failed to fetch repositories:",responce.content)
            url = None

    for repo in repos:
        print(repo["name"])


list_repos(user_name)

