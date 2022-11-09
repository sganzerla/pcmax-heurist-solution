import pandas as pd


class InstanceData:
    def __init__(self, machines: int, jobs: int, times: list[int], setups: list[list[int]]):
        self.M = range(machines)
        self.J = range(jobs)
        self.T = times
        self.S = setups


def read_file(file) -> InstanceData:

    # gera um vetor com conteudo de cada linha em cada posição
    data = open(file, 'r').readlines()

    #-----------------machines ----------------------------#
    machines = int(data[0])

    # -----------------jobs ------------------------------#
    jobs = int(data[1])

    # --------------- times -------------------------------#
    # segunda linha em diante até linha 2 + quantidade de jobs
    str_times = ' '.join(str(i) for i in data[2: 2 + jobs])
    times = [int(i) for i in str_times.split() if i.isdigit()]

    # ------------------ setup --------------------------#
    # depois da 2 + n jobs + machines (zeros) até  total de linhas - (2 + n jobs + machines) tempos de setup
    jm = jobs + machines  # tarefas + maquinas dummys (linhas zeros)

    str_setups = ' '.join(str(i) for i in data[2 + jm: len(data) - 2 + jm])
    setups_list = [int(i) for i in str_setups.split() if i.isdigit()]
    setups_matrix = [setups_list[i::jm] for i in range(jm)]

    df = pd.DataFrame(setups_matrix)

    # apagando últimas linhas dummy
    df.drop(df.tail(machines).index, inplace=True)
    # apagando últimas colunas dummy
    index_column = [i for i in range(jobs + machines) if i >= jobs]
    df.drop(df.columns[index_column], axis=1, inplace=True)

    return InstanceData(machines, jobs, times, df.T)


if __name__ == "__main__":

    file = 's_g01_01_0009_010_02_01.txt'

    # extraindo dados de uma instância
    instance = read_file(file)

    print(f"Machine: {len(instance.M)}")
    print(f"Jobs: {len(instance.J)}")
    print(f"Times: {instance.T}")
    print("Matriz com Setups")
    print(pd.DataFrame(instance.S))
