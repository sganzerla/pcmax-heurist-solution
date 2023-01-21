from code.Constructive import *
from code.Extract import *
from code.ExtractSolution import *
from code.Genetic import *
from code.Instance import *
from code.Notification import *
from code.Solution import *
from optparse import OptionParser
import os
import pandas as pd
import time


def build_greedy(inst: Instance) -> Solution:
    sol = Solution(inst)
    greedy = Constructive(inst)
    greedy.build_greedy(sol)
    return sol

def build_lit(inst: Instance, ex_sol: ExtractSolution) -> Solution:
    sol = Solution(inst)
    lit = Constructive(inst)
    lit.build_like(sol, ex_sol.sequence, ex_sol.size_each_m)
    return sol

def get_root_instances():
    parser = OptionParser()
    parser.add_option("-s", "--source", dest="source", type="string")
    parser.add_option("-r", "--repeat", dest="repeat", type="int")
    # solução gulosa usada na população inicial valor 1 senão 0 e 2 Prof. Felipe
    parser.add_option("-g", "--greedy", dest="greedy", type="int")
    (opts, _) = parser.parse_args()
    source = opts.source
    repeat = opts.repeat
    greedy = opts.greedy

    return repeat, source, greedy

def use_const_init_sol(type: int):
    return ['None', 'Greedy', 'Muller'][type]


if __name__ == "__main__":
    
    # python3 Tests.py --source instance/ --repeat 9 --greedy 0
    # python3 Tests.py -s instance/ -r 10 -g 1

    gen_size = 10  # quantidade de gerações
    repeat_size, root, greedy_type = get_root_instances()

    files = []
    for (_, _, paths) in os.walk(root):
        for file in paths:
            files.append(file)

    inst_size = len(files)  # quantidade de instâncias dentro da pasta
    files = sorted(files)
    # extrai dados da literatura
    lit_sols: List[ExtractSolution] = np.ndarray(inst_size, dtype=ExtractSolution)
    for i in range(inst_size):
        lit_sol = ExtractSolution(files[i], os.path.join("solution/" + files[i]))
        lit_sols[i] = lit_sol
    times = np.ndarray(repeat_size, dtype=float)
    cmaxs = np.ndarray(repeat_size, dtype=int)
    gaps = np.ndarray(repeat_size, dtype=float)
    data = pd.DataFrame(columns=["instance", "m", "n", "repeat", "population", "generation", "literature",
                        "cmax", "time", "gap",  "var_cmax", "std_cmax", "mean_cmax", "var_time", "std_time", "mean_time", "use_const_init_sol", "mutation_size"])
    for i in range(inst_size):
        file = files[i]
        name = "_".join(str(k) for k in file.split("_")[2:])
        inst = Instance(Extract(os.path.join(root + file)))
        greedy_sol = build_greedy(inst)
        lit_sol = build_lit(inst, lit_sols[i])
        
        pop_size = int(5 + (inst.get_rate()) * 0.50)
        
        for j in range(repeat_size):
            time_genet = time.time()
            init_pop: List[Solution] = np.ndarray(pop_size, dtype=Solution)
            constr = Constructive(inst)
            for k in range(pop_size):
                sol = Solution(inst)
                constr.build_naive(sol)
                init_pop[k] = sol
            
            # relatorio inclui solução gulosa dentro pop inicial
            if greedy_type == 1:
                init_pop[0] = greedy_sol
            if greedy_type == 2:
                init_pop[0] = lit_sol
                
                
            ga = Genetic(init_pop, inst)
            ga.next_generation(gen_size)
            times[j] = time.time() - time_genet
            cmaxs[j] = ga.inc_sol.cmax
            gap = ((lit_sol.cmax - ga.inc_sol.cmax) / ga.inc_sol.cmax)
            if gap != 0.0:
                gap = gap * -1
            gaps[j] = gap
            print(
                f"inst: {name} |  m: {inst.get_m()} | n: {inst.get_n()} | repeat: {j} | pop_size: {pop_size} | generations: {gen_size} | literature: {lit_sol.cmax} |  cmax: {cmaxs[j]} | time: {times[j]:.2f} | gap: {gaps[j]:.2f} | start_good_sol: {use_const_init_sol(greedy_type)} | mutations: {int(0.10 * pop_size + 1)}")
        var_time = np.var(times)
        mean_time = np.mean(times)
        std_time = np.std(times)
        var_cmax = np.var(cmaxs)
        mean_cmax = np.mean(cmaxs)
        std_cmax = np.std(cmaxs)
        use_good_init_sol = np.array(
            [use_const_init_sol(greedy_type)] * repeat_size)
        df = pd.DataFrame(data={
            "instance": np.array([name]*repeat_size),
            "m": np.array([inst.get_m()] * repeat_size),
            "n": np.array([inst.get_n()] * repeat_size),
            "literature": np.array([lit_sol.cmax] * repeat_size),
            "repeat": range(repeat_size),
            "cmax": cmaxs,
            "time": times,
            "var_cmax": np.array([var_cmax] * repeat_size),
            "std_cmax": np.array([std_cmax] * repeat_size),
            "mean_cmax": np.array([mean_cmax] * repeat_size),
            "var_time": np.array([var_time] * repeat_size),
            "std_time": np.array([std_time] * repeat_size),
            "mean_time": np.array([mean_time] * repeat_size),
            "generation": np.array([gen_size] * repeat_size),
            "population": np.array([pop_size] * repeat_size),
            "gap": gaps,
            "use_const_init_sol": use_good_init_sol,
            "mutation_size": np.array([int(0.10 * pop_size + 1)] * repeat_size)
        })

        data = pd.concat([data, df], ignore_index=True)

    data.to_csv(f'report{greedy_type}.csv', decimal=".", sep=";")
    print("File report.csv created.")
    notification = Notification(".credentials")
    notification.send_message(f'report{greedy_type}.csv', f"Instâncias: {inst_size} \n Repetiçõs: {repeat_size}\n Gerações: {gen_size} ", f'report{greedy_type}.csv')  
