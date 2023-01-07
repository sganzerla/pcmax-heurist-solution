from Solution import *
import random


class GA:
    def __init__(self, init_pop: list):
        self.__n_parent: int = len(init_pop)
        self.__population: list = init_pop
        self.__parent: dict = self.__calc_fitness__()
        self.__generation: int = 1
        self.incumbent: Solution = init_pop[0]

    def __calc_fitness__(self) -> dict:

        pop_ranked = sorted(self.__population, key=lambda x: x.cmax)
        fitness = {}
        total_fitness = 0
        # sum fitness total
        for i in range(self.__n_parent):
            sol: Solution = pop_ranked[i]
            total_fitness += 1 / sol.cmax

        # fitness individual
        for i in range(self.__n_parent):
            sol: Solution = pop_ranked[i]
            fit = (1 / sol.cmax) / total_fitness
            fitness[i] = Individual(sol, fit)

        self.incumbent = pop_ranked[0]
        return fitness

    def __select_parent__(self):

        # parents = self.parent.values()
        # for p in parents:
        #     p: Individual = p
        #     print(p.fitness, p.sol.cmax)

        return self.__population

    def __build_crossover__(self) -> list:
        # TODO
        return self.__population

    def __mutation_gene_make__(self):

        k = int(self.__n_parent * 0.10)
        # 20% parents
        change_gene = random.choices(range(self.__n_parent), k=k)
        for i in change_gene:
            self.__swap_random__(self.__population[i])

    @staticmethod
    def __swap_random__(solu: Solution):

        idx_m = solu.get_makespan_idx()
        first_job = solu.m[Node.Suc][solu.inst.get_n() + idx_m]
        jobs_make = []
        # jobs cmax
        while first_job < solu.inst.get_n():
            jobs_make.append(first_job)
            first_job = solu.m[Node.Suc][first_job]

        j1, j2 = 0, 0
        while j1 == j2:
            j1 = random.choice(jobs_make)
            j2 = random.choice(jobs_make)
        
        pre_j1 = solu.get_pre(j1)
        pre_j2 = solu.get_pre(j2)
        solu.eject_job(idx_m, j1)
        solu.eject_job(idx_m, j2)
        solu.insert_job(idx_m, j2, pre_j1)
        solu.insert_job(idx_m, j1, pre_j2)

    def next_generation(self, n_generation: int):

        for _ in range(n_generation):
            self.__parent = self.__calc_fitness__()
            self.__select_parent__()  # TODO
            self.__build_crossover__()  # TODO
            self.__mutation_gene_make__()  # ok
            self.__generation += 1


class Individual:
    def __init__(self, sol: Solution, fitness: float):
        self.sol = sol
        self.fitness = fitness
