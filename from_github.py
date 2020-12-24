import csv
import time
from github import GithubException
from github import Github, Commit
import configparser

config = configparser.ConfigParser(inline_comment_prefixes="#")
config.read('data/config.ini')

token = config['github']['token']


def download(repo, sha):
    try:
        return repo.get_commit(sha=sha)
    except GithubException as error:
        if error.status == 404:
            return None
        elif error.data["message"].startswith("API rate limit exceeded"):
            print("Request limit reached at line, Wait 500 seconds")
            time.sleep(500)
            return download(repo, sha)
        else:
            print('Unknown Exception not known from github', error.status, error.data)
            return None
    except Exception as e:
        print(traceback.format_exc())
        return None


import traceback


def get_commit(rep_name, sha) -> Commit:
    g = Github(token)
    try:
        repo = g.get_repo(rep_name)
        return download(repo, sha)
    except GithubException as error:
        if error.status == 404:
            return None
        elif error.data["message"].startswith("API rate limit exceeded"):
            print("Request limit reached at line, Wait 500 seconds")
            time.sleep(500)
            return get_commit(rep_name, sha)
        else:
            print('Exception from github', error.status, error.data)
            return None
    except Exception as e:
        print(traceback.format_exc())
        return None

def get_size(link):
    g = Github(token)
    try:
        repo = g.get_repo(link)
        return repo.size
    except GithubException as error:
        if error.data["message"].startswith("API rate limit exceeded"):
            print("Request limit reached at line, Wait 500 seconds")
            time.sleep(500)
            return get_size(link)
        else:
            print('Exception from github', error.status, error.data)
            return None
    except Exception as e:
        print(traceback.format_exc())
        return None

with open("./data/datasetv2.csv") as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header row.
    for row in reader:
        print("Getting row", row[0])
        link = row[1].replace("https://github.com/", "")
        size = get_size(link)
        if size is not None:
            with open("./data/repo_size.csv", "a+") as f:
                writer = csv.writer(f)
                row.append(size)
                writer.writerow(row)