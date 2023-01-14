from Solution import *
import random
from typing import List

class GA:
    def __init__(self, init_popul: List[Solution]):
        self.popul_size: int = len(init_popul)
        self.popul: List[Solution] = init_popul
        self.popul_fit: List[Individual] = None
        self.parent: List[List[Solution]] = None
        self.generation: int = 1
        self.incum_sol: Solution = init_popul[0]

    def __calc_fitness__(self):

        pop_ranked = sorted(self.popul, key=lambda x: x.cmax)
        fitness = np.ndarray(self.popul_size, dtype=Individual)
        total_fitness = 0

        # sum fitness total
        for i in range(self.popul_size):
            total_fitness += 1 / pop_ranked[i].cmax

        # fitness individual
        for i in range(self.popul_size):
            sol: Solution = pop_ranked[i]
            fit = (1 / sol.cmax) / total_fitness
            fitness[i] = Individual(sol, fit)

        self.incum_sol = pop_ranked[0]
        self.popul_fit = fitness

    def __crossover__(self):

        # acessar os casais
        print(self.parent[0][0].cmax, self.parent[1][0].cmax)
        
        # self.popul = lista com pais e os filhos

    def __selection_parent__(self):

        popul_fit: List[Individual] = self.popul_fit

        idx_g5 = int(self.popul_size * 0.80)
        idx_g4 = int(self.popul_size * 0.60)
        idx_g3 = int(self.popul_size * 0.40)
        idx_g2 = int(self.popul_size * 0.20)
        idx_g1 = 0
        fit_sum_group = np.zeros(5)
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

    def __make_mutation__(self, percent: float = 0.10):

        k = int(self.popul_size * percent)
        change_gene = random.choices(range(self.popul_size), k=k)
        for i in change_gene:
            self.__swap_random__(self.popul[i])

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
    def __change_jobs__(solu, idx_m, j1, j2):
        pre_j1 = solu.get_pre(j1)
        pre_j2 = solu.get_pre(j2)
        solu.eject_job(idx_m, j1)
        solu.eject_job(idx_m, j2)
        solu.insert_job(idx_m, j2, pre_j1)
        solu.insert_job(idx_m, j1, pre_j2)

    @staticmethod
    def __get_jobs_by_machine__(solu, idx_m):
        first_job = solu.m[Node.Suc][solu.inst.get_n() + idx_m]
        jobs_make = []
        # jobs cmax
        while first_job < solu.inst.get_n():
            jobs_make.append(first_job)
            first_job = solu.m[Node.Suc][first_job]
        return jobs_make

    def next_generation(self, n_generation: int):

        for _ in range(n_generation):
            self.__calc_fitness__()
            self.__selection_parent__()
            self.__crossover__()
            self.__make_mutation__()  # refatorar está muito caro
            self.generation += 1


class Individual:
    def __init__(self, sol: Solution, fitness: float):
        self.sol: Solution = sol
        self.fitness: float = fitness

class Parent:
    def __init__(self, sol_a: Solution, sol_b: Solution):
        self.sol_a: Solution = sol_a
        self.sol_b: Solution = sol_b
    
