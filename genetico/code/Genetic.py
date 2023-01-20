from typing import List
from math import ceil
from code.Constructive import *
from code.Neighborhood import *


class Genetic:
    def __init__(self, init_pop: List[Solution], inst: Instance):
        self.__pop_size: int = len(init_pop)
        self.__pop: List[Solution] = init_pop
        self.__fit_pop: List[Individual]
        self.__parent: List[List[Solution]]
        self.__children: List[Solution]
        self.__inst = inst
        self.__neighbor = Neighborhood(self.__inst)
        self.__const = Constructive(self.__inst)
        self.inc_sol: Solution
        self.generation: int = 0

    def __start_population__(self):
        if self.generation > 0:
            # junta pop original com nova
            self.__pop = np.concatenate(
                [self.__pop, self.__children], dtype=Solution, axis=0)

    def __calc_fitness__(self):

        pop_ranked = sorted(self.__pop, key=lambda x: x.cmax)
        pop_reduced = pop_ranked[:self.__pop_size]
        fitness = np.ndarray(self.__pop_size, dtype=Individual)
        total_fitness = 0

        # sum fitness total
        for i in range(self.__pop_size):
            total_fitness += 1 / pop_reduced[i].cmax

        # fitness individual
        for i in range(self.__pop_size):
            fit = (1 / pop_reduced[i].cmax) / total_fitness
            fitness[i] = Individual(pop_reduced[i], fit)

        # sol inc
        self.inc_sol = pop_reduced[0]
        self.__fit_pop = fitness
        self.__pop = pop_reduced

    def __selection_parent__(self):

        fit_pop: List[Individual] = self.__fit_pop

        idx_g5 = int(self.__pop_size * 0.80)
        idx_g4 = int(self.__pop_size * 0.60)
        idx_g3 = int(self.__pop_size * 0.40)
        idx_g2 = int(self.__pop_size * 0.20)
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

        weights = np.zeros(self.__pop_size, dtype=float)
        population = np.ones(self.__pop_size, dtype=Solution)
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

        parent_size = ceil(self.__pop_size / 2)
        p1 = random.choices(population, weights=weights, k=parent_size)
        p2 = random.choices(population, weights=weights, k=parent_size)
        parent: List[List[Solution]] = [p1, p2]
        self.__parent = parent

    def __crossover__(self):

        m = self.__inst.get_m()
        n = self.__inst.get_n()

        pair_size = ceil(self.__pop_size / 2)
        nursery_a = np.ndarray(pair_size, dtype=Solution)
        nursery_b = np.ndarray(pair_size, dtype=Solution)

        for p in range(pair_size):
            # jobs da maquina
            jobs_pa_str = ""
            jobs_pb_str = ""
            # qtd jobs por maquina
            jobs_size_pa = np.ndarray(m, dtype=int)
            jobs_size_pb = np.ndarray(m, dtype=int)

            for i in range(m):
                jobs_size_pa[i] = self.__parent[0][p].get_num_jobs_machine(i)
                jobs_size_pb[i] = self.__parent[1][p].get_num_jobs_machine(i)

                # 1º job mach
                job_a = self.__parent[0][p].m[Node.Suc][n + i]
                job_b = self.__parent[1][p].m[Node.Suc][n + i]

                while job_a < n:
                    jobs_pa_str += f" {job_a}"
                    job_a = self.__parent[0][p].m[Node.Suc][job_a]
                while job_b < n:
                    jobs_pb_str += f" {job_b}"
                    job_b = self.__parent[1][p].m[Node.Suc][job_b]

            chrom_pa = np.asarray([int(i)
                                   for i in jobs_pa_str.split() if i.isdigit()])
            chrom_pb = np.asarray([int(i)
                                   for i in jobs_pb_str.split() if i.isdigit()])
            cut = random.randint(1, n - 1)

            chrom_ca = np.concatenate([chrom_pa[:cut], chrom_pb[cut:]], axis=0)
            chrom_cb = np.concatenate([chrom_pb[:cut], chrom_pa[cut:]], axis=0)

            # fix
            chrom_a, chrom_b = self.__fix_chrom__(chrom_ca, chrom_cb)

            sol_a = Solution(self.__inst)
            sol_b = Solution(self.__inst)

            self.__const.build_best(sol_a, chrom_a)
            self.__const.build_best(sol_b, chrom_b)

            nursery_a[p] = sol_a
            nursery_b[p] = sol_b

        self.__children = np.concatenate([nursery_a, nursery_b], axis=0)

    @staticmethod
    def __fix_chrom__(chr_a: np.ndarray, chr_b: np.ndarray) -> tuple:

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

    def __make_mutation__(self):

        perc = int(0.10 * self.__pop_size + 1)
        rnd = random.choices(range(self.__pop_size), k=perc)
        for i in rnd:
            sol = self.__children[i]
            self.__neighbor.swap(sol)
            self.__neighbor.insertion(sol)
            self.__neighbor.swap(sol)
            self.__neighbor.insertion(sol)
            self.__neighbor.swap(sol)
            self.__neighbor.insertion(sol) 
     

    def next_generation(self, n_generation: int):

        for i in range(n_generation):
            self.__start_population__()
            self.__calc_fitness__()
            self.__selection_parent__()
            self.__crossover__()
            self.__make_mutation__()

            self.generation += 1
            # pop = np.ndarray(self.__pop_size, dtype=int)
            # for p in range(self.__pop_size):
            #     pop[p] = self.__pop[p].cmax

            # std = np.std(pop)
            # var = np.var(pop)
            # print(
            #     f"cmax: {self.inc_sol.cmax} | gen: {self.generation} | var: {var:.2f} | std: {std:.2f}")
            # if var < 1:
            #     break


class Individual:
    def __init__(self, sol: Solution, fitness: float):
        self.sol: Solution = sol
        self.fitness: float = fitness


class Parent:
    def __init__(self, sol_a: Solution, sol_b: Solution):
        self.sol_a: Solution = sol_a
        self.sol_b: Solution = sol_b
