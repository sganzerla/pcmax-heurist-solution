from Instance import Instance
from Solution import Solution
import numpy as np

class LocalSearchHandler:

    def __init__(self, inst: Instance):
        self.inst = inst

    # https://en.wikipedia.org/wiki/2-opt
    def build_2opt(self, sol: Solution):

        n1 = self.inst.get_n() + 1

        arcs = [(i, j) for i in range(n1)
                for j in range(n1) if 1 > i and i > j]
        
        best_cmax = sol.cmax
        for i, j in arcs:
            
            nova_rota  = self.__swap2opt__(i, j, sol)
            new_cmax = sol.cmax
            if new_cmax < best_cmax:
                best_cmax = new_cmax


    def __swap2opt__(self, i: int, j: int, sol: Solution):
        
        return 0