import os
from optparse import OptionParser
from ConstructiveSolution import *
from LocalSearch import *
import time
import copy


def write_file(file_report, text):
    file = open(file_report, 'a')
    file.write(text)
    file.close()


if __name__ == "__main__":

    # python.exe .\ReportLPiii.py -s .\instance\

    parser = OptionParser()
    parser.add_option("-s", "--path", dest="path", type="string")

    (opts, _) = parser.parse_args()

    path = opts.path
    # output = opts.output

    files = []
    for (_, _, file) in os.walk(path):
        for f in file:
            files.append(f)

    n_files = len(files)
    aux = 1

    report_file = "report_lpiii_" + time.strftime("%H_%M_%S.csv", time.localtime())
    head = "idx; inst; m; j; cmax_init; time_init; "
    head += "cmax_iii; time_ls; reduction; \n"
    write_file(report_file, head)

    for file in files:

        print(f"({aux}/{n_files}) - {file}")
        ex = Extract(path + file)
        inst = Instance(ex)
        solu = Solution(inst)

        report = f"{aux}/{n_files}; {file}; {inst.get_m()}; {inst.get_n()}; "
        greedy = ConstructiveSolution(inst)

        start = time.time()
        greedy.build_greedy(solu)
        end = time.time()
        cmax = copy.copy(solu.get_makespan())
        report += f"{solu.get_makespan()}; {(end-start):.4f}; "

        ls = LocalSearch(inst)
        start = time.time()

        for i in range(inst.get_m()):
            ls.gen_insert(solu, i)
        report += f"{solu.get_makespan()}; "
        print("G_INS", solu.get_makespan())


        end = time.time()
        red = ((cmax - solu.get_makespan())/cmax)*100
        if red > 0:
            red = red * -1
        report += f"{(end - start):.4f}; {(red):.2f}; \n"
        print(f"time_ls: {(end - start):.4f}")
        print(f"reduction: {(red):.2f}%;")
        aux += 1
        write_file(report_file, report)
    print(f"File {report_file} created with success.\n")
