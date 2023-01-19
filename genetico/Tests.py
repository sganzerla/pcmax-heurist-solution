from code.Constructive import *
from code.Extract import *
from code.Genetic import *
from code.Instance import *
from code.Solution import *
from optparse import OptionParser
import os
import pandas as pd
import time

def build_greedy(inst) -> Solution:
    sol = Solution(inst)
    greedy = Constructive(inst)
    greedy.build_greedy(sol)
    return sol

def get_root_instances():
    parser = OptionParser()
    parser.add_option("-s", "--root", dest="root", type="string")
    (opts, _) = parser.parse_args()
    root = opts.root

    files = []
    for (_, _, paths) in os.walk(root):
        for file in paths:
            files.append(file)
    return root, files


if __name__ == "__main__":

    # python3 Tests.py -s ../instance/

    pop_size = 10  # população inicial
    gen_size = 5  # quantidade de gerações
    repeat_size = 20  # repetir o GA com a mesma instância

    root, files = get_root_instances()

    instance_size = len(files)  # quantidade de instâncias dentro da pasta

    files = sorted(files)
    
    times = np.ndarray(repeat_size, dtype=float)
    cmaxs = np.ndarray(repeat_size, dtype=int)
    data = pd.DataFrame(columns=["instance", "m", "n", "cmax_const", "repeat", "cmax_genet", "time", "population", "generation", "var_cmax", "std_cmax", "mean_cmax", "var_time", "std_time", "mean_time"])

    for i in range(instance_size):
        name = files[i]
        inst = Instance(Extract(os.path.join(root + name)))
        greedy = build_greedy(inst)
        for j in range(repeat_size):
            time_genet = time.time()
            init_pop: List[Solution] = np.ndarray(pop_size, dtype=Solution)
            constr = Constructive(inst)

            for k in range(pop_size):
                sol = Solution(inst)
                constr.build_naive(sol)
                init_pop[k] = sol

            ga = Genetic(init_pop, inst)
            ga.next_generation(gen_size)
            times[j] = time.time() - time_genet
            cmaxs[j] = ga.inc_sol.cmax
            print(
                f"inst: {name} |  m: {inst.get_m()} | n: {inst.get_n()} | cmax_greedy: {greedy.cmax} |repeat: {j} | cmax_genetic: {cmaxs[j]} | time: {times[j]} ")
        names = np.array([name]*repeat_size)
        greedys = np.array([greedy.cmax]*repeat_size)
        ms = np.array([inst.get_m()]* repeat_size)
        ns = np.array([inst.get_n()]* repeat_size)
        var_time = np.array([np.var(times)] * repeat_size)
        mean_time = np.array([np.mean(times)] * repeat_size)
        std_time = np.array([np.std(times)] * repeat_size)
        var_cmax = np.array([np.var(cmaxs)] * repeat_size)
        mean_cmax = np.array([np.mean(cmaxs)] * repeat_size)
        std_cmax = np.array([np.std(cmaxs)] * repeat_size)
        population = np.array([pop_size] * repeat_size)
        generation = np.array([gen_size] * repeat_size)
        df = pd.DataFrame(data={
            "instance": names,
            "m": ms,
            "n": ns,
            "cmax_const": greedys,
            "repeat": range(repeat_size),
            "cmax_genet": cmaxs,
            "time": times,
            "var_cmax": var_cmax,
            "std_cmax": std_cmax,
            "mean_cmax" : mean_cmax,
            "var_time" : var_time,
            "std_time" : std_time,
            "mean_time": mean_time,
            "generation": generation,
            "population": population
        })
        
        data = pd.concat([data, df], ignore_index=True)
    
    data.to_csv('report.csv', decimal=".", sep = ";")
    print("File report.csv created.")