import numpy as np
import pandas as pd


class ConstrutiveSolution:
    def __init__(self, M: int, N: int, S: np.array):
        self.__M = M
        self.__N = N
        self.__S = pd.DataFrame(S).T
        self.__BM = self.__S.max().max()
        self.__Makespan = 0
        self.__Sol = self.__build_solution__()

    def get_makespan(self) -> int:
        return self.__Makespan

    def get_solution(self) -> np.array:
        return self.__Sol

    def get_max_value(self) -> int:
        return self.__BM

    def to_string(self):
        print(
            f"M: {self.__M}\nN: {self.__N}\nS: {self.__S}\nMax: {self.__BM}\nMakespan: {self.__Makespan}\nSolution: {self.__Sol}\n")

    def get_S(self, i: int, j: int) -> int:
        return self.__S[i][j]

    # retorna o indice da linha de menor valor da coluna selecionada
    def get_idx_min_by_col(self, col: int) -> int:
        return self.__S[col].idxmin()

    def get_S(self, i: int, j: int) -> int:
        return self.__S[i][j]

    def set_S(self, i: int, j: int, x: int):
        self.__S[i][j] = x

    def __build_solution__(self) -> list:

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
            row_idx = self.get_idx_min_by_col(n1)
            # menor valor de tempo de preparacao
            value_row = self.get_S(n1, row_idx)
            # altero o valor para não escolher novamente
            self.set_S(n1, row_idx, biggest_value1)
            # armazenando primeiro job a máquina
            machine_times[i].append({(n1, row_idx): value_row})
            # acumulando o primeiro valor
            total_time_machine[i] += value_row
            # informando o ultimo job de cada máquina
            last_job_machine[i] = row_idx
            # remove indice do jobs das opcoes disponiveis
            unrelated_jobs.remove(row_idx)

        # distribui os jobs na ordem que aparecem na máquina menos carregada
        for i in unrelated_jobs:
            # indice da máquina menos carregada
            idx_machine = total_time_machine.idxmin()
            # ultimo job adicionado da máquina
            last_job = last_job_machine[idx_machine]
            # valor do tempo de preparacao proximo job
            value_row = self.get_S(last_job, i)
            # informando o ultimo job de cada máquina
            last_job_machine[idx_machine] = i

            machine_times[idx_machine].append({(last_job, i): value_row})
            total_time_machine[idx_machine] += value_row

        # adiciona o tempo de encerramento em cada máquina com o último job
        for i in range(m):
            # ultimo job de cada máquina
            last_job = last_job_machine[i]
            # valor do ultimo job até tempo de
            value_row = self.get_S(last_job, n1)
            machine_times[i].append({(last_job, n1): value_row})
            total_time_machine[i] += value_row

        # atualiza o makespan
        self.__Makespan = np.max(total_time_machine)

        return machine_times
