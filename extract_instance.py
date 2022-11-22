import pandas as pd
from optparse import OptionParser
import time


class InstanceData:
    def __init__(self, machines: int, jobs: int, times: list, setups: list):
        self.M = range(machines)
        self.J = range(jobs)
        self.T = times
        self.S = setups


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

    # gera um vetor com conteudo de cada linha em cada posição
    data = open(file, 'r').readlines()

    machines = extract_machines(data)

    jobs = extract_jobs(data)

    times = extract_times(data, jobs)

    # tarefas + maquinas dummys (linhas zeros)
    setups_matrix = extract_setup_matrix(data, jobs + machines)

    df = remove_excess_cell(machines, jobs, setups_matrix)

    # transpoe matriz
    df = df.T

    # soma 1 da coluna fake
    t = len(times) + 1

    M1 = [[0 for _ in range(t)] for _ in range(t)]
    M1[0][0] = df[0][0]
    for i in range(t):
        for j in range(t):
            if i == j or i == t - 1 or j == t - 1:
                M1[i][j] = df[j][i] + 0
            else:
                M1[i][j] = df[j][i] + int(times[j])

    return InstanceData(machines, jobs, times, pd.DataFrame(M1))


if __name__ == "__main__":

    # para rodar o programa executar o comando
    # python extract_instance.py -r s_g01_01_0009_010_02_01.txt
    parser = OptionParser()
    parser.add_option("-r", "--file", dest="file", type="string")

    (opts, args) = parser.parse_args()
    print(f"Instance = {opts.file}", end=" | ")
    file = opts.file

    # marcando o tempo
    start = time.time()
    instance = read_file(file)
    # extraindo dados de uma instância
    end = time.time()
    
    print(f"Time Extract Data = {end - start}", end=" | ")
    print(f"Machine = {len(instance.M)}", end = " | ")
    print(f"Jobs = {len(instance.J)}", end = " | ")

