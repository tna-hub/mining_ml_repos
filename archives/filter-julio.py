import time
from github import GithubException
from github import Github
import csv

token = '453256b23318ad96b997267727c2c9b2fceea2d7'


def get_rep(ro, lin):
    g = Github(token)
    rate_limit = g.get_rate_limit()
    rep_link = ro[1]
    try:
        rep = rep_link.replace("https://github.com/", "")
        repo = g.get_repo(rep)
        lang = repo.language
        if str(lang).lower() == "python":
            return True
        else:
            print(rep_link + ":  " + str(lang))
            return False
    except GithubException as err:
        if err.status == 404:
            print(err.data['message'])
            return False
        else:
            print("Error occurred on Github")
            err = err.data['message']
            if rate_limit.core.remaining == 0:
                print(err)
                print("Request limit reached at line " + str(lin) + ". Wait 500 seconds")
                time.sleep(500)
                get_rep(ro, lin)
            # return False
    except Exception as err:
        print("Another exception  occurred at line " + str(lin) + ". Wait 500 seconds")
        print(err)
        time.sleep(500)
        get_rep(ro, lin)


lines = 0
with open('data/repos-julio.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        lines += 1
        if get_rep(row, lines):
            with open('data/filtered-julio.csv', mode='a+') as output:
                output_writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                output_writer.writerow(row)