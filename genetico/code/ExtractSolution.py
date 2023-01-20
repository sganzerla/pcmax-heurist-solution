import numpy as np
from optparse import OptionParser
import os

from code.Instance import *

class ExtractSolution:
    def __init__(self, path_file: str):
        self.fo: int
        self.sequence : np.ndarray(10, dtype=int)
        self.size_each_m: np.ndarray(2, dtype=int)
        



