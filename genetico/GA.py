from Solution import *
import random


class GA:
    def __init__(self, init_pop: list):
        self.__n_parent: int = len(init_pop)
        self.__population: list = init_pop
        self.__fit_population: dict
        # self.__parent: tuple
        self.__generation: int = 1
        self.incumbent: Solution = init_pop[0]

    def __calc_fitness__(self):

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
        self.__fit_population = fitness

    def __crossover_parent__(self):

        parent: list[Individual] = list(self.__fit_population.values())

        idx_g5 = int(self.__n_parent * 0.80)
        idx_g4 = int(self.__n_parent * 0.60)
        idx_g3 = int(self.__n_parent * 0.40)
        idx_g2 = int(self.__n_parent * 0.20)
        idx_g1 = 0
        group_fitness_sum = np.zeros(5)
        group_ind1 = []
        group_ind2 = []
        group_ind3 = []
        group_ind4 = []
        group_ind5 = []
        aux = 0
        for i in range(idx_g1, idx_g2):
            print(i, parent[i].sol.cmax, parent[i].fitness)
            group_fitness_sum[0] += parent[i].fitness
            group_ind1.append(parent[i].sol)
            aux += 1

        for i in range(idx_g2, idx_g3):
            print(i, parent[i].sol.cmax, parent[i].fitness)
            group_fitness_sum[1] += parent[i].fitness
            group_ind2.append(parent[i].sol)

        for i in range(idx_g3, idx_g4):
            print(i, parent[i].sol.cmax, parent[i].fitness)
            group_fitness_sum[2] += parent[i].fitness
            group_ind3.append(parent[i].sol)

        for i in range(idx_g4, idx_g5):
            print(i, parent[i].sol.cmax, parent[i].fitness)
            group_fitness_sum[3] += parent[i].fitness
            group_ind4.append(parent[i].sol)

        for i in range(idx_g5, self.__n_parent):
            print(i, parent[i].sol.cmax, parent[i].fitness)
            group_fitness_sum[4] += parent[i].fitness
            group_ind5.append(parent[i].sol)

        list_pop = [group_ind1, group_ind2,
                    group_ind3, group_ind4, group_ind5]
        for i in range(int(self.__n_parent/2)):
            parent_rnd = random.choices(
                list_pop, weights=group_fitness_sum, k=2)
            p1: Solution = parent_rnd[0][0]
            jobs_p1 = self.__get_jobs_by_machine__(p1, p1.cmax_idx)
            p2: Solution = parent_rnd[1][0]
            jobs_p2 = self.__get_jobs_by_machine__(p2, p2.cmax_idx)


            # TODO sortear o indice do corte do cromossomo
            
            
            

        return self.__population


    def __mutation_gene_make__(self, percent: float = 0.20):

        k = int(self.__n_parent * percent)
        # 20% parents
        change_gene = random.choices(range(self.__n_parent), k=k)
        for i in change_gene:
            self.__swap_random__(self.__population[i])

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
            self.__crossover_parent__()  # TODO
            self.__mutation_gene_make__()  # ok
            self.__generation += 1


class Individual:
    def __init__(self, sol: Solution, fitness: float):
        self.sol = sol
        self.fitness = fitness
