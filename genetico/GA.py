from Solution import *
import random
from typing import List


class GA:
    def __init__(self, init_popul: List[Solution], inst: Instance):
        self.popul_size: int = len(init_popul)
        self.popul: List[Solution] = init_popul
        self.popul_fit: List[Individual] = None
        self.parent: List[List[Solution]] = None
        self.children: List[Solution] = None
        self.generation: int = 1
        self.incum_sol: Solution = None
        self.inst = inst

    def __start_population__(self):
        if self.generation > 1:
            # junta a população original com a nova geração
            self.popul = np.concatenate(
                [self.popul, self.children], dtype=Solution, axis=0)

    def __calc_fitness__(self):

        pop_ranked = sorted(self.popul, key=lambda x: x.cmax)
        pop_reduced = pop_ranked[:self.popul_size]
        fitness = np.ndarray(self.popul_size, dtype=Individual)
        total_fitness = 0

        # sum fitness total
        for i in range(self.popul_size):
            total_fitness += 1 / pop_reduced[i].cmax

        # fitness individual
        for i in range(self.popul_size):
            fit = (1 / pop_reduced[i].cmax) / total_fitness
            fitness[i] = Individual(pop_reduced[i], fit)

        # atualizando o valor da incumbente
        self.incum_sol = pop_reduced[0]
        self.popul_fit = fitness
        self.popul = pop_reduced

    def __selection_parent__(self):

        popul_fit: List[Individual] = self.popul_fit

        idx_g5 = int(self.popul_size * 0.80)
        idx_g4 = int(self.popul_size * 0.60)
        idx_g3 = int(self.popul_size * 0.40)
        idx_g2 = int(self.popul_size * 0.20)
        idx_g1 = 0
        fit_sum_group = np.zeros(5, dtype=float)
        for i in range(idx_g1, idx_g2):
            i1 = i + idx_g1
            fit_sum_group[0] += popul_fit[i1].fitness
            i2 = i + idx_g2
            fit_sum_group[1] += popul_fit[i2].fitness
            i3 = i + idx_g3
            fit_sum_group[2] += popul_fit[i3].fitness
            i4 = i + idx_g4
            fit_sum_group[3] += popul_fit[i4].fitness
            i5 = i + idx_g5
            fit_sum_group[4] += popul_fit[i5].fitness

        weights = np.zeros(self.popul_size, dtype=float)
        population = np.ones(self.popul_size, dtype=Solution)
        for i in range(idx_g1, idx_g2):
            i1 = i + idx_g1
            weights[i1] = fit_sum_group[0]
            population[i1] = popul_fit[i1].sol
            i2 = i + idx_g2
            weights[i2] = fit_sum_group[1]
            population[i2] = popul_fit[i2].sol
            i3 = i + idx_g3
            weights[i3] = fit_sum_group[2]
            population[i3] = popul_fit[i3].sol
            i4 = i + idx_g4
            weights[i4] = fit_sum_group[3]
            population[i4] = popul_fit[i4].sol
            i5 = i + idx_g5
            weights[i5] = fit_sum_group[4]
            population[i5] = popul_fit[i5].sol

        parent_size = int(self.popul_size/2)
        p1 = random.choices(population, weights=weights, k=parent_size)
        p2 = random.choices(population, weights=weights, k=parent_size)
        parent: List[List[Solution]] = [p1, p2]
        self.parent = parent

    def __crossover__(self):

        m = self.inst.get_m()
        n = self.inst.get_n()

        n_pairs = int(self.popul_size / 2)
        children1 = np.ndarray(n_pairs, dtype=Solution)
        children2 = np.ndarray(n_pairs, dtype=Solution)
        # iterar todos os casais
        for p in range(n_pairs):
            # sequencia de jobs daquela solução
            jobs_pa_str = ""
            jobs_pb_str = ""
            # quantidade de jobs por maquina
            jobs_size_pa = np.ndarray(m, dtype=int)
            jobs_size_pb = np.ndarray(m, dtype=int)

            for i in range(m):
                # filhos vão herdar característica quant de jobs em cada máquina
                jobs_size_pa[i] = self.parent[0][p].get_num_jobs_machine(i)
                jobs_size_pb[i] = self.parent[1][p].get_num_jobs_machine(i)
                # primeiro job do pai a
                jm_a = self.parent[0][p].m[Node.Suc][n + i]
                jm_b = self.parent[1][p].m[Node.Suc][n + i]

                while jm_a < n:
                    jobs_pa_str += f" {jm_a}"
                    jm_a = self.parent[0][p].m[Node.Suc][jm_a]
                while jm_b < n:
                    jobs_pb_str += f" {jm_b}"
                    jm_b = self.parent[1][p].m[Node.Suc][jm_b]

            jobs_pa = np.asarray([int(i)
                                 for i in jobs_pa_str.split() if i.isdigit()])
            jobs_pb = np.asarray([int(i)
                                 for i in jobs_pb_str.split() if i.isdigit()])
            cut = random.randint(1, n-1)
          
            # crossover
            childa = np.concatenate([jobs_pa[:cut], jobs_pb[cut:]], axis=0)
            childb = np.concatenate([jobs_pb[:cut], jobs_pa[cut:]], axis=0)
            # reparação
            child1, child2 = self.__repar_gene__(childa, childb)

            sol_a = Solution(self.inst)
            sol_b = Solution(self.inst)

            sol_a.create_solution(child1, jobs_size_pa)
            sol_b.create_solution(child2, jobs_size_pb)
            
            children1[p] = sol_a
            children2[p] = sol_b

        self.children = np.concatenate([children1, children2], axis=0)

    def __repar_gene__(self, childa: np.ndarray, childb: np.ndarray):


        if len(childa) != len(childb):
            print("diferentes", len(childa), childa, len(childb), childb)
        uniq_a, uniq_b = set(), set()
        dup_a = [x for x in childa if x in uniq_a or (uniq_a.add(x) or False)]
        dup_b = [x for x in childb if x in uniq_b or (uniq_b.add(x) or False)]

        size = len(dup_b)
        # separando os índices dos elementos repetidos
        idx_dup_a = np.ndarray(size, dtype=int)
        for i in range(size):
            idx_dup_a[i] = np.where(childa == dup_a[i])[0][0]

        idx_dup_b = np.ndarray(size, dtype=int)
        for i in range(size):
            idx_dup_b[i] = np.where(childb == dup_b[i])[0][0]

        
        # substituindo os elementos repetidos
        for i in range(size):
            childa[idx_dup_a[i]] = dup_b[i]
            childb[idx_dup_b[i]] = dup_a[i]
        
        return childa, childb

    def __make_mutation__(self, percent: float = 0.05):
        k = int(self.popul_size * percent)

        change_gene = random.choices(range(self.popul_size), k=k)
        for i in change_gene:
            sol = self.children[i] 

            idx_m = sol.get_makespan_idx()
            jobs_m_str = ""
            jm_a = sol.m[Node.Suc][sol.inst.get_n() + idx_m]
            while jm_a < sol.inst.get_n():
                jobs_m_str += f" {jm_a}"
                jm_a = sol.m[Node.Suc][jm_a]
                
            jobs_m = [int(i) for i in jobs_m_str.split() if i.isdigit()]

            j1, j2 = random.sample(jobs_m, 2)
            
            prei = sol.get_pre(j1)
            prej = sol.get_pre(j2)
            sol.eject_job(idx_m, j1)
            sol.eject_job(idx_m, j2)
            sol.insert_job(idx_m, j2, prei)
            sol.insert_job(idx_m, j1, prej)
            sol.check_solution()


    def next_generation(self, n_generation: int):

        for _ in range(n_generation):
            self.__start_population__()
            self.__calc_fitness__()
            self.__selection_parent__()
            self.__crossover__()
            self.__make_mutation__() # TODO mutar os filhos

            self.generation += 1


class Individual:
    def __init__(self, sol: Solution, fitness: float):
        self.sol: Solution = sol
        self.fitness: float = fitness


class Parent:
    def __init__(self, sol_a: Solution, sol_b: Solution):
        self.sol_a: Solution = sol_a
        self.sol_b: Solution = sol_b
