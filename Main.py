from Instance import *
from Extract import *
from ConstrutiveSolution import *
from optparse import OptionParser
import os


def get_params():
    parser = OptionParser()
    parser.add_option("-s", "--path", dest="path", type="string")
    parser.add_option("-o", "--output", dest="output", type="string")

    (opts, _) = parser.parse_args()

    return opts.path, opts.output


def get_path_files(path):
    files = []
    for (_, _, file) in os.walk(path):
        for f in file:
            files.append(f)
    return files


if __name__ == "__main__":

    path, output = get_params()

    # adicionando o path de todas as instâncias
    files = get_path_files(path)

    # barra de progresso
    n_files = len(files)
    aux = 1
    for file in files:
        print(f"({aux}/{n_files})")
        ex = Extract(path + file)
        m, p, s = ex.get_M(), ex.get_P(), ex.get_S()
        ins = Instance(m, p, s)
        s, n = ins.get_S(), ins.get_N()

        cons = ConstrutiveSolution(m, n, s)
        cons.to_string()
        aux += 1
