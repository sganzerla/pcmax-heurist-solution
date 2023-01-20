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
    parser.add_option("-s", "--source", dest="source", type="string")
    parser.add_option("-r", "--repeat", dest="repeat", type="int")
    (opts, _) = parser.parse_args()
    source = opts.source
    repeat = opts.repeat
    
            
    return repeat, source

def use_const_init_sol(type: int):
    return ['None', 'Greedy', 'Muller'][type]

if __name__ == "__main__":

    # python3 Tests.py -s ../instance/ -r 20
    gen_size = 5  # quantidade de gerações
    start_good_sol = 0 # solução gulosa usada na população inicial valor 1 senão 0 e 2 Felipe
    repeat_size, root = get_root_instances()

    files = []
    for (_, _, paths) in os.walk(root):
        for file in paths:
            files.append(file)


    instance_size = len(files)  # quantidade de instâncias dentro da pasta

    files = sorted(files)
    
    times = np.ndarray(repeat_size, dtype=float)
    cmaxs = np.ndarray(repeat_size, dtype=int)
    gaps = np.ndarray(repeat_size, dtype=float)
    data = pd.DataFrame(columns=["instance", "m", "n", "repeat", "population", "generation", "cmax_const",
                        "cmax_genet", "time", "gap",  "var_cmax", "std_cmax", "mean_cmax", "var_time", "std_time", "mean_time", "use_const_init_sol", "mutation_size"])
    for i in range(instance_size):
        file = files[i]
        name = "_".join(str(k) for k in file.split("_")[2:])
        inst = Instance(Extract(os.path.join(root + file)))
        greedy = build_greedy(inst)
        pop_size = int(5 + (inst.get_n() / inst.get_m()) * 0.50)
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
            gaps[j] = ((greedy.cmax - ga.inc_sol.cmax) / ga.inc_sol.cmax) * -1
            print(
                f"inst: {name} |  m: {inst.get_m()} | n: {inst.get_n()} | repeat: {j} | pop_size: {pop_size} | generations: {gen_size} | cmax_greedy: {greedy.cmax} |  cmax_genetic: {cmaxs[j]} | time: {times[j]:.2f} | gap: {gaps[j]:.2f} | start_good_sol: {use_const_init_sol(start_good_sol)} | mutations: {int(0.10 * pop_size + 1)}")
        mutations = np.array([int(0.10 * pop_size + 1)]* repeat_size)
        names = np.array([name]*repeat_size)
        greedys = np.array([greedy.cmax] * repeat_size)
        ms = np.array([inst.get_m()]* repeat_size)
        ns = np.array([inst.get_n()]* repeat_size)
        var_time = np.var(times)
        vars_time = np.array([var_time] * repeat_size)
        mean_time = np.mean(times)
        means_time = np.array([mean_time] * repeat_size)
        std_time = np.std(times)
        stds_time = np.array([std_time] * repeat_size)
        var_cmax = np.var(cmaxs)
        vars_cmax = np.array([var_cmax] * repeat_size)
        mean_cmax = np.mean(cmaxs)
        means_cmax = np.array([mean_cmax] * repeat_size)
        std_cmax = np.std(cmaxs)
        stds_cmax = np.array([std_cmax] * repeat_size)
        population = np.array([pop_size] * repeat_size)
        generation = np.array([gen_size] * repeat_size)
        use_good_init_sol = np.array([use_const_init_sol(start_good_sol)] * repeat_size)
        df = pd.DataFrame(data={
            "instance": names,
            "m": ms,
            "n": ns,
            "cmax_const": greedys,
            "repeat": range(repeat_size),
            "cmax_genet": cmaxs,
            "time": times,
            "var_cmax": vars_cmax,
            "std_cmax": stds_cmax,
            "mean_cmax" : means_cmax,
            "var_time" : vars_time,
            "std_time" : stds_time,
            "mean_time": means_time,
            "generation": generation,
            "population": population,
            "gap": gaps,
            "use_const_init_sol": use_good_init_sol,
            "mutations": mutations
        })
        
        data = pd.concat([data, df], ignore_index=True)
    
    data.to_csv('report.csv', decimal=".", sep = ";")
    print("File report.csv created.")