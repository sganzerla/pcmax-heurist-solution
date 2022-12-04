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

    def insert_job(self, m: int, job: int, pre: int):

        suc = self.m[Node.Suc][pre]
        # remove arco
        self.C[m] += -self.inst.get_S(pre, suc)

        # adiciona arco da esquerda
        self.C[m] += self.inst.get_S(pre, job)

        # adiciona arco da direita
        self.C[m] += self.inst.get_S(job, suc)
        
        self.m[Node.Suc][pre] = job
        self.m[Node.Pre][job] = pre
        self.m[Node.Suc][job] = suc

        # precisa atualizar o valor do CMAX quando for menor ou maior
        if self.C[m] != self.Cmax:
            self.i_Cmax = np.argmax(self.C)
            self.Cmax = max(self.C)

        self.mj[job] = m

    def check_solution(self):
        ok = 1
        for m in range(self.inst.get_M()):
            job = self.inst.get_N()+m
            cm = self.inst.get_S(job, self.m[Node.Suc][job])
            job = self.m[Node.Suc][job]
            if self.mj[job] != m:
                print(
                    f"Erro de alocado do job {job} : maquina solu {self.mj[job]} maquina correta {m}")
                ok = 0
            while job < self.inst.get_N():
                cm += self.inst.get_S(job, self.m[Node.Suc][job])
                job = self.m[Node.Suc][job]
            if cm != self.C[m]:
                print("Erro no calculo do tempo total da maquina ",
                      m, " C solu: ", self.C[m], " C correto: ", cm)
                ok = 0
        if ok:
            print("Solution ok")

    def check_fact(self):

        print("------------------------------------")
        print("01) Somando os tempos de cada job nas máquinas e comparando com CMax.")
        print("------------------------------------\n")
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

                suc = job
                setup_time = self.inst.get_S(pre, suc)
                total += setup_time
                print(f"    ({pre + 1}, {job + 1}): {setup_time}")
                pre = suc
                if aux_j == itens - 1:
                    suc = J
                    setup_time = self.inst.get_S(pre, suc)
                    total += setup_time
                    print(f"    ({pre + 1}, {suc + 1}): {setup_time}")

                aux_j += 1
            machine_time.append(total)
            print(f"Total: {total}\n")

        cmax = max(machine_time)
        print("Resultado: ")
        if cmax == self.Cmax:
            print(
                f"      OK. Valor correto Cmax para a configuração de máquinas x jobs: {cmax}")
        else:
            print(
                f"      Erro. Valor incorreto Cmax para a configuração de máquinas x jobs: {cmax} != {self.Cmax}")

        print("")
        print("------------------------------------")
        print("02) Verificando se todos os jobs foram utilizados nas máquinas.")
        print("------------------------------------\n")
        jobs = [i for i in range(J)]

        print(f"Jobs disponíveis: {[i + 1 for i in jobs]}")
        print(f"Jobs utilizados: { [i + 1 for i in jobs_used]}\n")
        print("Resultado:")
        if set(jobs) == set(jobs_used):
            print(
                f"    OK. Todos os jobs {len(jobs)} disponíveis foram usados.")
        else:
            print("     Erro. Nem todos os jobs foram utilizados na solução.")
            diff = set(jobs).difference(set(jobs_used))
            print(f"{[i + 1 for i in diff]}")

        print("")
