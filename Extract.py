import numpy as np

class Extract:
    def __init__(self, file: str):
        self.__data = self.__read_file__(file)
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
        str_times = ' '.join(str(i) for i in self.__data[2: 2 + self.__J])
        times = [int(i) for i in str_times.split() if i.isdigit()]
        return np.array(times)
    
    def __extract_S__(self):
        # depois da 2 + n jobs + machines (zeros) até  total de linhas - (2 + n jobs + machines) tempos de setup
        jm = self.__J + self.__M
        str_setups = ' '.join(str(i) for i in self.__data[2 + jm: len(self.__data) - 2 + jm])
        setups_1_dim = [int(i) for i in str_setups.split() if i.isdigit()]
        setups_matrix = [setups_1_dim[i::jm] for i in range(jm)]
        return np.array(setups_matrix)

    
    def to_string(self):
        print(f"M: {self.__M}\nJ: {self.__J}\nT: {self.__T}\nS: {self.__S}")
     







    def __read_file__(self, file):

         # gera um vetor com conteudo de cada linha em cada posição
        data = open(file, 'r').readlines()

        return data
    
        