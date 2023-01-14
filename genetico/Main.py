from ConstructiveSolution import *
from GA import *

if __name__ == "__main__":

    path = '001_struc_2_10_01'
    
    inst = Instance(Extract(path))

    init_pop = []

    for i in range(50):
        greedy = ConstructiveSolution(inst)
        solu = Solution(inst)
        greedy.build_naive(solu)
        init_pop.append(solu)

    ga = GA(init_pop)

    ga.next_generation(25)
    print(ga.incum_sol.cmax)
