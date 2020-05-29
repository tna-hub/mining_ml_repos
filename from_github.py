import time
from github import GithubException
from github import Github, Commit
import configparser

config = configparser.ConfigParser(inline_comment_prefixes="#")
config.read('data/config.ini')

token = config['github']['token']


def download(g, repo, sha):
    try:
        return repo.get_commit(sha=sha)
    except GithubException as error:
        if error.status == 404:
            return None
        else:
            if g.rate_limit.core.remaining < 5:
                print("Request limit reached at line, Wait 500 seconds")
                time.sleep(500)
                return download(g, repo, sha)
            else:
                print('Unknown exception on github', error)
                return None
    except Exception as e:
        print(e)
        return None


import traceback


def get_commit(rep_name, sha) -> Commit:
    g = Github(token)
    rate_limit = g.get_rate_limit()
    try:
        repo = g.get_repo(rep_name)
        return download(g, repo, sha)
    except GithubException as error:
        if error.status == 404:
            return None
        else:
            if rate_limit.core.remaining < 5:
                print("Request limit reached at line, Wait 500 seconds")
                time.sleep(500)
                return get_commit(rep_name, sha)
            else:
                print('Exception not know from github', error)
                return None
    except Exception as e:
        print(traceback.format_exc())
        return None
