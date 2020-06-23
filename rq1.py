from objects import *
from pprint import pprint
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
import configparser
import csv
import time

Base.prepare(engine, reflect=True)

config = configparser.ConfigParser(inline_comment_prefixes="#")
config.read('data/config.ini')

min_lift = config['rq1']['min_lift']
min_support = config['rq1']['min_support']
min_confidence = config['rq1']['min_confidence']

modules = []


def set_uniq_modules(repo_id):
    uniq_modules = set()
    for file in session.query(Element).filter(Element.repo_id == repo_id,
                                              Element.is_code_file == True).all():
        imports = file.imports
        if imports is not None:
            for module in imports.split(','):
                if module:
                    uniq_modules.add(module)
    nb_uniq_modules = len(uniq_modules)
    if nb_uniq_modules > 0:
        return list(uniq_modules)
    return None


def main():
    start_time = time.time()
    print("=======================Starting to get unique modules and saving to file==========================")
    for repo_id in range(2, 14165):
        uniq_modules = set_uniq_modules(repo_id)
        if uniq_modules is not None:
            print("{}: {} unique repositories. Elapsed time: {:.2f} min".format(repo_id,
                                                                                len(uniq_modules),
                                                                                (time.time() - start_time) / 60))

            with open('data/uniq_modules.csv', 'a+') as f:
                wr = csv.writer(f)
                wr.writerow(uniq_modules)
    print("=======================Finished! Well done!==========================")


if __name__ == "__main__":
    main()
