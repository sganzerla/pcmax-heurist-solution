from Instance import Instance
from Solution import Solution


class LocalSearchHandler:

    def __init__(self, inst: Instance):
        self.inst = inst

    def build_2opt(self, sol: Solution):

        n1 = range(self.inst.get_n() + 1)
        arcs = [(i, j) for i in n1 for j in n1 if 1 <
                i and i < j and j < self.inst.get_n()]
        best_cost = 0
        best_change = []
        for i, j in arcs:
            current_cost = sol.new_cost_2opt(i, j)
            if best_cost > current_cost:
                best_cost = current_cost
                best_change = [i, j]
                
        print("best change: ", best_change, "reduzindo o custo ", best_cost)
