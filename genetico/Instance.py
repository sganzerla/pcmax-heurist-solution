from Extract import *


class Instance:
    def __init__(self, ext: Extract):
        self.__m = ext.get_m()
        self.__p = ext.get_p()
        self.__n = len(self.__p)
        self.__s = self.__join_times__(ext.get_s())

    def __join_times__(self, s: np.ndarray) -> np.ndarray:
        n = self.get_n()
        # matriz n + 1 * n
        idx = [(i, j) for i in range(n + 1) for j in range(n)]
        for i, j in idx:
            s[i][j] = s[i][j] + self.__p[j]
        return s

    def to_string(self):
        print(
            f"M: {self.__m}\nN: {self.__n}\nP: {self.__p}\nS: {self.__s}")

    def get_m(self) -> int:
        return self.__m

    def get_n(self) -> int:
        return self.__n

    def get_p(self, i: int) -> int:
        return self.__p[i]

    def get_p_copy(self) -> np.ndarray:
        return self.__p.copy()

    def get_s(self, i: int, j: int) -> int:
        if i == j:
            return 0
        if i >= self.__n:
            return self.__s[self.__n, j]

        if j >= self.__n:
            return self.__s[i, self.__n]

        return self.__s[i, j]
