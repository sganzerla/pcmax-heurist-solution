from Instance import *
from Extract import *
from Solution import *
from ConstructiveSolution import *
from optparse import OptionParser
import os


def get_path_files(path):
    files = []
    for (_, _, file) in os.walk(path):
        for f in file:
            files.append(f)
    return files


if __name__ == "__main__":

    # path = pasta onde estão as instancias
    # python.exe .\Main.py -s .\instance_one\

    parser = OptionParser()
    parser.add_option("-s", "--path", dest="path", type="string")
    # parser.add_option("-o", "--output", dest="output", type="string")

    (opts, _) = parser.parse_args()

    path = opts.path

    # adicionando o path de todas as instâncias
    files = get_path_files(path)

    # barra de progresso
    n_files = len(files)
    aux = 1

    for file in files:
        print(f"({aux}/{n_files})")

        ex = Extract(path + file)
        ins = Instance(ex)
        solu = Solution(ins)

        greedy = ConstructiveSolution(ins)
        # greedy.build_naive(solu)
        # solu.to_string()
        # solu.reset()
        
        ins.to_string()
        greedy.build_greedy(solu)
        solu.to_string()
        #solu.check_fact()
        aux += 1
        exit(0)

