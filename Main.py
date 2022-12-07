import os
from optparse import OptionParser

from ConstructiveSolution import *
from Insertion import *


def get_path_files(path_root: str):
    path_files = []
    for (_, _, path_file) in os.walk(path_root):
        for f in path_file:
            path_files.append(f)
    return path_files


if __name__ == "__main__":

    # python.exe .\Main.py -s .\instance_one\

    parser = OptionParser()
    parser.add_option("-s", "--path", dest="path", type="string")
    # parser.add_option("-o", "--output", dest="output", type="string")

    (opts, _) = parser.parse_args()

    path = opts.path

    # add path root com inst
    files = get_path_files(path)

    # barra de progress
    n_files = len(files)
    aux = 1

    for file in files:
        print(f"({aux}/{n_files})")

        ex = Extract(path + file)
        inst = Instance(ex)
        solu = Solution(inst)

        greedy = ConstructiveSolution(inst)
        insert = Insertion(inst)
        # greedy.build_naive(solu)
        # solu.to_string()
        # solu.check_fact()
        # solu.check_solution()
        # solu.reset()
        
        # inst.to_string()
        greedy.build_greedy(solu)
        solu.to_string()
        solu.check_solution()
        insert.search(solu)        
        solu.to_string()
        solu.check_solution() 
        aux += 1
        exit(0)

