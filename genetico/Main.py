from ConstructiveSolution import *
from GA import *

if __name__ == "__main__":

    # path = '001_struc_2_10_01'
    path = '006_struc_2_100_01'
    
    inst = Instance(Extract(path))

    pop_size = 200
    
    init_pop: List[Solution] = np.ndarray(pop_size, dtype=Solution)
    const_sol = ConstructiveSolution(inst)
    
    for i in range(pop_size):
        solu = Solution(inst)
        const_sol.build_naive(solu)
        init_pop[i] = solu

   
    ga = GA(init_pop, inst)
    ga.next_generation(1000)
    
    
     # testando a adição de uma solução gulosa
    solu = Solution(inst)
    const_sol.build_greedy(solu)
    print("CMax Guloso: ", solu.cmax)
    
