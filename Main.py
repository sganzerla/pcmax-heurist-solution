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

    ex = Extract(path)
    inst = Instance(ex)
    solu = Solution(inst)

    greedy = ConstructiveSolution(inst)
    ls = LocalSearch(inst)

    # greedy.build_naive(solu)
    greedy.build_greedy(solu)
    solu.to_string()

    print("================ 3-opt=============")
    ls.opt3(solu, solu.get_makespan_idx())
    print(solu.get_makespan())
    solu.check_solution()
    
    print("================ Insertion =============")
    ls.insertion(solu)
    print(solu.get_makespan())
    solu.check_solution()

    print("================ Swap      =============")
    ls.swap(solu)
    print(solu.get_makespan())
    solu.check_solution()

