from Solution import *
from Instance import *

#  https://www.ic.unicamp.br/~reltech/PFG/2021/PFG-21-40.pdf

class LocalSearchSolution:
    def __init__(self, inst: Instance):
        self.inst = inst

    def build_2_opt(self):
        ciclos = 10
        arcs = [(i, j) for i in range(self.inst.get_N() + 1)
                for j in range(self.inst.get_N() + 1) if 1 <= i < j]

        while ciclos > 0:

            # for i, j in arcs:
            #     custos_atualizados = self.__swap__(i, j)
                # if custos_atualizados < custos:
                    
                
            ciclos -= 1

    def __swap__(self, i, j) -> np.ndarray:
        
        # troco os arcos e retorno o valor atualizado dos custos de cada máquina
        return []
