from ConstructiveSolution import *
from GA import *

if __name__ == "__main__":

    path = '001_struc_2_10_01'
    
    inst = Instance(Extract(path))

    init_pop = np.ndarray(50, dtype=Solution)

    greedy = ConstructiveSolution(inst)
    for i in range(50):
        solu = Solution(inst)
        greedy.build_naive(solu)
        init_pop[i] = solu

    ga = GA(init_pop)

    ga.next_generation(20)
    print(ga.incum_sol.cmax)
