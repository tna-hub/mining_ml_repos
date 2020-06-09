from objects import *
from pprint import pprint
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
import configparser

Base.prepare(engine, reflect=True)

config = configparser.ConfigParser(inline_comment_prefixes="#")
config.read('data/config.ini')

min_lift= config['rq1']['min_lift']
min_support = config['rq1']['min_support']
min_confidence = config['rq1']['min_confidence']

modules = []


def do_add(s, x):
    length = len(s)
    s.add(x)
    return len(s) != length


def set_mods():
    for i in range(2, 5):
        repo_mods = set()
        for file in session.query(Element).filter(Element.repo_id == i,
                                                  Element.is_code_file == True).all():
            imports = file.imports
            if imports is not None:
                for mod in imports.split(','):
                    if mod != '':
                        do_add(repo_mods, mod)
        if len(repo_mods) > 0:
            print(len(repo_mods), 'unique modules in repository', i)
            modules.append(list(repo_mods))
    return modules


dataset = set_mods()
pprint(dataset)

te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)
df = pd.DataFrame(te_ary, columns=te.columns_)
print(df)

frequent_itemsets = apriori(df, min_support=0.6, use_colnames=True)
frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
print(frequent_itemsets[(frequent_itemsets['length'] == 1) &
                        (frequent_itemsets['support'] >= 0.8)])
