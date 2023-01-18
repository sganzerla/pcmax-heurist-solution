from code.Instance import *
from code.Solution import *

class Neighborhood:

    def __init__(self, inst: Instance):
        self.inst = inst

    def insertion(self, solu: Solution):

        while True:
            best_delta = 0
            best_mov = []
            for i in range(self.inst.get_m()):
                if solu.get_c(i) < solu.get_makespan():
                    continue
                mi = self.inst.get_n()+i
                jobi = solu.get_suc(mi)
                while jobi != mi:
                    deltai = self.inst.get_s(
                        solu.get_pre(jobi), solu.get_suc(jobi))
                    deltai -= self.inst.get_s(solu.get_pre(jobi), jobi)
                    deltai -= self.inst.get_s(jobi, solu.get_suc(jobi))

                    if solu.get_c(i) + deltai > solu.get_makespan():
                        jobi = solu.get_suc(jobi)
                        continue
                    for j in range(self.inst.get_m()):
                        mj = self.inst.get_n()+j
                        if j == i or solu.get_suc(mj) == mj:
                            continue
                        jobj = mj
                        while True:
                            deltaj = -self.inst.get_s(jobj, solu.get_suc(jobj))
                            deltaj += self.inst.get_s(jobi, solu.get_suc(jobj))
                            deltaj += self.inst.get_s(jobj, jobi)

                            if solu.get_c(j) + deltaj > solu.get_makespan():
                                jobj = solu.get_suc(jobj)
                                if jobj == mj:
                                    break
                                continue

                            if deltai + deltaj < best_delta:
                                best_delta = deltai + deltaj
                                best_mov = [i, jobi, j, jobj]

                            jobj = solu.get_suc(jobj)
                            if jobj == mj:
                                break

                    jobi = solu.get_suc(jobi)

            if best_delta == 0:
                break

            solu.eject_job(best_mov[0], best_mov[1])
            solu.insert_job(best_mov[2], best_mov[1], best_mov[3])

    def swap(self, solu: Solution):
        while True:
            best_delta = 0
            best_mov = []
            for i in range(self.inst.get_m()):
                if solu.get_c(i) < solu.get_makespan():
                    continue
                mi = self.inst.get_n()+i
                jobi = solu.get_suc(mi)
                while jobi != mi:
                    for j in range(i+1, self.inst.get_m()):
                        mj = self.inst.get_n()+j
                        jobj = solu.get_suc(mj)
                        while jobj != mj:
                            deltaj = -self.inst.get_s(solu.get_pre(jobj), jobj)
                            deltaj -= self.inst.get_s(jobj, solu.get_suc(jobj))
                            deltaj += self.inst.get_s(solu.get_pre(jobj), jobi)
                            deltaj += self.inst.get_s(jobi, solu.get_suc(jobj))

                            deltai = -self.inst.get_s(solu.get_pre(jobi), jobi)
                            deltai -= self.inst.get_s(jobi, solu.get_suc(jobi))
                            deltai += self.inst.get_s(solu.get_pre(jobi), jobj)
                            deltai += self.inst.get_s(jobj, solu.get_suc(jobi))

                            if solu.get_c(j) + deltaj > solu.get_makespan() or \
                               solu.get_c(i) + deltai > solu.get_makespan():
                                jobj = solu.get_suc(jobj)
                                if jobj == mj:
                                    break
                                continue

                            if solu.get_c(j) + deltaj < solu.get_makespan() or \
                               solu.get_c(i) + deltai < solu.get_makespan():
                                if deltai + deltaj <= best_delta:
                                    best_delta = deltai + deltaj
                                    best_mov = [i, jobi, j, jobj]

                            jobj = solu.get_suc(jobj)

                    jobi = solu.get_suc(jobi)

            if best_delta == 0:
                break

            prei = solu.get_pre(best_mov[1])
            prej = solu.get_pre(best_mov[3])
            solu.eject_job(best_mov[0], best_mov[1])
            solu.eject_job(best_mov[2], best_mov[3])
            solu.insert_job(best_mov[0], best_mov[3], prei)
            solu.insert_job(best_mov[2], best_mov[1], prej)

    def gen_insert(self, solu: Solution, m: int) -> bool:
        if solu.get_num_jobs_machine(m) < 3:
            print("insercao generalizada nao pode ser aplicada, nr insuficientes de tarefas: 3")
            return False

        ok = False

        while True:
            job1 = self.inst.get_n() + m
            job2 = solu.get_suc(job1)
            job3 = solu.get_suc(job2)

            best_delta = 0
            best_move = []
            for _ in range(solu.get_num_jobs_machine(m)-3):
                for _ in range(1, solu.get_num_jobs_machine(m)-2):
                    for _ in range(2, solu.get_num_jobs_machine(m)-1):
                        delta = -self.inst.get_s(solu.get_pre(job1), job1)
                        delta -= self.inst.get_s(solu.get_pre(job2), job2)
                        delta -= self.inst.get_s(solu.get_pre(job3), job3)

                        delta += self.inst.get_s(solu.get_pre(job1), job2)
                        delta += self.inst.get_s(solu.get_pre(job2), job3)
                        delta += self.inst.get_s(solu.get_pre(job3), job1)

                        if delta < best_delta:
                            best_delta = delta
                            best_move = [job1, job2, job3]
                            job3 = solu.get_suc(job3)

                    job2 = solu.get_suc(job2)
                    job3 = solu.get_suc(job2)

                job1 = solu.get_suc(job1)
                job2 = solu.get_suc(job1)
                job3 = solu.get_suc(job2)

            if best_delta < 0:
                pre1 = solu.get_pre(best_move[0])
                pre2 = solu.get_pre(best_move[1])
                pre3 = solu.get_pre(best_move[2])

                solu.cut(best_move[0])
                solu.cut(best_move[1])
                solu.cut(best_move[2])

                solu.patch(pre1, best_move[1])
                solu.patch(pre2, best_move[2])
                solu.patch(pre3, best_move[0])

                ok = True
            else:
                break

        return ok
