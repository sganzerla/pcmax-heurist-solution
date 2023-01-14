from Solution import *
import random
from typing import List

class GA:
    def __init__(self, init_popul: List[Solution]):
        self.popul_size: int = len(init_popul)
        self.popul: List[Solution] = init_popul
        self.popul_fit: dict
        self.parent: List[Parent]
        self.generation: int = 1
        self.incum_sol: Solution = init_popul[0]

    def __calc_fitness__(self):

        pop_ranked = sorted(self.popul, key=lambda x: x.cmax)
        fitness = {}
        total_fitness = 0

        # sum fitness total
        for i in range(self.popul_size):
            sol: Solution = pop_ranked[i]
            total_fitness += 1 / sol.cmax

        # fitness individual
        for i in range(self.popul_size):
            sol: Solution = pop_ranked[i]
            fit = (1 / sol.cmax) / total_fitness
            fitness[i] = Individual(sol, fit)

        self.incum_sol = pop_ranked[0]
        self.popul_fit = fitness

    def __crossover__(self):

        return self.popul
    
    
    def __selection_parent__(self):

        popul_fit: List[Individual] = list(self.popul_fit.values())

        idx_g5 = int(self.popul_size * 0.80)
        
        idx_g4 = int(self.popul_size * 0.60)
        idx_g3 = int(self.popul_size * 0.40)
        idx_g2 = int(self.popul_size * 0.20)
        idx_g1 = 0
        group_fit_sum = np.zeros(5)
        group_idx1 = []
        group_idx2 = []
        group_idx3 = []
        group_idx4 = []
        group_idx5 = []

        for i in range(idx_g1, idx_g2):
            group_fit_sum[0] += popul_fit[i].fitness
            group_idx1.append(popul_fit[i].sol)

            i2 = i + idx_g2
            group_fit_sum[1] += popul_fit[i2].fitness
            group_idx2.append(popul_fit[i2].sol)

            i3 = i + idx_g3
            group_fit_sum[2] += popul_fit[i3].fitness
            group_idx3.append(popul_fit[i3].sol)

            i4 = i + idx_g4
            group_fit_sum[3] += popul_fit[i4].fitness
            group_idx4.append(popul_fit[i4].sol)

            i5 = i + idx_g5
            group_fit_sum[4] += popul_fit[i5].fitness
            group_idx5.append(popul_fit[i5].sol)


        list_pop = [group_idx1, group_idx2,
                    group_idx3, group_idx4, group_idx5]

        parent = []
        for i in range(int(self.popul_size/2)):
            rnd = random.choices(list_pop, weights=group_fit_sum, k=2)
            p1: Solution = rnd[0][0]
            p2: Solution = rnd[1][0]
            parent.append(Parent(p1, p2))
        
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
        self.sol = sol
        self.fitness = fitness

class Parent:
    def __init__(self, sol_a: Solution, sol_b: Solution):
        self.sol_a = sol_a
        self.sol_b = sol_b
    
