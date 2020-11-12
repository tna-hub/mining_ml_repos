import csv

# import PyGithub
import time
import traceback

from github import Github, GithubException

g = Github("d8d97e7ed5e531618033400d120b9ff3244b0071")


def get_data(link):
    name = link.replace('https://github.com/', '')
    lang = None
    nb_commits = None
    try:
        repo = g.get_repo(name)
        lang = repo.language
        nb_commits = repo.get_commits().totalCount
    except GithubException as error:
        if error.data["message"].startswith("API rate limit exceeded"):
            print("Request limit reached at line, Wait 500 seconds")
            time.sleep(500)
            return get_data(link)
        else:
            print('Unknown Exception not known from github', error.status, error.data)
    except Exception as e:
        print(traceback.format_exc())
    return lang, nb_commits

with open("sota_arxiv_link_github.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            line_count += 1
            language, commits = get_data(row[0])
            if language is None or commits is None:
                pass
            else:
                if language == "Python":
                    print('Found python repo', row[0])
                    with open('sota_arxiv_python.csv', 'a+') as f:
                        f.write(f'{row[0]},{language},{commits}\n')