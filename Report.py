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

    # python.exe .\Main.py -s .\instance_one\

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
    
    report_file = "report_" + time.strftime("%H_%M_%S.csv", time.localtime())
    head = "index; instance; mach; jobs; fo_constr; idx_m_fo_constr; time_constr; "
    head += "fo_insert; idx_m_fo_insert; time_insert; "
    head += "fo_2opt; idx_m_fo_2opt; time_2opt; "
    head += "fo_3opt; idx_m_fo_3opt; time_3opt; \n"
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
        report += f"{solu.get_makespan()}; {solu.get_makespan_idx()}; {end-start}; "
        
        ls = LocalSearch(inst)
        
        print("================ Insertion =============")
        sol_a = copy.copy(solu)
        start = time.time()
        ls.insertion(sol_a)
        end = time.time()
        report += f"{sol_a.get_makespan()}; {sol_a.get_makespan_idx()}; {end-start}; "    
        
        print("================ 2Opt-Swap =============")
        sol_b = copy.copy(solu)
        start = time.time()
        ls.swap(sol_b)
        end = time.time()
        report += f"{sol_b.get_makespan()}; {sol_b.get_makespan_idx()}; {end-start}; "    

        print("================ 3Opt =============")
        sol_c = copy.copy(solu)
        start = time.time()
        ls.opt3(sol_c, sol_c.get_makespan_idx())
        end = time.time()
        report += f"{sol_c.get_makespan()}; {sol_c.get_makespan_idx()}; {end-start}; \n"  
        
        print(f"-------------------------------------------------------------------------------------------------------------------------- \n")
        aux += 1
        write_file(report_file, report)
    print(f"File {report_file} created with success.\n")