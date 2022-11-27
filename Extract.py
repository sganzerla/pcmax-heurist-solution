import numpy as np


class Extract:
    def __init__(self, path_file: str):
        self.__data = self.__read_file__(path_file)
        self.__M = self.__extract_M__()
        self.__N = self.__extract_N__()
        self.__P = self.__extract_P__()
        self.__S = self.__extract_S__()

    def __extract_M__(self) -> int:
        return int(self.__data[0])

    def __extract_N__(self) -> int:
        return int(self.__data[1])

    def __extract_P__(self) -> np.array:
        # segunda linha em diante até linha 2 + quantidade de jobs
        data = self.__data
        text = ' '.join(str(i) for i in data[2: 2 + self.__N])
        times = [int(i) for i in text.split() if i.isdigit()]
        return np.array(times)

    def __extract_S__(self):
        # depois da 2 + n jobs + machines (zeros) até  total de linhas - (2 + n jobs + machines) tempos de setup
        data = self.__data
        jm = self.__N + self.__M
        text = ' '.join(str(i) for i in data[2 + jm: len(data) - 2 + jm])
        array = [int(i) for i in text.split() if i.isdigit()]
        multi_array = [array[i::jm] for i in range(jm)]

        # mantem a matrix com n jobs + 1, removendo redundancias
        reduced_border = self.__reduce_border__(multi_array)
        return reduced_border

    def __reduce_border__(self, S: np.array) -> np.array:
        jobs = self.get_N()
        jm = jobs + self.get_M()
        # corte da matriz colunas j + 1 até j + m
        S = np.delete(S, slice(jobs + 1, jm), axis=1)
        # corte da matriz linhas j + 1 até j + m
        S = np.delete(S, slice(jobs + 1, jm), axis=0)
        return S

    def __read_file__(self, file):
        return open(file, 'r').readlines()

    def to_string(self):
        print(f"M: {self.__M}\nN: {self.__N}\nP: {self.__P}\nS: {self.__S}")

    def get_M(self) -> int:
        return self.__M

    def get_N(self) -> int:
        return self.__N

    def get_P(self) -> np.array:
        return self.__P

    def get_S(self) -> np.array:
        return self.__S
