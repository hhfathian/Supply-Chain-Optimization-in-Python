from pulp import *
import pandas as pd

cities=range(0,15)
n=15

model=LpProblem("Minimize_TSP_Problem", LpMinimize)

# Define Decision Variables
x = LpVariable.dicts('X', [(c1, c2) for c1 in cities for c2 in cities], cat='Binary')
u = LpVariable.dicts('U', [c1 for c1 in cities], 
                     lowBound=0, upBound=(n-1), cat="Integer")

dist=pd.read_excel('dist.xlsx')

# Define Objective
model += lpSum([dist.iloc[c1, c2] * x[(c1, c2)] 
                for c1 in cities for c2 in cities])

# Define Constraints
for c2 in cities:
    model += lpSum([x[(c1, c2)] for c1 in cities if c1 != c2]) == 1
for c1 in cities:
    model += lpSum([x[(c1, c2)] for c2 in cities if c2 != c1]) == 1
    
# Solve Model
model.solve()

result=[x[(c1, c2)].varValue for c1 in cities for c2 in cities]

TSP_keys=[x[(c1, c2)] for c1 in cities for c2 in cities]

result_df=pd.DataFrame()
result_df['TSP_keys']=TSP_keys
result_df['result']=result

