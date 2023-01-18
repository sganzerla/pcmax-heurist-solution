from code.Constructive import *
from code.Extract import *
from code.Genetic import *
from code.Instance import *
from code.Solution import *
import os
from optparse import OptionParser

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-r", "--file", dest="file", type = "string")
    (opts, _) = parser.parse_args()
    path = opts.file
    
    if path is None:
        # path = '../instance/001_struc_2_10_01'
        # path = '../instance/002_struc_2_10_02'
        path = '../instance/006_struc_2_100_01'


    inst = Instance(Extract(os.path.join(path)))

    pop_size = 30
    
    init_pop: List[Solution] = np.ndarray(pop_size, dtype=Solution)
    const_sol = Constructive(inst)
    
    for i in range(pop_size):
        sol = Solution(inst)
        const_sol.build_naive(sol)
        init_pop[i] = sol

   
    sol = Solution(inst)
    const_sol.build_greedy(sol)
    init_pop[0] = sol
    ga = Genetic(init_pop, inst)
    ga.next_generation(30)
    print("CMax Guloso: ", sol.cmax)
    
    

    
