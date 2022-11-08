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
    string_times = ' '.join(str(item) for item in data[2: 2 + jobs])
    times = [int(i) for i in string_times.split() if i.isdigit()]

    # depois da 2 + n jobs linhas até  2 + n jobs + 2 tem os tempos de inicio e saida das máquinas
    string_start_exit = ' '.join(str(item)
                                 for item in data[2 + jobs: 2 + jobs + 2])
    start_exit = [int(i) for i in string_start_exit.split() if i.isdigit()]

    times.insert(0, start_exit[0])  # adiciona o tempo de entrada
    times.append(start_exit[1])  # adiciona  o tempo de saida

    # ------------------ setup --------------------------#
    # depois da 2 + n jobs + 2 linhas até  total de linhas - (2 + n jobs + 2) tempos de setup
    string_setups = ' '.join(str(item)
                             for item in data[2 + jobs + 2: len(data) - 2 + jobs + 2])
    setups_list = [int(i) for i in string_setups.split() if i.isdigit()]
    setups_matrix = [setups_list[i::jobs + 2] for i in range(jobs + 2)]

    return InstanceData(machines, jobs, times, setups_matrix)


if __name__ == "__main__":

    file = 's_g01_01_0009_010_02_01.txt'

    # extraindo dados de uma instância
    instance = read_file(file)

    # TODO 
    # usar os dados da instance com alguma heurística
