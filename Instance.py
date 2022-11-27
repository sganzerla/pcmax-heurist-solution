import numpy as np
import pandas as pd
class Instance:
    def __init__(self, M: int, P: np.array, S: np.array):
        self.__M = M
        self.__P = P
        self.__N = len(P)
        self.__S = self.__join_times__(S)
        
    def __join_times__(self, S: np.array) -> np.array:
        n = self.get_N()
        for i in range(n):
            S[i][:] = S[i][:] + self.__P[i]
        return S
    
    
    def to_string(self):
        print(f"M: {self.__M}\nN: {self.__N}\nP: {self.__P}\nS: {pd.DataFrame(self.__S).T}")
        
    def get_M(self) -> int:
        return self.__M
    
    def get_N(self) -> int:
        return self.__N
    
    def get_P(self, i)-> int:
        return self.P[i] 
    
    def get_S(self, i, j) -> int:
        return self.__S[i][j]
    
    
        
    

