from Solution import *
import random


class GA:
    def __init__(self, init_pop: list):
        self.__n_parent: int = len(init_pop)
        self.__population: list = init_pop
        self.best_fitness: Solution = init_pop[0]
        self.__parent: dict = self.__calc_fitness__()
        self.__generation: int = 1

    def __get_population__(self, x: dict) -> list:
        pop = x.values()
        population = []
        for i in pop:
            ind: Individual = i
            population.append(ind.sol)

        return population

    def __calc_fitness__(self) -> dict:

        pop_ranked = sorted(self.__population, key=lambda x: x.cmax)
        fitness = {}
        total_fitness = 0
        # calcula o custo total dos n melhores individuos
        for i in range(self.__n_parent):
            sol: Solution = pop_ranked[i]
            total_fitness += 1/sol.cmax

        # melhores individuos com o respectivo valor da aptidão
        for i in range(self.__n_parent):
            sol: Solution = pop_ranked[i]
            fit = (1/sol.cmax)/total_fitness
            fitness[i] = Individual(sol, fit)

        # atualiza o valor do mais apto
        self.best_fitness = pop_ranked[0]
        return fitness

    def __select_parent__(self):

        # TODO ROLETA
        # parents = self.parent.values()
        # for p in parents:
        #     p: Individual = p
        #     print(p.fitness, p.sol.cmax)

        return self.__population

    def __build_crossover__(self) -> list:
        # TODO
        return self.__population

    def __mutation_gene_make__(self) -> list:
        # TODO  REALIZAR UM SWAP ENTRE JOBS NA MAQUINA MAKESPAN
        for i in self.__population:
            self.__swap_random__(i)

        return self.__population

    def __swap_random__(self, solu: Solution):

        idx_m = solu.get_makespan_idx()
        first_job = solu.m[Node.Suc][solu.inst.get_n() + idx_m]
        jobs_make = []
        # Obtendo os jobs da máquina makespan
        while first_job < solu.inst.get_n():
            jobs_make.append(first_job)
            first_job = solu.m[Node.Suc][first_job]
        # escolhendo dois pra troca aleatoriamente
        j1, j2 = 0, 0
        while j1 == j2:
            j1 = random.choice(jobs_make)
            j2 = random.choice(jobs_make)

        prei = solu.get_pre(j1)
        prej = solu.get_pre(j2)
        solu.ejeta_job(idx_m, j1)
        solu.ejeta_job(idx_m, j2)
        solu.insert_job(idx_m, j2, prei)
        solu.insert_job(idx_m, j1, prej)

    def next_generation(self, stop_gener: int):

        for _ in range(stop_gener):
            self.__parent = self.__calc_fitness__()
            self.__select_parent__()  # fazer
            self.__build_crossover__()  # fazer
            self.__mutation_gene_make__()  # ok
            self.__generation += 1


class Individual():
    def __init__(self, sol: Solution, fitness: float):
        self.sol = sol
        self.fitness = fitness
