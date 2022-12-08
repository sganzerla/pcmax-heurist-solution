from Instance import Instance
from Solution import Solution

class LocalSearch:

    def __init__(self, inst: Instance):
        self.inst = inst


    def insertion(self,solu : Solution):
      
       while True: 
          best_delta = 0
          best_mov = [] 
          for i in range(self.inst.get_m()):
             if solu.get_c(i) < solu.get_makespan():
                continue
             mi = self.inst.get_n()+i
             jobi =solu.get_suc(mi)
             while jobi != mi:
                   deltai = self.inst.get_s(solu.get_pre(jobi),solu.get_suc(jobi)) 
                   deltai -= self.inst.get_s(solu.get_pre(jobi),jobi) 
                   deltai -= self.inst.get_s(jobi,solu.get_suc(jobi)) 
                   
                   if solu.get_c(i) + deltai > solu.get_makespan():
                      jobi = solu.get_suc(jobi)
                      continue
                   for j in range(self.inst.get_m()):
                      mj = self.inst.get_n()+j
                      if j == i or solu.get_suc(mj) == mj: 
                            continue
                      jobj = mj 
                      while True:  
                            deltaj = -self.inst.get_s(jobj,solu.get_suc(jobj))
                            deltaj += self.inst.get_s(jobi,solu.get_suc(jobj))
                            deltaj += self.inst.get_s(jobj,jobi)
                            
                            if solu.get_c(j) + deltaj > solu.get_makespan():
                               jobj = solu.get_suc(jobj)
                               if jobj == mj:
                                 break
                               continue
                         
                            if deltai + deltaj < best_delta:
                               best_delta = deltai + deltaj 
                               best_mov = [i, jobi, j, jobj]
                               
                            jobj = solu.get_suc(jobj)   
                            if jobj == mj:
                              break

                   jobi = solu.get_suc(jobi)         
          
          print(best_delta)
          print(best_mov)
          if best_delta == 0:
             break

          solu.ejeta_job(best_mov[0],best_mov[1])
          solu.insert_job(best_mov[2],best_mov[1],best_mov[3])
            
    def swap(self,solu : Solution):
          
       while True: 
          best_delta = 0
          best_mov = [] 
          for i in range(self.inst.get_m()):
             if solu.get_c(i) < solu.get_makespan():
                continue
             mi = self.inst.get_n()+i
             jobi =solu.get_suc(mi)
             while jobi != mi:
                   for j in range(i+1, self.inst.get_m()):
                      mj = self.inst.get_n()+j
                      jobj = solu.get_suc(mj)
                      while jobj != mj:  
                            deltaj = -self.inst.get_s(solu.get_pre(jobj),jobj)
                            deltaj -= self.inst.get_s(jobj,solu.get_suc(jobj))
                            deltaj += self.inst.get_s(solu.get_pre(jobj),jobi)
                            deltaj += self.inst.get_s(jobi,solu.get_suc(jobj))
                            
                            deltai = -self.inst.get_s(solu.get_pre(jobi),jobi) 
                            deltai -= self.inst.get_s(jobi,solu.get_suc(jobi)) 
                            deltai += self.inst.get_s(solu.get_pre(jobi),jobj)
                            deltai += self.inst.get_s(jobj,solu.get_suc(jobi))
                            
                            if solu.get_c(j) + deltaj > solu.get_makespan() or \
                               solu.get_c(i) + deltai > solu.get_makespan():
                               jobj = solu.get_suc(jobj)
                               if jobj == mj:
                                 break
                               continue
                         
                            if solu.get_c(j) + deltaj < solu.get_makespan() or \
                               solu.get_c(i) + deltai < solu.get_makespan():
                               if deltai + deltaj <= best_delta: 
                                  best_delta = deltai + deltaj 
                                  best_mov = [i, jobi, j, jobj]
                               
                            jobj = solu.get_suc(jobj)   

                   jobi = solu.get_suc(jobi)         
          
          print(best_delta)
          print(best_mov)
          if best_delta == 0:
             break

          prei = solu.get_pre(best_mov[1])
          prej = solu.get_pre(best_mov[3])
          solu.ejeta_job(best_mov[0], best_mov[1])
          solu.ejeta_job(best_mov[2], best_mov[3])
          solu.insert_job(best_mov[0], best_mov[3], prei)
          solu.insert_job(best_mov[2], best_mov[1], prej)
         
                
