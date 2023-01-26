import numpy as np

class Convert:
    def __init__(self, path: str):
        self.__data = open(path, 'r').readlines()
        self.__m = int(self.__data[0])
        self.__n = int(self.__data[1])
        self.__p: list
        self.__extract_p__()
        self.__s: list
        self.__extract_s__()
        
    def to_string(self):
        print(f"Máquinas: {self.__m}")
        print(f"Tarefas: {self.__n}")
        print(f"Tempo processamento: {self.__p}")
        i = 0
        x = 0
        y = self.__n
        for i in range(self.__n + 1):
            print(f"Tempos preparação iniciando na posição {i}: {self.__s[x:y]}")
            x = y
            y += self.__n
        
    def write_file(self, file: str):
        with open(file, 'w') as w:
            w.write(f"{self.__n} {self.__m}")
            for i in self.__p:                
                w.write(f"\n{i}")
            st = 0
            nd = st
            for i in range(self.__n + 1):
                nd += self.__n 
                x = [k for k in self.__s[st: nd]]
                for j in range(0, self.__n):
                    w.write(f"\n{i} {j+1} {x[j]}")
                st = nd
                   
                
            w.close()
        
        
    
    def __extract_s__(self):
        jm = self.__n + self.__m
        st = jm + 2
        nd = st
        x = []
        for i in range(self.__n + 1):
            nd += jm 
            x.extend([int(i) for i in self.__data[st: nd - 1] if int(i) != 500])
            st = nd
        self.__s = x
        
    def __extract_p__(self) -> list:
        # lin 2 até lin 2 + n jobs
        text = ' '.join(str(i) for i in self.__data[2: 2 + self.__n])
        self.__p = [int(i) for i in text.split() if i.isdigit()]
    


from optparse import OptionParser
 
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-r', '--file', dest="file")
    (opts, _) = parser.parse_args()
    path = opts.file
    
    inst = Convert(path)
    inst.to_string()
    inst.write_file("text")
    