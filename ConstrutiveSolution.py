import sys 
from Solution import *
from Instance import *
import random


class ConstrutiveSolution:
    def __init__(self, inst: Instance):
        self.inst = inst

    def build_naive(self, solu: Solution):
        jobs = [i for i in range(self.inst.get_N())]
        random.shuffle(jobs)

        for i in range(self.inst.get_N()):
            m = random.randint(0, self.inst.get_M()-1)
            solu.insert_job(
                m, jobs[i], solu.get_pre(self.inst.get_N()+m))

    def build_greedy(self, solu: Solution):
        i_jobs = self.inst.get_copy_P().argsort()[::-1]

        for i in i_jobs:
            best_delta = sys.maxsize 
            best_move=[-1, -1]
            for j in range(self.inst.get_M()):
                job = self.inst.get_N()+j
                suc_job = solu.get_suc(job)
                delta = solu.get_C(j) + self.inst.get_S(job,i)+self.inst.get_S(i,suc_job)\
                             -self.inst.get_S(job,suc_job)
                if delta < best_delta:
                   best_delta = delta
                   best_move = [j, job]                   
                while suc_job < self.inst.get_N():
                    job = suc_job
                    suc_job = solu.get_suc(job)
                    delta = solu.get_C(j) + self.inst.get_S(job,i)+self.inst.get_S(i,suc_job)\
                             -self.inst.get_S(job,suc_job)
                    if delta < best_delta:
                        best_delta = delta
                        best_move = [j, job]                   
            
            solu.insert_job(best_move[0], i,best_move[1]) 
