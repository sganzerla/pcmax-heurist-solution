import sys
from Solution import *
from Instance import *
import random


class ConstructiveSolution:
    def __init__(self, inst: Instance):
        self.inst = inst

    def build_naive(self, solu: Solution):
        jobs = [i for i in range(self.inst.get_n())]
        random.shuffle(jobs)

        for i in range(self.inst.get_n()):
            m = random.randint(0, self.inst.get_m() - 1)
            solu.insert_job(
                m, jobs[i], solu.get_pre(self.inst.get_n() + m))

    def build_greedy(self, solu: Solution):
        i_jobs = self.inst.get_p_copy().argsort()[::-1]

        for i in i_jobs:
            best_delta = sys.maxsize
            best_move = [-1, -1]
            for j in range(self.inst.get_m()):
                job = self.inst.get_n() + j
                suc = solu.get_suc(job)
                # remove arco
                delta = solu.get_c(j) - self.inst.get_s(job, suc)
                # add arco esq
                delta += self.inst.get_s(job, i)
                # add arco dir
                delta += self.inst.get_s(i, suc)

                if delta < best_delta:
                    best_delta = delta
                    best_move = [j, job]

                while suc < self.inst.get_n():
                    job = suc
                    suc = solu.get_suc(job)
                    # remove arco
                    delta = solu.get_c(j) - self.inst.get_s(job, suc)
                    # add arc esq
                    delta += self.inst.get_s(job, i)
                    # add arc dir
                    delta += self.inst.get_s(i, suc)

                    if delta < best_delta:
                        best_delta = delta
                        best_move = [j, job]

            solu.insert_job(best_move[0], i, best_move[1])
