from Solution import *
from typing import Callable


class GA:
    def __init__(self, init_pop: list):
        self.n_parent = len(init_pop)
        self.parent: dict = self.__calc_fitness__(init_pop)
        self.population: list = self.__get_population__(self.parent)
        self.generation = 1
        self.best_fitness: Solution = init_pop[0]

    def __get_population__(self, x: dict) -> list:
        pop = x.values()
        population = []
        for i in pop:
            ind: Individual = i
            population.append(ind.sol)

        return population

    def __calc_fitness__(self, population: list) -> dict:

        pop_ranked = sorted(population, key=lambda x: x.cmax)
        fitness = {}
        total_fitness = 0
        # calcula o custo total dos n melhores individuos
        for i in range(self.n_parent):
            sol: Solution = pop_ranked[i]
            total_fitness += 1/sol.cmax

        # melhores individuos com o respectivo valor da aptidão
        for i in range(self.n_parent):
            sol: Solution = pop_ranked[i]
            fit = (1/sol.cmax)/total_fitness
            fitness[i] = Individual(sol, fit)

        # atualiza o valor do mais apto
        self.best_fitness = pop_ranked[0]

        return fitness

    def select_parents(self) -> list:
        return self.population

    def build_crossover(self) -> list:

        return self.population

    def mutation_gene(self) -> list:
        return self.population

    def next_generation(self, stop_gener: int):

        incumbente = self.best_fitness.cmax
        for i in range(stop_gener):
            parents = self.select_parents()
            children = self.build_crossover()
            population = parents.extend(children)
            self.generation += 1
            self.__calc_fitness__(children)
            if incumbente == self.best_fitness.cmax:
                print(f"Encerrado porque {i}° geração não obteve melhoria.")
                exit()
            else:
                print(f"CMax {self.best_fitness.cmax} == {incumbente}: {i}° geração ")
            incumbente = self.best_fitness.cmax

class Individual():
    def __init__(self, sol: Solution, fitness: float):
        self.sol = sol
        self.fitness = fitness
