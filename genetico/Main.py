from optparse import OptionParser
from ConstructiveSolution import *

if __name__ == "__main__":

    # python.exe .\Main.py -s .\instance\instance
    parser = OptionParser()
    parser.add_option("-s", "--path", dest="path", type="string")

    (opts, _) = parser.parse_args()

    path = opts.path

    ex = Extract(path)
    inst = Instance(ex)

    initial_population = []
    total_makespan = 0
    for i in range(5):
        solu = Solution(inst)
        greedy = ConstructiveSolution(inst)
        greedy.build_naive(solu)
        initial_population.append(solu)
        total_makespan += solu.cmax

 
    for i in initial_population:
        person: Solution = i
        print(person.cmax)

    print("--------------")
    ordenad = sorted(initial_population, key=lambda x: x.cmax)
    for i in ordenad:
        person: Solution = i
        print(person.cmax)
        


    print("Total:",total_makespan)