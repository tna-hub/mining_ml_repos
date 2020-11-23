import os

from git import Git


def load():
    with open("test_saner.csv") as f:
        i = 1
        for line in f.readlines():
            print(line)
            line = line.replace('\n', '')
            name = str(i) + '_' + line.split('/')[-1].replace('\n', '')
            os.system(f'git clone {line} {name}')
            i += 1

print([name for name in os.listdir(".") if os.path.isdir(name)])