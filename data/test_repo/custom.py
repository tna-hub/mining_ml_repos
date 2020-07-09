from numpy import loadtxt as lt
import numpy as np


class CustomClassLoadFile1:
    def __init__(self, file, mode):
        self.file = file
        with open(self.file, mode):
            pass

    def custom_func_load_file_in_class(self):
        a = lt(fname='../data/test_datafile.csv')


def custom_func_load_file(self):
    a = lt(fname='../data/test_datafile.csv')


class CustomClassLoadFile2:
    def __init__(self, file, mode):
        self.file = file
        np.loadtxt(file, mode)
