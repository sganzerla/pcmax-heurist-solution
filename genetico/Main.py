from ConstructiveSolution import *
from GA import *

if __name__ == "__main__":

    path = '001_struc_2_10_01'

    ex = Extract(path)
    inst = Instance(ex)

    init_pop = []
    total_makespan = 0
    
    
    for i in range(50):
        solu = Solution(inst)
        greedy = ConstructiveSolution(inst)
        greedy.build_naive(solu)
        init_pop.append(solu)
        total_makespan += solu.cmax


    ga = GA(init_pop)
    
    ga.next_generation(4)
    print(ga.best_fitness.cmax)
    