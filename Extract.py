import numpy as np


class Extract:
    def __init__(self, path_file: str):
        self.__data = self.__read_file__(path_file)
        self.__M = self.__extract_M__()
        self.__J = self.__extract_J__()
        self.__T = self.__extract_T__()
        self.__S = self.__extract_S__()

    def __extract_M__(self) -> int:
        return int(self.__data[0])

    def __extract_J__(self) -> int:
        return int(self.__data[1])

    def __extract_T__(self) -> np.array:
        # segunda linha em diante até linha 2 + quantidade de jobs
        data = self.__data
        text = ' '.join(str(i) for i in data[2: 2 + self.__J])
        times = [int(i) for i in text.split() if i.isdigit()]
        return np.array(times)

    def __extract_S__(self):
        # depois da 2 + n jobs + machines (zeros) até  total de linhas - (2 + n jobs + machines) tempos de setup
        data = self.__data
        jm = self.__J + self.__M
        text = ' '.join(str(i) for i in data[2 + jm: len(data) - 2 + jm])
        array = [int(i) for i in text.split() if i.isdigit()]
        multi_array = [array[i::jm] for i in range(jm)]
        return np.array(multi_array)

    def __read_file__(self, file):
        return open(file, 'r').readlines()

    def to_string(self):
        print(f"M: {self.__M}\nJ: {self.__J}\nT: {self.__T}\nS: {self.__S}")

    def get_M(self) -> int:
        return self.__M

    def get_J(self) -> int:
        return self.__J

    def get_T(self) -> np.array:
        return self.__T

    def get_S(self) -> np.array:
        return self.__S
