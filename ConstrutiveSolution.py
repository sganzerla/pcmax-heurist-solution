import numpy as np
import pandas as pd
import copy
from enum import Enum
from Solution import *
from Instance import *
import random
class ConstrutiveSolution:
    def __init__(self, inst : Instance, solu : Solution): 
        self.inst = inst
        self.solu = solu

    def build_naive(self):
        jobs = [ i for i in range(self.inst.get_N())]
        random.shuffle(jobs) 
       
        for i in range(self.inst.get_N()):
            m = random.randint(0,self.inst.get_M()-1)
            self.solu.insert_job(m,jobs[i],self.solu.get_pre(self.inst.get_N()+m)) 

    def build_greedy(self):
        i_jobs = self.inst.get_copy_P().argsort()[::-1]
        
        for i in i_jobs: 
            m = random.randint(0,self.inst.get_M()-1)
            self.solu.insert_job(m,i,self.solu.get_pre(self.inst.get_N()+m))             
