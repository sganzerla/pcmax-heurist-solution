import pandas as pd
import os
import numpy as np

class BuildPandas:
    def __init__(self, path: str ):
        self.df: pd.DataFrame = pd.read_csv(path, decimal=",")
        self.df_report_cmax: pd.DataFrame
        self.build_report_cmax()
        

    def build_report_cmax(self):
        df = self.df.groupby(['struct','instance', 'literature'], sort=False, as_index=False)['cmax'].aggregate({'Min':'min', 'Max':'max', 'Mean': 'mean', 'Std': 'std', 'Var': 'var'})
        df['Gap Min'] = self.__calc_gap_min__(df, 'literature', 'Min')
        df['Gap Mean'] = self.__calc_gap_min__(df, 'literature', 'Mean')
        # deixar float com 2 decimais
        df: pd.DataFrame = df.round(2)
        # começa o indice com 1
        df.index +=1
        
        self.df_report_cmax = df
        
    def __calc_gap_min__(self, df_gr: pd.DataFrame, col_a: str, col_b: str) -> pd.Series:
        col = (df_gr[col_a] - df_gr[col_b]) / df_gr[col_b]
        col =  col.apply(lambda x: x * -100 if float(x) != 0.0 else x )
        col = col.apply(lambda x: str(f"{x:.2f}%"))
        return col

    def get_latex_report_cmax(self):
        print(self.df_report_cmax.to_latex(header=["Struct", "Instance", "C(BKS)", "C(Min)", "C(Max)", "C(Mean)", "C(Std)", "C(Var)", "Min", "Mean"]))

    def get_latex_type_instances(self):
        df: pd.DataFrame = self.df.groupby(['struct', 'm' , 'n'], sort=False, as_index=False)['struct', 'm' , 'n']
        df = df.mean().round()
        df['instances'] = 5
        df = df.groupby(['struct', 'instances', 'm', 'n'], sort=False, as_index=False)['struct', 'instances', 'm', 'n']
        df = df.first()
        df.index +=1
        print(df.to_latex(header=["Struct", "Instances", "M", "N"]))
    
    def get_mean_group_instances_type(self) -> pd.DataFrame:
        df = self.df.groupby(['struct', 'm', 'n'], sort=False, as_index=False)['literature'].aggregate({'BKS(Mean)': 'mean', 'BKS(Std)': 'std'})
        df2 = self.df.groupby(['struct', 'm', 'n'], sort=False, as_index=False)['cmax'].aggregate({'GA(Mean)': 'mean', 'GA(Std)': 'std'})
        df['GA(Mean)'] = df2['GA(Mean)']
        df['GA(Std)'] = df2['GA(Std)']
        df: pd.DataFrame = df.round(2)
        df['GAP'] = self.__calc_gap_min__(df, 'BKS(Mean)', 'GA(Mean)')
        df.index += 1
        print(df.to_latex())
        
    def get_mean_group_instances_type_mean_time(self) -> pd.DataFrame:
       df = self.df[['struct','m', 'n', 'mean_time']]
       df = df.groupby(['m', 'n' ],  sort=False, as_index=False)['mean_time'].aggregate({'Time(Mean)':'mean'})
       df = df.round(2)
       print(df.to_latex())
       
    
if __name__ == "__main__":
    
    # uninformed initial solution
    u_is = os.path.join("amd", "report0.csv")
    
    # greedy initial solution
    g_is = os.path.join("amd", "report1.csv")

    # literary initial solution
    l_is = os.path.join("amd", "report2.csv")
    
    report = [u_is, g_is, l_is]
    
    x = np.ndarray(3, dtype=pd.DataFrame)
    for i in range(1):
        u = BuildPandas(report[i]) 
        u.get_mean_group_instances_type_mean_time()