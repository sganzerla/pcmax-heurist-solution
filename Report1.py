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

    # python.exe .\Report1.py -s .\instance\

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
    
    report_file = "report_1_" + time.strftime("%H_%M_%S.csv", time.localtime())
    head = "idx; inst; m; j; cmax_init; idx_cmax_init; time_init; "
    head += "cmax_g_ins; idx_cmax_g_ins; cmax_ins; idx_cmax_ins; cmax_swap; idx_cmax_swap; "
    head += "cmax_ins; idx_cmax_ins; cmax_swap; idx_cmax_swap; cmax_g_ins; idx_cmax_g_ins; "
    head += "time; reduction; \n"
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
        report += f"{solu.get_makespan()}; {solu.get_makespan_idx()}; {end-start}; "
        
        ls = LocalSearch(inst)
        start = time.time()
        for i in range(inst.get_m()):
            ls.gen_insert(solu, i)
        print("G_INS", solu.get_makespan(), solu.get_makespan_idx())
        report += f"{solu.get_makespan()}; {solu.get_makespan_idx()}; "
        ls.insertion(solu)
        report += f"{solu.get_makespan()}; {solu.get_makespan_idx()}; "
        print("INS:", solu.get_makespan(), solu.get_makespan_idx())
        ls.swap(solu)
        report += f"{solu.get_makespan()}; {solu.get_makespan_idx()}; "
        print("SWAP", solu.get_makespan(), solu.get_makespan_idx())
        ls.insertion(solu)
        report += f"{solu.get_makespan()}; {solu.get_makespan_idx()}; "
        print("INS", solu.get_makespan(), solu.get_makespan_idx())
        ls.swap(solu)
        report += f"{solu.get_makespan()}; {solu.get_makespan_idx()}; "
        print("SWAP", solu.get_makespan(), solu.get_makespan_idx())
        for i in range(inst.get_m()):
            ls.gen_insert(solu, i)
        report += f"{solu.get_makespan()}; {solu.get_makespan_idx()}; "
        print("G_INS", solu.get_makespan(), solu.get_makespan_idx())
        end = time.time()
        report += f"{(end - start)}; {(((cmax - solu.get_makespan())/cmax)*100):.2f}%; \n"
        print(f"time: {(end - start)}")
        print(f"reduction: {(((cmax - solu.get_makespan())/cmax)*100):.2f}%;")
        aux += 1
        write_file(report_file, report)
    print(f"File {report_file} created with success.\n")