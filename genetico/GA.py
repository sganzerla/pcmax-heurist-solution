from Solution import *


class GA:
    def __init__(self, init_pop: list):
        self.n_parent = len(init_pop)
        self.parent: dict = self.__calc_fitness__(init_pop)
        self.generation = 1

    def __calc_fitness__(self, population: list) -> dict:
        pop_ranked = sorted(population, key=lambda x: x.cmax)
        fitness = {}
        total_fitness = 0
        for i in range(self.n_parent):
            sol: Solution = pop_ranked[i]
            total_fitness += 1/sol.cmax

        for i in range(self.n_parent):
            sol: Solution = pop_ranked[i]
            fit = (1/sol.cmax)/total_fitness
            fitness[i] = Individual(sol, fit)
        return fitness

    def select_parents(self) -> list:
        return self.population

    def crossover(self) -> list:

        return self.__

    def mutation_gene(self) -> list:
        return self.population

    def next_generation(self, stop_gener: int) -> Solution:

        for i in range(stop_gener):
            i

        return self.population[0]


class Individual():
    def __init__(self, sol: Solution, fitness: float):
        self.sol = sol
        self.fitness = fitness
