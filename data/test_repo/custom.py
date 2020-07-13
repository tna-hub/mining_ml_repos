from numpy import loadtxt as lt
import numpy as np


class CustomClassLoadFile1:
    def __init__(self, file, mode):
        self.file = file
        with open(self.file, mode):
            pass

    a = 'constant1'
    c = a

    def custom_func_load_file_in_class(self):
        x = lt(fname='../data/test_datafile.csv')


def custom_func_load_file(self):
    y = lt(fname='../data/test_datafile.csv')


class CustomClassLoadFile2:
    def __init__(self, file, mode):
        self.file = file
        np.loadtxt(file, mode)


b = 'constant1' + 'constant2' + 'constant3'
c = b + 'fuck you'
