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
