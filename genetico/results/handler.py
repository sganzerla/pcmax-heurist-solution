import pandas as pd
import os

# uninformed initial solution
u_is = pd.read_csv(os.path.join("amd", "report0.csv"))
# greedy initial solution
# g_is = 
# literary initial solution
# l_is =


# u_is.reset_index(drop=True)
# print(u_is.head(5))
u_is_group = u_is.groupby(['struct','instance', 'literature'], sort=False, as_index=False)['cmax'].aggregate({'Min':'min', 'Max':'max', 'Mean': 'mean', 'Std': 'std', 'Var': 'var'})

# reduzir casas decimais


def calc_gap_min(u_is_group: pd.DataFrame, col_a: str, col_b: str) -> pd.Series:
    col = (u_is_group[col_a] - u_is_group[col_b]) / u_is_group[col_b]
    col =  col.apply(lambda x: x * -100 if float(x) != 0.0 else x )
    col.round(2)
    col = col.apply(lambda x: str(f"{x:.2f}%"))
    return col

u_is_group['Gap Min'] = calc_gap_min(u_is_group, 'literature', 'Min')
u_is_group['Gap Mean'] = calc_gap_min(u_is_group, 'literature', 'Mean')

u_is_group = u_is_group.round(2)

print(u_is_group)

