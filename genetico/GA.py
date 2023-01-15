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
            self.popul = np.concatenate([self.popul, self.children], dtype=Solution, axis=0)

    def __calc_fitness__(self):

        pop_ranked = sorted(self.popul, key=lambda x: x.cmax)
        pop_reduced = pop_ranked[:self.popul_size]
        fitness = np.ndarray(self.popul_size, dtype=Individual)
        total_fitness = 0

        # sum fitness total
        i = 0
        for i in range(self.popul_size):
            total_fitness += 1 / pop_reduced[i].cmax

        # fitness individual
        i = 0
        for i in range(self.popul_size):
            fit = (1 / pop_reduced[i].cmax) / total_fitness
            fitness[i] = Individual(pop_reduced[i], fit)

        # atualizando o valor da incumbente
        self.incum_sol = pop_reduced[0]
        self.popul_fit = fitness
        self.popul =  pop_reduced

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
            child1 = -np.ones(n, dtype=int)
            child2 = -np.ones(n, dtype=int)

            for k in range(n):
                if k < cut:
                    child1[k] = jobs_pa[k]
                    child2[k] = jobs_pb[k]
                else:
                    child1[k] = jobs_pb[k]
                    child2[k] = jobs_pa[k]
            sol_a = Solution(self.inst)
            sol_b = Solution(self.inst)

            # TODO fazer reparação no dna antes de usar
            # sol_a.create_solution(child1, jobs_size_pa)
            # sol_b.create_solution(child2, jobs_size_pb)
            sol_a.create_solution(jobs_pa, jobs_size_pa)
            sol_b.create_solution(jobs_pb, jobs_size_pb)
            children1[p] = sol_a
            children2[p] = sol_b

        self.children = np.concatenate(
            [children1, children2], dtype=Solution, axis=0)

    def __make_mutation__(self, percent: float = 0.10):
        k = int(self.popul_size * percent)

        change_gene = random.choices(range(self.popul_size), k=k)
        for i in change_gene:
            self.__swap_random__(self.children[i])

    @staticmethod
    def __swap_random__(solu: Solution):

        idx_m = solu.get_makespan_idx()
        jobs_make = GA.__get_jobs_by_machine__(solu, idx_m)

        j1, j2 = 0, 0
        while j1 == j2:
            j1 = random.choice(jobs_make)
            j2 = random.choice(jobs_make)

        GA.__change_jobs__(solu, idx_m, j1, j2)

    @staticmethod
    def __change_jobs__(solu: Solution, idx_m: int, j1: int, j2: int):
        pre_j1 = solu.get_pre(j1)
        pre_j2 = solu.get_pre(j2)
        solu.eject_job(idx_m, j1)
        solu.eject_job(idx_m, j2)
        solu.insert_job(idx_m, j2, pre_j1)
        solu.insert_job(idx_m, j1, pre_j2)

    @staticmethod
    def __get_jobs_by_machine__(solu: Solution, idx_m: int):
        first_job = solu.m[Node.Suc][solu.inst.get_n() + idx_m]
        num_jobs_machine = solu.get_num_jobs_machine(idx_m)
        jobs_make = np.ones(num_jobs_machine, dtype=int)
        aux = 0
        while first_job < solu.inst.get_n():
            jobs_make[aux] = first_job
            first_job = solu.m[Node.Suc][first_job]
            aux += 1
        return jobs_make

    def next_generation(self, n_generation: int):

        for _ in range(n_generation):
            self.__start_population__()
            self.__calc_fitness__()
            self.__selection_parent__()
            self.__crossover__()
            # self.__make_mutation__() # TODO mutar os filhos

            self.generation += 1


class Individual:
    def __init__(self, sol: Solution, fitness: float):
        self.sol: Solution = sol
        self.fitness: float = fitness


class Parent:
    def __init__(self, sol_a: Solution, sol_b: Solution):
        self.sol_a: Solution = sol_a
        self.sol_b: Solution = sol_b
