import numpy as np
from code.Instance import *

class ExtractSolution:
    def __init__(self, file: str):
        self.data: str = open(file, 'r').readlines()
        self.name: str = file.split("/")[1].split("_")[0] + "_" + "_".join(str(k) for k in file.split("_")[2:])
        self.m : int = int(self.name.split("_")[2])
        self.n : int = int(self.name.split("_")[3])
        self.fo: int = int(self.data[4].split("=")[1])
        self.sequence : np.ndarray = self.get_sequence_jobs()
        self.size_each_m: np.ndarray(2, dtype=int)
        

    def get_sequence_jobs(self) -> np.ndarray:
        
        jobs = []
        each = np.ndarray(self.m, dtype=int)
        for i in range(self.m):
            line = (i * 4) + 7
            x = [int(i) for i in self.data[line].split("-") if i.isdigit() and int(i) <= self.n ]
            each[i] = len(x)
            jobs.extend(x)
        self.sequence = jobs
        self.size_each_m = each
