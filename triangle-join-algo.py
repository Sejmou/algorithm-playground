# DATABASE (bad Python "simulation" lol):
import pandas as pd # pandas DataFrames are probably closest Python equivalent to SQL tables
import numpy as np

# attributes
# make sure all the values in A, B, C are distinct and each list contains same number of values (m+1)
A = np.arange(0,10000) # values for attribute A
B = np.arange(10000,20000) # values for attribute B
C = np.arange(20000,30000) # values for attribute C

# relations
R = list([A[0], b] for b in B) + list([a, B[0]] for a in A)
S = list([B[0], c] for c in C) + list([b, C[0]] for b in B)
T = list([A[0], c] for c in C) + list([a, C[0]] for a in A)

R = pd.DataFrame(R, columns=['A', 'B'])
S = pd.DataFrame(S, columns=['B', 'C'])
T = pd.DataFrame(T, columns=['A', 'C'])

# GOAL:
# Solve the "triangle query" problem in most efficient possible way
# I.e. find most efficient way to execute the query
# SELECT * FROM R,S,T WHERE
# R.A = T.A AND R.B = S.B AND S.C = T.C
#
# on the "database" (set of tables R, S, T) defined above
#
# This query is mentioned in the ADBS slides at least
# However, confusingly, it is not the same as the result of the efficient algorithm (pseudo code in the slides, for Python implementation see below)
# For the ADBS exercise, the triangle query is described as
# SELECT DISTINCT a,b,c FROM r NATURAL JOIN s NATURAL JOIN t;

# This is also the result the two algorithms (inefficient vs. efficient in terms of size of intermediate results) implemented here produce

# Note: probably my implementation of the efficient algorithm is even slower in terms of runtime
# I use for loops and don't take advantage of pandas/NumPy matrix operations
# However, that's not the point here, as the size of intermediate query results is the cost metric that is interesting wrt. databases (see below for details)
# The code I implemented here in Python is just a toy example, the algorithms should actually be used in traditional SQL databases!

# When looking at the efficiency of traditional SQL database queries, one has to think of large DBMSs
# Here disk I/O is always the bottleneck for query execution times
# The larger intermediate results of a query become, the more likely they are to become too large to be kept in memory
# We have to temporarily write back to (and read from) the disk, which is several orders of magnitude slower!
# So, memory efficiency is actually quite important!
# Therefore, the size of intermediate result is a very useful "cost metric" in DBMS query execution plans!

relations = {'R': R, 'S': S, 'T': T}
print('relations:')
for rel_name, rel_df in relations.items():
  print(f'{rel_name}:')
  print(rel_df)
  print()
  #rel_df.to_csv(f'{rel_name}.csv', index=False)

m = R.shape[0] - 1
print(f'number of entries per relation = m + 1 = {m + 1}\n')

# query execution plan that is inefficient in terms of size of intermediate results
# required joins are executed using combination of two natural joins (order doesn't matter if all relations are of equal size)
# joins (can be visualized as join tree, too): (R joined with T) joined with S
def inefficient_triangle_query(R: pd.DataFrame, S: pd.DataFrame, T: pd.DataFrame):
  cost = 0 # cost in terms of size of intermediate results
  first = pd.merge(R, T, how='inner')
  cost += first.shape[0]

  second = pd.merge(first, S, how='inner')
  cost += second.shape[0]

  res = second.drop_duplicates()
  return res, cost

def efficient_triangle_query(R: pd.DataFrame, S: pd.DataFrame, T: pd.DataFrame):
  Q = []
  cost = 0 # cost in terms of size of intermediate results

  L_A = pd.Series(np.intersect1d(R.A, T.A), name="L_A")
  cost += L_A.shape[0]
  #print(L_A)
  for a in L_A:
    La_B = pd.Series(np.intersect1d(R[R.A == a].B, S.B), name="La_B")
    cost += La_B.shape[0]
    #print(La_B)
    for b in La_B:
      Lab_C = pd.Series(np.intersect1d(S[S.B == b].C, T[T.A == a].C), name="Lab_C")
      cost += Lab_C.shape[0]
      for c in Lab_C:
        Q.append([a, b, c])
 
  return pd.DataFrame(Q, columns=['A', 'B', 'C']), cost


Q_res_ineff, cost_ineff = inefficient_triangle_query(R, S, T)
print('Inefficient query output:')
print(Q_res_ineff)
print('cost (size of intermediate results) =', cost_ineff, '\n')

Q_res_eff, cost_eff = efficient_triangle_query(R, S, T)
print('Efficient query output:')
print(Q_res_eff)
print('cost (size of intermediate results) =', cost_eff)

print('\nStats for comparison:')
print('m = ', m)
print('m² = ', m * m)
print('m log(m) = ', m * np.log(m))