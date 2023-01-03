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

    initial_population = []
    for i in range(5):
        solu = Solution(inst)
        greedy = ConstructiveSolution(inst)
        greedy.build_naive(solu)
        initial_population.append(solu)

    for i in initial_population:
        person: Solution = i
        print(person.cmax)

    ordenad = sorted(initial_population, key=lambda x: x.cmax)
    for i in initial_population:
        person: Solution = i
        print(person.cmax)
