import numpy as np
from code.Instance import *

class ExtractSolution:
    def __init__(self, filename: str, path: str):
        self.__data: str = open(path, 'r').readlines()
        self.name: str = filename.split("_")[0] + "_" + "_".join(str(k) for k in path.split("_")[1:])
        self.m : int = int(self.name.split("_")[2])
        self.n : int = int(self.name.split("_")[3])
        self.fo: int = int(self.__data[4].split("=")[1])
        self.sequence : np.ndarray(self.n, dtype=int)
        self.size_each_m: np.ndarray(self.m, dtype=int)
        self.__extract_sequence_jobs__()

    def __extract_sequence_jobs__(self) -> np.ndarray:
        
        jobs = []
        each = np.ndarray(self.m, dtype=int)
        for i in range(self.m):
            line = (i * 4) + 7
            x = [int(i) - 1 for i in self.__data[line].split("-") if i.isdigit() and int(i) <= self.n ]
            each[i] = len(x)
            jobs.extend(x)
        self.sequence = jobs
        self.size_each_m = each
