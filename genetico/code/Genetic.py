import numpy as np
import random

from typing import List

from code.Instance import *
from code.Solution import *
from code.Neighborhood import *
from code.Constructive import *


class Genetic:
    def __init__(self, init_pop: List[Solution], inst: Instance):
        self.pop_size: int = len(init_pop)
        self.pop: List[Solution] = init_pop
        self.fit_pop: List[Individual]
        self.parent: List[List[Solution]]
        self.children: List[Solution]
        self.generation: int = 1
        self.inc_sol: Solution
        self.inst = inst
        self.neighbor = Neighborhood(self.inst)
        self.constr = Constructive(self.inst)

    def __start_population__(self):
        if self.generation > 1:
            # junta pop original com nova
            self.pop = np.concatenate(
                [self.pop, self.children], dtype=Solution, axis=0)

    def __calc_fitness__(self):

        pop_ranked = sorted(self.pop, key=lambda x: x.cmax)
        pop_reduced = pop_ranked[:self.pop_size]
        fitness = np.ndarray(self.pop_size, dtype=Individual)
        total_fitness = 0

        # sum fitness total
        for i in range(self.pop_size):
            total_fitness += 1 / pop_reduced[i].cmax

        # fitness individual
        for i in range(self.pop_size):
            fit = (1 / pop_reduced[i].cmax) / total_fitness
            fitness[i] = Individual(pop_reduced[i], fit)

        # sol inc
        self.inc_sol = pop_reduced[0]
        self.fit_pop = fitness
        self.pop = pop_reduced

    def __selection_parent__(self):

        fit_pop: List[Individual] = self.fit_pop

        idx_g5 = int(self.pop_size * 0.80)
        idx_g4 = int(self.pop_size * 0.60)
        idx_g3 = int(self.pop_size * 0.40)
        idx_g2 = int(self.pop_size * 0.20)
        idx_g1 = 0
        fit_sum_group = np.zeros(5, dtype=float)
        for i in range(idx_g1, idx_g2):
            i1 = i + idx_g1
            fit_sum_group[0] += fit_pop[i1].fitness
            i2 = i + idx_g2
            fit_sum_group[1] += fit_pop[i2].fitness
            i3 = i + idx_g3
            fit_sum_group[2] += fit_pop[i3].fitness
            i4 = i + idx_g4
            fit_sum_group[3] += fit_pop[i4].fitness
            i5 = i + idx_g5
            fit_sum_group[4] += fit_pop[i5].fitness

        weights = np.zeros(self.pop_size, dtype=float)
        population = np.ones(self.pop_size, dtype=Solution)
        for i in range(idx_g1, idx_g2):
            i1 = i + idx_g1
            weights[i1] = fit_sum_group[0]
            population[i1] = fit_pop[i1].sol
            i2 = i + idx_g2
            weights[i2] = fit_sum_group[1]
            population[i2] = fit_pop[i2].sol
            i3 = i + idx_g3
            weights[i3] = fit_sum_group[2]
            population[i3] = fit_pop[i3].sol
            i4 = i + idx_g4
            weights[i4] = fit_sum_group[3]
            population[i4] = fit_pop[i4].sol
            i5 = i + idx_g5
            weights[i5] = fit_sum_group[4]
            population[i5] = fit_pop[i5].sol

        parent_size = int(self.pop_size / 2)
        p1 = random.choices(population, weights=weights, k=parent_size)
        p2 = random.choices(population, weights=weights, k=parent_size)
        parent: List[List[Solution]] = [p1, p2]
        self.parent = parent

    def __crossover__(self):
        
        # if self.generation % 2 == 0:
            self.__encoded_by_job__()
        # else:
            # self.__encoded_by_machine__()

    def __encoded_by_job__(self):

        m = self.inst.get_m()
        n = self.inst.get_n()

        n_pairs = int(self.pop_size / 2)
        children1 = np.ndarray(n_pairs, dtype=Solution)
        children2 = np.ndarray(n_pairs, dtype=Solution)

        for p in range(n_pairs):
            # jobs da maquina
            jobs_pa_str = ""
            jobs_pb_str = ""
            # qtd jobs por maquina
            jobs_size_pa = np.ndarray(m, dtype=int)
            jobs_size_pb = np.ndarray(m, dtype=int)

            for i in range(m):
                jobs_size_pa[i] = self.parent[0][p].get_num_jobs_machine(i)
                jobs_size_pb[i] = self.parent[1][p].get_num_jobs_machine(i)

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
            cut_l = random.randint(1, int(n /2))
            cut_r = random.randint(int(n /2), n-1)

            # crossover ABA == BAB
            child_a = np.concatenate([jobs_pa[:cut_l], jobs_pb[cut_l:cut_r], jobs_pa[cut_r:]], axis=0)
            child_b = np.concatenate([jobs_pb[:cut_l], jobs_pa[cut_l:cut_r], jobs_pb[cut_r:]], axis=0)
            
            # fix
            child1, child2 = self.__fix_chrom__(child_a, child_b)

            sol_a = Solution(self.inst)
            sol_b = Solution(self.inst)

            self.constr.build_like(sol_a, child1, jobs_size_pa)
            self.constr.build_like(sol_b, child2, jobs_size_pb)
            
            children1[p] = sol_a
            children2[p] = sol_b

        self.children = np.concatenate([children1, children2], axis=0)

    @staticmethod
    def __fix_chrom__(chr_a: np.ndarray, chr_b: np.ndarray):

        uniq_a, uniq_b = set(), set()
        dup_a = [x for x in chr_a if x in uniq_a or (uniq_a.add(x) or False)]
        dup_b = [x for x in chr_b if x in uniq_b or (uniq_b.add(x) or False)]

        size = len(dup_b)
        # idx jobs dup A|B
        idx_dup_a = np.ndarray(size, dtype=int)
        idx_dup_b = np.ndarray(size, dtype=int)
        for i in range(size):
            idx_dup_a[i] = np.where(chr_a == dup_a[i])[0][0]
            idx_dup_b[i] = np.where(chr_b == dup_b[i])[0][0]

        # subs jobs dup
        for i in range(size):
            chr_a[idx_dup_a[i]] = dup_b[i]
            chr_b[idx_dup_b[i]] = dup_a[i]
        
        return chr_a, chr_b

    def __encoded_by_machine__(self):
        
        n = self.inst.get_n()
        n_pairs = int(self.pop_size / 2)
        children1 = np.ndarray(n_pairs, dtype=Solution)
        children2 = np.ndarray(n_pairs, dtype=Solution)
        for i in range(n_pairs):
            jobs_pa = -np.ones(n, dtype=int)
            jobs_pb = -np.ones(n, dtype=int)
         
            for j in range(n):
                jobs_pa[j] = self.parent[0][i].get_job_machine(j)
                jobs_pb[j] = self.parent[1][i].get_job_machine(j)
          
            # one point 
            cut = random.randint(1, n-1)
            
            child_a = np.concatenate([jobs_pa[:cut], jobs_pb[cut:]], axis=0)
            child_b = np.concatenate([jobs_pb[:cut], jobs_pa[cut:]], axis=0)
            
            # sep list jobs por maq
            child1 = np.ndarray(self.inst.get_m(), dtype=list)
            child2 = np.ndarray(self.inst.get_m(), dtype=list)
            for k in range(self.inst.get_m()):
                va = [j for j in range(self.inst.get_n()) if child_a[j] == k]
                vb = [j for j in range(self.inst.get_n()) if child_b[j] == k]
                random.shuffle(va)
                random.shuffle(vb)
                child1[k] = va
                child2[k] = vb

            sol_a = Solution(self.inst)
            sol_b = Solution(self.inst)

            sol_a.create_sol_strat_b(child1)
            sol_b.create_sol_strat_b(child2)
            
            children1[i] = sol_a
            children2[i] = sol_b

        self.children = np.concatenate([children1, children2], axis=0)

    def __make_mutation__(self):
        
        for i in [0, int(self.pop_size * 0.25) - 1, int(self.pop_size * 0.5) - 1]:
            sol = self.children[i] 
            self.neighbor.swap(sol)
            self.neighbor.insertion(sol)
            # for i in range(self.inst.get_m()):
            #     self.ls.gen_insert(sol, i)
            self.neighbor.swap(sol)
            self.neighbor.insertion(sol)
            # for i in range(self.inst.get_m()):
            #     ls.gen_insert(sol, i)

    def next_generation(self, n_generation: int):

        for i in range(n_generation):
            self.__start_population__()
            self.__calc_fitness__()
            self.__selection_parent__()
            self.__crossover__()
            self.__make_mutation__()

            self.generation += 1
            pop = np.ndarray(self.pop_size, dtype=int)    
            for i in range(self.pop_size):
                pop[i] = self.pop[i].cmax
                
            std = np.std(pop)
            var = np.var(pop)
            print(f"cmax: {self.inc_sol.cmax} | gen: {self.generation} | var: {var:.2f} | std: {std:.2f}")
            if var < 1:
                break


class Individual:
    def __init__(self, sol: Solution, fitness: float):
        self.sol: Solution = sol
        self.fitness: float = fitness


class Parent:
    def __init__(self, sol_a: Solution, sol_b: Solution):
        self.sol_a: Solution = sol_a
        self.sol_b: Solution = sol_b
