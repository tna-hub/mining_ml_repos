from pydriller import RepositoryMining as rpm
import collections
import itertools
from git import Repo
import os


dataset = "data/datasetv2.csv"

class datafile:
    def __init__(self, repo, filename):
        self.filename = filename
        self.commits = rpm(repo, filepath=self.filename).traverse_commits()
        self.mod_files = []

        if self.commits is not None:
            self.coms = []
            for commit in self.commits:
                coms_files = []
                for file in commit.modifications:
                    if (file.new_path != self.filename) and (file.old_path != self.filename):
                        coms_files.append(file.new_path)
                self.coms.append(coms_files)
            self.mod_files = self.freq_sorted(itertools.chain.from_iterable(self.coms))
            temp = self.mod_files
            self.mod_files = [tup for tup in self.mod_files if tup[1] != 1]
            self.nb_commits = len(self.coms)

    def freq_sorted(self, iterable, key=None, reverse=False, include_freq=True):
        """Return a list of items from iterable sorted by frequency.

        If include_freq, (item, freq) is returned instead of item.

        key(item) must be hashable, but items need not be.

        *Higher* frequencies are returned first.  Within the same frequency group,
        items are ordered according to key(item).
        """
        if key is None:
            key = lambda x: x

        key_counts = collections.defaultdict(int)
        items = {}
        for n in iterable:
            k = key(n)
            key_counts[k] += 1
            items.setdefault(k, n)

        if include_freq:
            def get_item(k, c):
                return items[k], c
        else:
            def get_item(k, c):
                return items[k]

        return [get_item(k, c) for k, c in
                sorted(key_counts.items(),
                       key=lambda kc: (-kc[1], kc[0]),
                       reverse=reverse)]


class Repository:
    def __init__(self, link, name=None):
        self.name = link.split("/")[-1] if name is None else name
        self.link = link
        self.folders = []
        self.code_files = []
        self.non_code_files = []
        try:
            if not os.path.isdir(self.name):
                Repo.clone_from(link, self.name)
            self.get_infos()
        except Exception as e:
            print(e)

    def get_infos(self):
        # r r: root, d: directory, f: file
        for r, d, f in os.walk(self.name):
            for file in f:
                path = os.path.join(r, file)
                ff = File(path)
                if not (ff.ignore or ff.is_hidden):
                    if ff.extension == ".py":
                        self.code_files.append(path)
                    else:
                        self.non_code_files.append(path)

            for folder in d:
                is_hidden = False
                pat = os.path.join(r, folder)
                for el in pat.split("/"):
                    if el.startswith("."):
                        is_hidden = True
                        break
                if not is_hidden:
                    self.folders.append(pat)


class File:
    def __init__(self, filename):
        self.filename = filename.replace(" ", "").lower()
        self.is_hidden = False
        self.extension = "no"
        if self.filename is not None:
            for data in self.filename.split("/"):
                if data.startswith("."):
                    self.is_hidden = True
                    break
            ext = os.path.splitext(self.filename.replace(" ", ""))[-1].lower()
            self.extension = ext if ext is not None and ext != "" else "no"
        self.ignore = True if ("readme" in self.filename) or ("requirement" in self.filename) or ("setup" in self.filename) else False

    #def is_datafile(self):


def getext(filename):
    ext = os.path.splitext(filename)[-1]
    return ext if ext is not None or ext != "" else "no"

def h1(folder, code):
    return