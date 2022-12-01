import numpy as np
from Extract import *


class Instance:
    def __init__(self, extr: Extract):
        self.__M = extr.get_M()
        self.__P = extr.get_P()
        self.__N = len(self.__P)
        self.__S = self.__join_times__(extr.get_S())

    def __join_times__(self, S: np.array) -> np.ndarray:
        # soma o tempo das máquina na última linha mas mantem original o setup da última coluna
        n = self.get_N()
        # cria uma lista de indices da matriz sempre com uma linha a mais que coluna
        idx = [(i, j) for i in range(n + 1) for j in range(n)]
        for i, j in idx:
            S[i][j] = S[i][j] + self.__P[j]
        return S

    def to_string(self):
        print(
            f"M: {self.__M}\nN: {self.__N}\nP: {self.__P}\nS: {self.__S}")

    def get_M(self) -> int:
        return self.__M

    def get_N(self) -> int:
        return self.__N

    def get_P(self, i: int) -> int:
        return self.__P[i]

    def get_copy_P(self) -> np.ndarray:
        return self.__P.copy()

    def get_S(self, i: int, j: int) -> np.ndarray:
        if i == j:
            return 0
        if i >= self.__N:
            return self.__S[self.__N, j]

        if j >= self.__N:
            return self.__S[i, self.__N]

        return self.__S[i, j]
