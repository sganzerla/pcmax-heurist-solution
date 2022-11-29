import numpy as np
import pandas as pd
import copy
from enum import Enum
from Instance import *

class Solution:
    def __init__(self, inst : Instance):
      self.inst = inst;
      self.mj = -np.ones(inst.get_N(), dtype = int)
      self.m = -np.ones( (2,inst.get_N()+inst.get_M()), dtype = int)
      for i in range(0,inst.get_M()):
        self.m[0][inst.get_N()+i] = inst.get_N()+i
        self.m[1][inst.get_N()+i] = inst.get_N()+i
      self.Cmax  = 0
      self.i_Cmax  = -1
      self.C = np.zeros(inst.get_M(),dtype = int)
      
    def reset(self):
      self.mj = -np.ones(self.inst.get_N(), dtype = int)
      self.m = -np.ones( (2,self.inst.get_N()+self.inst.get_M()), dtype = int)
      for i in range(0,self.inst.get_M()):
        self.m[0][self.inst.get_N()+i] = self.inst.get_N()+i
        self.m[1][self.inst.get_N()+i] = self.inst.get_N()+i
      self.Cmax  = 0
      self.i_Cmax  = -1
      self.C = np.zeros(self.inst.get_M(),dtype = int)
    
    def get_makespan(self) -> int:
      return self.Cmax
    
    def get_C(self,m: int) -> int:
      return self.C[m]

    def get_suc(self,job: int) -> int:
      return self.m[1][job] 
    
    def get_pre(self,job: int) -> int:
      return self.m[0][job]
    
    def get_job_machine(self,job: int) -> int:
          return self.mj[job]

    def get_index_makespan(self) -> int:
      return self.i_Cmax
      
    def to_string(self):
        for i in range(self.inst.get_M()):
              print(f"M{i} : " , end ="")
              fj = self.m[1][self.inst.get_N()+i]
              while fj < self.inst.get_N():
                    print( fj, end=" " )
                    fj = self.m[1][fj]
              print('\nC : ',self.C[i])
        print('\nCmax : ',self.Cmax)
              
    def insert_job(self, index_m: int, job: int, pre: int):
      self.C[index_m] += self.inst.get_S(pre,job) - self.inst.get_S(pre,self.m[1][pre])
      self.C[index_m] += self.inst.get_S(job,self.m[1][pre])
      suc = self.m[1][pre]
      self.m[1][pre] = job      
      self.m[0][job] = pre
      self.m[1][job] = suc;
      
      if self.C[index_m] > self.Cmax:
            self.Cmax = self.C[index_m]
            self.i_Cmax = index_m
      self.mj[job] = index_m      
    