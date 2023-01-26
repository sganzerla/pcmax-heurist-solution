# convert-instance

Programa para converter instâncias PCMAX do formato oriundo da tese do professor Felipe Muller para o formato convencionado abaixo:

* Primeira linha estão a quantidade de tarefas e quantidade de máquinas respectivamente
* Segunda linha até a quantidade de tarefas estão os tempos de processamento das tarefas
* A primeira linha após os tempos de processamento estão os tempos de preparação das máquinas quando iniciam em determinada posição. Por exemplo, abaixo a tarefa 1 saíndo na posição zero tem custo 18, se fosse a tarefa 2 tería 20 e assim sucessivamente:

    0 1 18
    0 2 20
    0 3 13
    0 4 2
    0 5 12
    0 6 13
    0 7 10
    0 8 10

## Como usar

Pode-se converter uma instância de forma isolada ou uma pasta inteira.

Se informar a opção `-u` (unique), o parâmetro é o endereço de uma única instância:

        python3 Main.py -u instance/001_struc_2_10_01

Se quiser converter uma pasta inteira, informe a opção `-a` (all), o parâmetro é o endereço da pasta raiz:

        python3 Main.py -a instance/
