import pandas as pd
from optparse import OptionParser
import time
import os
import numpy as np


class SolutionData:
    def __init__(self, sol: list, fo: int, time_report: float):
        self.sol = sol
        self.fo = fo
        self.time_report = time_report

    def save_to_file(self, file):
        write_file(
            file, f"{self.time_report}; {self.fo}; {self.sol}; "
        )


class InstanceData:
    def __init__(self, machines: int, jobs: int, times: list, setups: list, time_report: float):
        self.M = range(machines)
        self.J = range(jobs)
        self.T = times
        self.S = setups
        self.time_report = time_report

    def save_to_file(self, file):
        write_file(
            file, f" {instance.time_report}; {len(instance.M)}; {len(instance.J)}; ")


def write_file(file_report, text):
    file = open(file_report, 'a')
    file.write(text)
    file.close()


def extract_machines(data):
    machines = int(data[0])
    return machines


def extract_jobs(data):
    jobs = int(data[1])
    return jobs


def extract_times(data, jobs):
    # segunda linha em diante até linha 2 + quantidade de jobs
    str_times = ' '.join(str(i) for i in data[2: 2 + jobs])
    times = [int(i) for i in str_times.split() if i.isdigit()]
    return times


def extract_setup_matrix(data, jm):
    # depois da 2 + n jobs + machines (zeros) até  total de linhas - (2 + n jobs + machines) tempos de setup
    str_setups = ' '.join(str(i) for i in data[2 + jm: len(data) - 2 + jm])
    setups_list = [int(i) for i in str_setups.split() if i.isdigit()]
    setups_matrix = [setups_list[i::jm] for i in range(jm)]
    return setups_matrix


def remove_excess_cell(machines, jobs, setups_matrix):
    df = pd.DataFrame(setups_matrix)

    # deixa apenas 1 coluna de tempo de preparacao
    df.drop(df.tail(machines - 1).index, inplace=True)

    # deixa apenas 1 coluna de tempo de preparacao
    index_column = [i for i in range(jobs + machines) if i - 1 >= jobs]
    df.drop(df.columns[index_column], axis=1, inplace=True)
    return df


def read_file(file) -> InstanceData:

    # marcando o tempo
    time_start = time.time()

    # gera um vetor com conteudo de cada linha em cada posição
    data = open(file, 'r').readlines()

    machines = extract_machines(data)

    jobs = extract_jobs(data)

    times = extract_times(data, jobs)

    # tarefas + maquinas dummys (linhas zeros)
    setups_matrix = extract_setup_matrix(data, jobs + machines)

    df = remove_excess_cell(machines, jobs, setups_matrix)

    M1 = join_setup_time(times, df)

    end = time.time()

    return InstanceData(machines, jobs, times, pd.DataFrame(M1), end - time_start)


def join_setup_time(times, df):

    # soma 1 da coluna fake
    t = len(times) + 1
    # transpoe matriz
    df = df.T

    M1 = np.zeros((t, t), dtype=int)
    M1[0][0] = df[0][0]
    for i in range(t):
        for j in range(t):
            # diagonal, ultima linha e ultima coluna permanecem o mesmo valor
            if i == j or i == t - 1 or j == t - 1:
                M1[i][j] = df[j][i]
            else:
                M1[i][j] = df[j][i] + int(times[j])
    return M1


def get_params():
    parser = OptionParser()
    parser.add_option("-s", "--path", dest="path", type="string")
    parser.add_option("-o", "--output", dest="output", type="string")

    (opts, _) = parser.parse_args()

    path = opts.path
    output = opts.output

    return path, output


def build_construtive(instance: InstanceData):

    # marcando o tempo
    time_start = time.time()

    matrix = np.array(instance.S, dtype=int)

    # cria matriz n linhas com zero colunas
    machine_times = [[] for _ in instance.M]

    # acumular o tempo total em cada máquina
    total_time_machine = np.zeros(len(instance.M), dtype=int)

    for i in range(len(matrix)):
        # seleciona só uma linha da matriz e ignora as colunas do setup
        row = matrix[i][:len(instance.J)]

        # menor elemento da linha
        min_job = np.amin(row)
        # indice do menor elemento
        idx_min_job = int(np.where(row == min_job)[0][0])

        # valor da máquina menos carregada
        maq = np.min(total_time_machine)
        # indice da máquina menos carregada
        idx_machine = int(np.where(total_time_machine == maq)[0][0])

        # quando máquina só tem um item, acumulo o tempo de preparacao inicial
        if len(machine_times[idx_machine]) == 1:
            first_job: dict = machine_times[idx_machine][0]
            _, y  = list(first_job.keys())[0]
            total_time_machine[idx_machine] += matrix[len(instance.J)][y]
            
        # acumular tempo do job a maquina menos carregada
        total_time_machine[idx_machine] += min_job

        # adicionando o job ao conjunto de tarefas da máquina
        machine_times[idx_machine].append({(i, idx_min_job): min_job})

    makespan = np.max(total_time_machine)
    end = time.time()
    return SolutionData(machine_times, makespan, end - time_start)


if __name__ == "__main__":

    # para rodar o programa executar o comando
    # python extract_instance.py -s path_instance -o output_path + filename
    path, output = get_params()

    files = []
    for (root, dirs, file) in os.walk(path):
        for f in file:
            files.append(f)

    n_files = len(files)
    aux = 1

    # coloca o cabeçalho no relatório, colunas separadas por ponto e vírgula e o fim da linha indicado \n
    write_file(
        output, "index; instance; time_extract_data; machines; jobs; time_construtive; fo; solution; \n")

    for file in files:
        print(f"({aux}/{n_files})")

        # escrevendo identificador da instancia
        write_file(output, f"({aux}/{n_files}); {file};")

        # extraindo dados de uma instância
        instance = read_file(path + file)

        # escrevendo dados extraidos da instancia
        instance.save_to_file(output)

        # criar método construtivo
        constr = build_construtive(instance)

        constr.save_to_file(output)

        # criar método busca local
        # write_file( dados do método busca local, lembrar de colocar o nome das colunas fora do laço)

        write_file(output, "\n")
        aux += 1
