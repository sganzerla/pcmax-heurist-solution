class InstanceData:
    def __init__(self, machines: int, jobs: int, times: list[int], preparation: list[list[int]]):
        self.M = range(machines)
        self.J = range(jobs)
        self.T = times
        self.P = preparation


def read_file(file) -> InstanceData:

    # gera um vetor com conteudo de cada linha em cada posição
    data = open(file, 'r').readlines()

    #-----------------machines ----------------------------#
    machines = int(data[0])

    # -----------------jobs ------------------------------#
    jobs = int(data[1])

    # --------------- times -------------------------------#
    # maquinas tem um tempo adicional de entrada e saida nas tarefas
    # terceira linha até linha 2 + quantidade de jobs + quantidade de máquinas são os tempos
    string_times = ' '.join(str(item) for item in data[2: 2 + jobs + 2])
    times = [int(i) for i in string_times.split() if i.isdigit()]
    source = times[jobs]
    sink =  times[jobs + 1]
    print(source, sink)
    # TODO arrumar isso


if __name__ == "__main__":

    file = 's_g01_01_0009_010_02_01.txt'
    instance = read_file(file)
