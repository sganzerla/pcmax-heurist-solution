import sys
import random

from code.Instance import *
from code.Solution import *


class Constructive:
    def __init__(self, inst: Instance):
        self.__inst = inst

    def build_like_a(self, sol: Solution, jobs: np.ndarray, size_each_m: np.ndarray):

        j_aux = 0
        for m in range(self.__inst.get_m()):
            size = size_each_m[m]
            pre = self.__inst.get_n() + m
            for _ in range(size):
                job = jobs[j_aux]
                sol.insert_job(m, job, pre)
                pre = job
                j_aux += 1

    def build_like_b(self, sol: Solution, jobs: np.ndarray):
        j_aux = 0
        for m in range(self.__inst.get_m()):
            pre = self.__inst.get_n() + m
            for j in jobs[m]:
                job = j
                sol.insert_job(m, job, pre)
                pre = job
                j_aux += 1

    def build_naive(self, solu: Solution):
        jobs = [i for i in range(self.__inst.get_n())]
        random.shuffle(jobs)

        for i in range(self.__inst.get_n()):
            m = random.randint(0, self.__inst.get_m() - 1)
            solu.insert_job(
                m, jobs[i], solu.get_pre(self.__inst.get_n() + m))

    def build_greedy(self, solu: Solution):
        i_jobs = self.__inst.get_p_copy().argsort()[::-1]

        for i in i_jobs:
            best_delta = sys.maxsize
            best_move = [-1, -1]
            for j in range(self.__inst.get_m()):
                job = self.__inst.get_n() + j
                suc = solu.get_suc(job)
                # remove arco
                delta = solu.get_c(j) - self.__inst.get_s(job, suc)
                # add arco esq
                delta += self.__inst.get_s(job, i)
                # add arco dir
                delta += self.__inst.get_s(i, suc)

                if delta < best_delta:
                    best_delta = delta
                    best_move = [j, job]

                while suc < self.__inst.get_n():
                    job = suc
                    suc = solu.get_suc(job)
                    # remove arco
                    delta = solu.get_c(j) - self.__inst.get_s(job, suc)
                    # add arc esq
                    delta += self.__inst.get_s(job, i)
                    # add arc dir
                    delta += self.__inst.get_s(i, suc)

                    if delta < best_delta:
                        best_delta = delta
                        best_move = [j, job]

            solu.insert_job(best_move[0], i, best_move[1])
