import numpy as np


class Extract:
    def __init__(self, path_file: str):
        self.__data = self.__read_file__(path_file)
        self.__m = self.__extract_m__()
        self.__n = self.__extract_n__()
        self.__p = self.__extract_p__()
        self.__s = self.__extract_s__()

    def __extract_m__(self) -> int:
        return int(self.__data[0])

    def __extract_n__(self) -> int:
        return int(self.__data[1])

    def __extract_p__(self) -> np.array:
        # lin 2 até lin 2 + n jobs
        data = self.__data
        text = ' '.join(str(i) for i in data[2: 2 + self.__n])
        times = [int(i) for i in text.split() if i.isdigit()]
        return np.array(times)

    def __extract_s__(self) -> np.ndarray:
        # lin 2 + n jobs + machines até total de lin - (2 + n jobs + machines)
        data = self.__data
        jm = self.__n + self.__m
        text = ' '.join(str(i) for i in data[2 + jm: len(data) - 2 + jm])
        array = [int(i) for i in text.split() if i.isdigit()]
        multi_array = [array[i::jm] for i in range(jm)]
        # inv matriz
        multi_array = np.array(multi_array).T
        # red matrix n jobs + 1
        reduced_border = self.__reduce_border__(multi_array)
        return reduced_border

    def __reduce_border__(self, s: np.ndarray) -> np.ndarray:
        jobs = self.__n
        jm = jobs + self.__m
        # red matriz: col j + 1 até j + m
        s = np.delete(s, slice(jobs + 1, jm), axis=1)
        # red matriz lin j + 1 até j + m
        s = np.delete(s, slice(jobs + 1, jm), axis=0)
        return s

    @staticmethod
    def __read_file__(file):
        return open(file, 'r').readlines()

    def to_string(self):
        print(f"M: {self.__m}\nN: {self.__n}\nP: {self.__p}\nS: {self.__s}")

    def get_m(self) -> int:
        return self.__m

    def get_p(self) -> np.ndarray:
        return self.__p

    def get_s(self) -> np.ndarray:
        return self.__s
