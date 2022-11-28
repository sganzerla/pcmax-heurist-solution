import numpy as np
import pandas as pd
import copy
from enum import Enum


class Strategy(Enum):
    NEXT = 1
    BEST = 2


class ConstrutiveSolution:
    def __init__(self, M: int, N: int, S: np.array, strategy: Strategy = Strategy.BEST):
        self.__M = M
        self.__N = N
        self.__S = pd.DataFrame(S).T
        self.__SClone = copy.copy(self.__S)
        self.__Max = self.__S.max().max()
        self.__Makespan = 0
        self.__strategy = strategy
        self.__Sol = self.__build_solution__(self.__strategy)

    def get_makespan(self) -> int:
        return self.__Makespan

    def get_solution(self) -> np.array:
        return self.__Sol

    def get_max_value(self) -> int:
        return self.__Max

    def to_string(self):
        print(
            f"M: {self.__M}\nN: {self.__N}\nS: {self.__S}\nMax: {self.__Max}\nStrategy: {self.__strategy}\nMakespan: {self.__Makespan}\nSolution: {self.__Sol}\n")

    # retorna o indice da coluna de menor valor da linha selecionada
    def __get_idx_min_by_row__(self, row: int) -> int:
        return self.__SClone.iloc[row].idxmin()

    def __get_S__(self, i: int, j: int) -> int:
        return self.__SClone[i][j]

    def __update_S__(self, i: int, j: int, x: int):
        self.__SClone[i][j] = x

    def __build_solution__(self, strategy: Strategy) -> list:

        m = self.__M
        n1 = self.__N
        # cria matriz n linhas com zero colunas
        machine_times = [[] for _ in range(m)]
        # lista de jobs disponíveis
        unrelated_jobs = [i for i in range(n1)]
        # acumular o tempo total em cada máquina
        total_time_machine = pd.Series(np.zeros(m, dtype=int))
        # ultimo job adicionado em cada máquina
        last_job_machine = pd.Series(np.zeros(m, dtype=int))
        # obtendo o maior valor da matriz
        biggest_value1 = self.get_max_value() + 1

        # escolhe o job com menor tempo de preparação inicial para cada máquina e adiciona os tempo de preparação
        for i in range(m):
            # indice da coluna com menor tempo de preparacao
            col_idx = self.__get_idx_min_by_row__(n1)
            # menor valor de tempo de preparacao
            value_row = self.__get_S__(col_idx, n1)
            # altero o valor para não escolher novamente
            self.__update_S__(col_idx, n1, biggest_value1)
            # armazenando primeiro job a máquina
            machine_times[i].append({(n1, col_idx): value_row})
            # acumulando o primeiro valor
            total_time_machine[i] += value_row
            # informando o ultimo job de cada máquina
            last_job_machine[i] = col_idx
            # remove indice do jobs das opcoes disponiveis
            unrelated_jobs.remove(col_idx)

        if strategy == Strategy.NEXT:
            # distribui os jobs na ordem que aparecem na máquina menos carregada
            for i in unrelated_jobs:
                # indice da máquina menos carregada
                idx_machine = total_time_machine.idxmin()
                # ultimo job adicionado da máquina
                last_job = last_job_machine[idx_machine]
                # valor do tempo de preparacao proximo job
                value_row = self.__get_S__(last_job, i)
                # informando o ultimo job de cada máquina
                last_job_machine[idx_machine] = i

                machine_times[idx_machine].append({(last_job, i): value_row})
                total_time_machine[idx_machine] += value_row

        else:
            # distribui os jobs na ordem que aparecem na máquina menos carregada
            jobs = len(unrelated_jobs)

            for _ in range(jobs):
                # indice da máquina menos carregada
                idx_machine = total_time_machine.idxmin()
                # ultimo job adicionado da máquina
                last_job = last_job_machine[idx_machine]

                best_job = self.__Max
                best_job_idx = 0
                for i in unrelated_jobs:
                    # valor do tempo de preparacao proximo job
                    value_row = self.__get_S__(last_job, i)
                    if value_row < best_job:
                        best_job = value_row
                        best_job_idx = i
                    # informando o ultimo job de cada máquina

                last_job_machine[idx_machine] = best_job_idx

                machine_times[idx_machine].append(
                    {(last_job, best_job_idx): best_job})
                total_time_machine[idx_machine] += best_job
                # remove indice do jobs das opcoes disponiveis
                unrelated_jobs.remove(best_job_idx)
                # resetando variaveis auxiliares
                best_job = self.__Max
                best_job_idx = 0

        # adiciona o tempo de encerramento em cada máquina com o último job
        for i in range(m):
            # ultimo job de cada máquina
            last_job = last_job_machine[i]
            # valor do ultimo job até tempo de
            value_row = self.__get_S__(last_job, n1)
            machine_times[i].append({(last_job, n1): value_row})
            total_time_machine[i] += value_row

            # atualiza o makespan
        self.__Makespan = np.max(total_time_machine)

        return machine_times
