import numpy as np
from Instance import *
from enum import IntEnum


class Node(IntEnum):
    Pre = 0
    Suc = 1


class Solution:
    def __init__(self, inst: Instance):
        self.inst = inst
        self.mj = -np.ones(inst.get_N(), dtype=int)
        self.m = -np.ones((2, inst.get_N()+inst.get_M()), dtype=int)
        for i in range(0, inst.get_M()):
            self.m[Node.Pre][inst.get_N()+i] = inst.get_N()+i
            self.m[Node.Suc][inst.get_N()+i] = inst.get_N()+i
        self.Cmax = 0
        self.i_Cmax = -1
        self.C = np.zeros(inst.get_M(), dtype=int)

    def reset(self):
        self.mj = -np.ones(self.inst.get_N(), dtype=int)
        self.m = -np.ones((2, self.inst.get_N()+self.inst.get_M()), dtype=int)
        for i in range(0, self.inst.get_M()):
            self.m[Node.Pre][self.inst.get_N() + i] = self.inst.get_N() + i
            self.m[Node.Suc][self.inst.get_N() + i] = self.inst.get_N() + i
        self.Cmax = 0
        self.i_Cmax = -1
        self.C = np.zeros(self.inst.get_M(), dtype=int)

    def get_makespan(self) -> int:
        return self.Cmax

    def get_C(self, m: int) -> int:
        return self.C[m]

    def get_suc(self, job: int) -> int:
        return self.m[Node.Suc][job]

    def get_pre(self, job: int) -> int:
        return self.m[Node.Pre][job]

    def get_job_machine(self, job: int) -> int:
        return self.mj[job]

    def get_idx_makespan(self) -> int:
        return self.i_Cmax

    def to_string(self):
        for i in range(self.inst.get_M()):
            print(f"M{i + 1} : ", end="")
            fj = self.m[Node.Suc][self.inst.get_N()+i]
            while fj < self.inst.get_N():
                print(fj + 1, end=" ")
                fj = self.m[Node.Suc][fj]
            print('\nC : ', self.C[i])
        print('\nCmax : ', self.Cmax, '\n')

    def insert_job(self, idx_m: int, job: int, pre: int):
        self.C[idx_m] += -self.inst.get_S(pre, self.m[Node.Suc][pre]) + \
                         self.inst.get_S(pre, job) + \
                         self.inst.get_S(job, self.m[Node.Suc][pre])
        suc = self.m[Node.Suc][pre]
        self.m[Node.Suc][pre] = job
        self.m[Node.Pre][job] = pre
        self.m[Node.Suc][job] = suc

        if self.C[idx_m] > self.Cmax:
            self.Cmax = self.C[idx_m]
            self.i_Cmax = idx_m

        self.mj[job] = idx_m

    def check_fact(self):

        print("------------------------------------")
        print("01) Verificando jobs em cada máquina.")
        print("------------------------------------")
        M = self.inst.get_M()
        J = self.inst.get_N()
        # armazena os indices dos jobs de cada máquina
        machine_idx_jobs = [[] for _ in range(M)]

        for i in range(M):
            fj = self.m[Node.Suc][J + i]
            while fj < J:
                machine_idx_jobs[i].append(fj)
                fj = self.m[Node.Suc][fj]

        machine_time = []
        jobs_used = []
        aux_m = 0
        for machine in machine_idx_jobs:
            aux_m += 1
            pre = J
            total = 0
            print(f"M{aux_m}: {[i + 1 for i in machine]}")
            itens = len(machine)
            aux_j = 0
            for job in machine:
                jobs_used.append(job)
                aux_j += 1
                if aux_j == itens:
                    job = J
                suc = job
                setup_time = self.inst.get_S(pre, suc)
                total += setup_time
                print(f"    ({pre + 1}, {job + 1}): {setup_time}")
                pre = suc
            machine_time.append(total)
            print(f"Total: {total}\n")

        cmax = max(machine_time)
        print(F"\nCMax: {cmax}")

        if cmax == self.Cmax:
            print(f"Cmax: {cmax}. OK")
        else:
            print(f"Cmax: {cmax} != {self.Cmax}. Errado")

        print("")
        print("------------------------------------")
        print("02) Verificando distribuição dos jobs.")
        print("------------------------------------")
        jobs = [i for i in range(J)]
        print(f"Jobs disponíveis: {[i + 1 for i in jobs]}")
        print(f"Jobs utilizados: { [i + 1 for i in jobs_used]}")

        if set(jobs) == set(jobs_used):
            print("Todos os jobs disponíveis foram usados. OK")
        else:
            print("Nem todos os jobs foram utilizados. ERRO")

        print("")
