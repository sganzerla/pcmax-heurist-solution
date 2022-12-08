import os
from optparse import OptionParser

from ConstructiveSolution import *
from LocalSearch import *


if __name__ == "__main__":

    # python.exe .\Main.py -s .\instance_one\

    parser = OptionParser()
    parser.add_option("-s", "--path", dest="path", type="string")
    # parser.add_option("-o", "--output", dest="output", type="string")

    (opts, _) = parser.parse_args()

    path = opts.path

    # add path root com inst


    ex = Extract(path)
    inst = Instance(ex)
    solu = Solution(inst)

    greedy = ConstructiveSolution(inst)
    ls = LocalSearch(inst)
    
    #greedy.build_naive(solu)
    greedy.build_greedy(solu)
    solu.to_string()
    
    
    print("================ Insertion =============") 
    ls.insertion(solu)        
    print(solu.get_makespan())
    solu.check_solution() 

    print("================ Swap      =============") 
    ls.swap(solu)        
    print(solu.get_makespan())
    solu.check_solution() 
   
    print("================ 3-opt=============") 
    for m in range(inst.get_m()) : 
        ls.opt3(solu, m)
    print(solu.get_makespan())
    solu.check_solution()

    print("\n\n") 
    solu.to_string()

