import pandas as pd
import numpy as np
import random
from collections import Counter

n = 10 # number of times
u = 9 # user number
p = 4 # page number
log_list=[]

for i in range(n):
    user = random.randint(1,u)
    page = random.randint(1,p)
    log = (user,i,page)
    log_list.append(log)

print(log_list)
log = pd.DataFrame(log_list, columns=['user','time','page']) #creating pandas dataframe
#log = log.sort_values(by='user') #sorting the pandas dataframe according to user
#print(log)

triple_user=[]
triples_final=[]
user_lists = {}
for un in range (1,u):
    loc = log['page'].where(log['user'] == un) #working with each user number
    loc = [x for x in loc if pd.isnull(x) == False and x != 'nan'] #deleting empty values for each list
    #print(f'user{un}', loc)

    for i in range(0,len(loc)-2):
        j = i+3
        triples=loc[i:j]
        triple_user.append(triples) #creating the triples list
        print(f'This is the triple list for user{u}:', triple_user)
    triples_final.append(triple_user)
print('This is the complete triples list', triples_final)
