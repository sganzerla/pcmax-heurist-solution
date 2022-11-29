import numpy as np


class Instance:
    def __init__(self, M: int, P: np.array, S: np.ndarray):
        self.__M = M
        self.__P = P
        self.__N = len(P)
        self.__S = self.__join_times__(S)

    def __join_times__(self, S: np.array) -> np.ndarray:
        n = self.get_N()
        for i in range(n):
            S[i][0:n] = S[i][0:n] + self.__P[i]
        return S

    def to_string(self):
        print(
            f"M: {self.__M}\nN: {self.__N}\nP: {self.__P}\nS: {self.__S}")

    def get_M(self) -> int:
        return self.__M

    def get_N(self) -> int:
        return self.__N

    def get_P(self, i: int) -> int:
        return self.P[i]

    def get_S(self,i : int, j : int) -> np.ndarray:
        if i == j:
            return 0
        if i >= self.__N:
            return self.__S[self.__N,j]
       
        if j >= self.__N:
            return self.__S[i,self.__N]
             
        return self.__S[i,j]
