from ConstructiveSolution import *
from GA import *

if __name__ == "__main__":

    path = '001_struc_2_10_01'
    
    inst = Instance(Extract(path))

    pop_size = 60
    
    init_pop: List[Solution] = np.ndarray(pop_size, dtype=Solution)
    const_sol = ConstructiveSolution(inst)
    
    for i in range(pop_size):
        solu = Solution(inst)
        const_sol.build_naive(solu)
        init_pop[i] = solu

    # testando a adição de uma solução gulosa
    solu = Solution(inst)
    const_sol.build_greedy(solu)
    
    init_pop[0] = solu
    print("CMax Guloso: ", solu.cmax)
    ga = GA(init_pop, inst)

    ga.next_generation(1)
    print("CMax Genético: ", ga.incum_sol.cmax)
