import numpy as np
from Instance import *
from enum import IntEnum


class Node(IntEnum):
    Pre = 0
    Suc = 1


class Solution:
    def __init__(self, inst: Instance):
        self.inst = inst
        self.mj = -np.ones(inst.get_n() + inst.get_m(), dtype=int)
        self.m = -np.ones((2, inst.get_n() + inst.get_m()), dtype=int)
        for i in range(0, inst.get_m()):
            self.m[Node.Pre][inst.get_n() + i] = inst.get_n() + i
            self.m[Node.Suc][inst.get_n() + i] = inst.get_n() + i
        self.c = np.zeros(inst.get_m(), dtype=int)
        # armazena o numero de jobs em cada maquina
        self.n = np.zeros(inst.get_m(), dtype=int)
        self.cmax = 0
        self.cmax_idx = -1

        for i in range(self.inst.get_m()):
            self.mj[self.inst.get_n()+i] = i

    def reset(self):
        self.mj = -np.ones(self.inst.get_n() + self.inst.get_m(), dtype=int)
        self.m = -np.ones((2, self.inst.get_n() +
                          self.inst.get_m()), dtype=int)
        for i in range(0, self.inst.get_m()):
            self.m[Node.Pre][self.inst.get_n() + i] = self.inst.get_n() + i
            self.m[Node.Suc][self.inst.get_n() + i] = self.inst.get_n() + i
        self.c = np.zeros(self.inst.get_m(), dtype=int)
        self.n = np.zeros(self.inst.get_m(), dtype=int)
        self.cmax = 0
        self.cmax_idx = -1

        for i in range(self.inst.get_m()):
            self.mj[self.inst.get_n()+i] = i

    def get_makespan(self) -> int:
        return self.cmax

    def get_c(self, m: int) -> int:
        return self.c[m]

    def get_suc(self, job: int) -> int:
        return self.m[Node.Suc][job]

    def get_pre(self, job: int) -> int:
        return self.m[Node.Pre][job]

    def get_num_jobs_machine(self, machine: int) -> int:
        return self.n[machine]

    def get_job_machine(self, job: int) -> int:
        return self.mj[job]

    def get_makespan_idx(self) -> int:
        return self.cmax_idx

    def to_string(self):
        for i in range(self.inst.get_m()):
            print(f"M{i + 1} : ", end="")
            fj = self.m[Node.Suc][self.inst.get_n() + i]
            while fj < self.inst.get_n():
                print(fj + 1, end=" ")
                fj = self.m[Node.Suc][fj]
            print('\nC : ', self.c[i])
        print('\nCmax : ', self.cmax, '\n')

    def cut(self, job: int):  # corta a arco entre o job e o seu antecessor
        pre = self.m[Node.Pre][job]
        m = self.get_job_machine(job)

        # remove arco da esq
        self.c[m] -= self.inst.get_s(pre, job)

        self.m[Node.Pre][job] = -1
        self.m[Node.Suc][pre] = -1

        # check CMAX
        if self.c[m] != self.cmax:
            self.cmax_idx = np.argmax(self.c)
            self.cmax = self.c[self.cmax_idx]

    # fecha o arco
    def patch(self, pre: int, suc: int): 
        if self.get_job_machine(pre) != self.get_job_machine(suc):
            print("erro, as tarefas devem ser da mesma maquina")
            return

        # remove arco da esq
        m = self.get_job_machine(pre)
        self.c[m] += self.inst.get_s(pre, suc)

        self.m[Node.Pre][suc] = pre
        self.m[Node.Suc][pre] = suc

        # check CMAX
        if self.c[m] != self.cmax:
            self.cmax_idx = np.argmax(self.c)
            self.cmax = self.c[self.cmax_idx]

    def insert_job(self, m: int, job: int, pre: int):

        suc = self.m[Node.Suc][pre]
        # remove arco
        self.c[m] += -self.inst.get_s(pre, suc)
        # add arco da esq
        self.c[m] += self.inst.get_s(pre, job)
        # add arco da dir
        self.c[m] += self.inst.get_s(job, suc)

        self.m[Node.Pre][job] = pre
        self.m[Node.Suc][job] = suc
        self.m[Node.Suc][pre] = job
        self.m[Node.Pre][suc] = job

        # check CMAX
        if self.c[m] != self.cmax:
            self.cmax_idx = np.argmax(self.c)
            self.cmax = self.c[self.cmax_idx]
        self.mj[job] = m
        self.n[m] += 1

    def ejeta_job(self, m: int, job: int):

        suc = self.m[Node.Suc][job]
        pre = self.m[Node.Pre][job]

        # remove arco da esq
        self.c[m] -= self.inst.get_s(pre, job)
        # remove arco da dir
        self.c[m] -= self.inst.get_s(job, suc)
        # add arco
        self.c[m] += self.inst.get_s(pre, suc)

        self.m[Node.Suc][job] = -1
        self.m[Node.Pre][job] = -1
        self.m[Node.Suc][pre] = suc
        self.m[Node.Pre][suc] = pre

        # check CMAX
        if self.c[m] != self.cmax:
            self.cmax_idx = np.argmax(self.c)
            self.cmax = self.c[self.cmax_idx]
        self.mj[job] = -1
        self.n[m] -= 1

    def check_solution(self):
        ok = 1
        for m in range(self.inst.get_m()):
            job = self.inst.get_n() + m
            cm = self.inst.get_s(job, self.m[Node.Suc][job])
            job = self.m[Node.Suc][job]
            if self.mj[job] != m:
                print(
                    f"Erro de alocado do job {job} : maquina solu {self.mj[job]} maquina correta {m}")
                ok = 0
            while job < self.inst.get_n():
                cm += self.inst.get_s(job, self.m[Node.Suc][job])
                job = self.m[Node.Suc][job]
            if cm != self.c[m]:
                print("Erro no calculo do tempo total da maquina ",
                      m, " C solu: ", self.c[m], " C correto: ", cm)
                ok = 0
        if ok:
            print("Solution ok")

    def check_fact(self):

        print("------------------------------------")
        print("01) Soma tempos job até CMax.")
        print("------------------------------------\n")
        m = self.inst.get_m()
        n = self.inst.get_n()
        # add idx jobs para maq
        machine_idx_jobs = [[] for _ in range(m)]

        for i in range(m):
            fj = self.m[Node.Suc][n + i]
            while fj < n:
                machine_idx_jobs[i].append(fj)
                fj = self.m[Node.Suc][fj]

        machine_time = []
        jobs_used = []
        aux_m = 0
        for machine in machine_idx_jobs:
            aux_m += 1
            pre = n
            total = 0
            print(f"M{aux_m}: {[i + 1 for i in machine]}")
            itens = len(machine)
            aux_j = 0
            for job in machine:
                jobs_used.append(job)

                suc = job
                setup_time = self.inst.get_s(pre, suc)
                total += setup_time
                print(f"    ({pre + 1}, {job + 1}): {setup_time}")
                pre = suc
                if aux_j == itens - 1:
                    suc = n
                    setup_time = self.inst.get_s(pre, suc)
                    total += setup_time
                    print(f"    ({pre + 1}, {suc + 1}): {setup_time}")

                aux_j += 1
            machine_time.append(total)
            print(f"Total: {total}\n")

        cmax = max(machine_time)
        print("Resultado: ")
        if cmax == self.cmax:
            print(
                f"      OK. Valor correto Cmax para a configuração de máquinas x jobs: {cmax}")
        else:
            print(
                f"      Erro. Valor incorreto Cmax para a configuração de máquinas x jobs: {cmax} != {self.cmax}")

        print("")
        print("------------------------------------")
        print("02) Verificando se todos os jobs foram utilizados nas máquinas.")
        print("------------------------------------\n")
        jobs = [i for i in range(n)]

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
