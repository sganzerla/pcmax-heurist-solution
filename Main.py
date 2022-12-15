import os
from optparse import OptionParser

from ConstructiveSolution import *
from LocalSearch import *


if __name__ == "__main__":

    # python.exe .\Main.py -s .\instance_one\

    parser = OptionParser()
    parser.add_option("-s", "--path", dest="path", type="string")
    # parser.add_option("-o", "--output", dest="output", type="string")

    (opts, _) = parser.parse_args()

    path = opts.path

    # add path root com inst


    ex = Extract(path)
    inst = Instance(ex)
    solu = Solution(inst)

    greedy = ConstructiveSolution(inst)
    ls = LocalSearch(inst)
    
    #greedy.build_naive(solu)
    greedy.build_greedy(solu)
    solu.to_string()
    
    
    print("================ Insertion =============") 
    ls.insertion(solu)        
    print(solu.get_makespan())
    solu.check_solution() 

    print("================ Swap      =============") 
    ls.swap(solu)        
    print(solu.get_makespan())
    solu.check_solution() 
   
    print("================ 3-opt=============") 
    for m in range(inst.get_m()) : 
        ls.opt3(solu, m)
    print(solu.get_makespan())
    solu.check_solution()

    print("\n\n") 
    solu.to_string()

    r = open('pontos.txt', 'w')
    r.write(str(inst.get_m())+" "+str(inst.get_n())+"\n")
#    for i in range(inst.get_n()):
#        r.write(str(inst.get_p(i))+"\n")

    for i in range(inst.get_n()):
        r.write("0 " + str(i+1) + " " + str(inst.get_s(inst.get_n(),i))+"\n") 
        
    for i in range(inst.get_n()):
        for j in range(inst.get_n()):
            if j == i:
               continue
            r.write(str(i+1) +" " + str(j+1) + " " + str(inst.get_s(i,j)) +"\n") 
    
    for i in range(inst.get_n()):
        r.write(str(i+1) + " 0 " + str(inst.get_s(i,inst.get_n()))+"\n") 
                
    r.close()



