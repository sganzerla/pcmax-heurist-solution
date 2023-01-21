import pandas as pd
import os
import numpy as np

class BuildPandas:
    def __init__(self, path: str ):
        self.df: pd.DataFrame = pd.read_csv(path)
        self.df_report_cmax: pd.DataFrame
        self.build_report_cmax()
        

    def build_report_cmax(self):
        df_gr = self.df.groupby(['struct','instance', 'literature'], sort=False, as_index=False)['cmax'].aggregate({'Min':'min', 'Max':'max', 'Mean': 'mean', 'Std': 'std', 'Var': 'var'})
        df_gr['Gap Min'] = self.__calc_gap_min__(df_gr, 'literature', 'Min')
        df_gr['Gap Mean'] = self.__calc_gap_min__(df_gr, 'literature', 'Mean')
        # deixar float com 2 decimais
        df_gr: pd.DataFrame = df_gr.round(2)
        # começa o indice com 1
        df_gr.index +=1
        
        self.df_report_cmax = df_gr
        
    def __calc_gap_min__(self, df_gr: pd.DataFrame, col_a: str, col_b: str) -> pd.Series:
        col = (df_gr[col_a] - df_gr[col_b]) / df_gr[col_b]
        col =  col.apply(lambda x: x * -100 if float(x) != 0.0 else x )
        col = col.apply(lambda x: str(f"{x:.2f}%"))
        return col

    def get_latex_report_cmax(self):
        print(self.df_report_cmax.to_latex(header=["Struct", "Instance", "C(BKS)", "C(Min)", "C(Max)", "C(Mean)", "C(Std)", "C(Var)", "Min", "Mean"]))

    def get_latex_type_instances(self):
        print(self.df)
        df: pd.DataFrame = self.df.groupby(['struct', 'm' , 'n'], sort=False, as_index=False)['struct', 'm' , 'n']
        df = df.mean().round()
        df['instances'] = df['m'] - df['m'] + 5
        print(df.to_latex())
        

if __name__ == "__main__":
    
    # uninformed initial solution
    u_is = os.path.join("amd", "report0.csv")
    # greedy initial solution
    g_is = os.path.join("amd", "report1.csv")
    # literary initial solution
    l_is = os.path.join("amd", "report2.csv")
    
    u = BuildPandas(l_is)
    u.get_latex_type_instances()
