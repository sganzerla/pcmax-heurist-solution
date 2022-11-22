import pandas as pd
from optparse import OptionParser

class InstanceData:
    def __init__(self, machines: int, jobs: int, times: list, setups: list):
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

    # deixando apenas uma linha dummy
    df.drop(df.tail(machines - 1).index, inplace=True)
    # deixando apenas uma coluna dummy
    index_column = [i for i in range(jobs + machines) if i - 1 >= jobs]
    df.drop(df.columns[index_column], axis=1, inplace=True)



    return InstanceData(machines, jobs, times, df.T)




if __name__ == "__main__":

    # para rodar o programa executar o comando
    # python extract_instance.py -r s_g01_01_0009_010_02_01.txt
    parser = OptionParser()
    parser.add_option("-r", "--file", dest= "file", type="string")
    
    (opts, args ) = parser.parse_args()
    print(f"Instance{opts.file}")
    file = opts.file
    # extraindo dados de uma instância
    instance = read_file(file)

    print(f"Machine: {len(instance.M)}")
    print(f"Jobs: {len(instance.J)}")
    print(f"Times: {instance.T}")
    print("Matriz com Setups")
    print(pd.DataFrame(instance.S))
