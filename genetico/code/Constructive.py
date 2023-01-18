import sys
import random
from typing import List

from code.Solution import *


class Constructive:
    def __init__(self, inst: Instance):
        self.__inst = inst

    def build_like(self, sol: Solution, jobs: np.ndarray, size_each_m: np.ndarray):

        j_aux = 0
        for m in range(self.__inst.get_m()):
            size = size_each_m[m]
            pre = self.__inst.get_n() + m
            for _ in range(size):
                job = jobs[j_aux]
                sol.insert_job(m, job, pre)
                pre = job
                j_aux += 1

    def build_naive(self, sol: Solution):
        jobs = [i for i in range(self.__inst.get_n())]
        random.shuffle(jobs)

        for i in range(self.__inst.get_n()):
            m = random.randint(0, self.__inst.get_m() - 1)
            sol.insert_job(
                m, jobs[i], sol.get_pre(self.__inst.get_n() + m))

    def build_best(self, sol: Solution, i_jobs: np.ndarray):

        self.__build_jobs__(sol, i_jobs)

    def __build_jobs__(self, sol, i_jobs):
        for i in i_jobs:
            best_delta = sys.maxsize
            best_move = [-1, -1]
            for j in range(self.__inst.get_m()):
                job = self.__inst.get_n() + j
                suc = sol.get_suc(job)
                # remove arco
                delta = sol.get_c(j) - self.__inst.get_s(job, suc)
                # add arco esq
                delta += self.__inst.get_s(job, i)
                # add arco dir
                delta += self.__inst.get_s(i, suc)

                if delta < best_delta:
                    best_delta = delta
                    best_move = [j, job]

                while suc < self.__inst.get_n():
                    job = suc
                    suc = sol.get_suc(job)
                    # remove arco
                    delta = sol.get_c(j) - self.__inst.get_s(job, suc)
                    # add arc esq
                    delta += self.__inst.get_s(job, i)
                    # add arc dir
                    delta += self.__inst.get_s(i, suc)

                    if delta < best_delta:
                        best_delta = delta
                        best_move = [j, job]

            sol.insert_job(best_move[0], i, best_move[1])


    def build_greedy(self, sol: Solution):
        i_jobs = self.__inst.get_p_copy().argsort()[::-1]

        self.__build_jobs__(sol, i_jobs)