# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 20:56:16 2021

@author: iri_0
"""

import csv
def read_file(file):
    lst=[]
    with open(file, 'rt', encoding='utf-8-sig') as f:
        rows = csv.reader(f)
        headers = next(rows)
        for row in rows:
            record = dict(zip(headers,row))
            lst.append(record)
    return lst

record=read_file(r'D:\ICE\542\Intive.csv')

#%% Page visited for each user

user1=[]
user2=[] 
user3=[]
user4=[]
user5=[]
user6=[]
user7=[]
user8=[]
user9=[]
user10=[]

for i in record:
  if i['user'] == '1':
      page= i['page']
      user1.append(page)
  elif i['user'] == '2':
       page= i['page']
       user2.append(page)
  elif i['user'] == '3':
       page= i['page']
       user3.append(page)
  elif i['user'] == '4':
       page= i['page']
       user4.append(page)
  elif i['user'] == '5':
       page= i['page']
       user5.append(page) 
  elif i['user'] == '6':
       page= i['page']
       user6.append(page)   
  elif i['user'] == '7':
       page= i['page']
       user7.append(page)
  elif i['user'] == '8':
       page= i['page']
       user8.append(page)
  elif i['user'] == '9':
       page= i['page']
       user9.append(page)
  elif i['user'] == '10':
       page= i['page']
       user10.append(page)   


print(f'user1: ', user1)
print(f'user2: ', user2)
print(f'user3: ', user3)
print(f'user4: ', user4)
print(f'user5: ', user5)
print(f'user6: ', user6)
print(f'user7: ', user7)
print(f'user8: ', user8)
print(f'user9: ', user9)
print(f'user10: ', user10)

def tuples(lista):
    a=tuple(lista)
    return a

#%% Triples of each user

def triples(user):
    triple_user=[] 
    for j in range(len(user)-2):
        a=tuples(user)[j:j+3]
        triple_user.append(a)
    return triple_user

print(f' Triples user1: ', triples(user1))
print(f' Triples user2: ', triples(user2)) 
print(f' Triples user3: ', triples(user3))   
print(f' Triples user4: ', triples(user4)) 
print(f' Triples user5: ', triples(user5))   
print(f' Triples user6: ', triples(user6)) 
print(f' Triples user7: ', triples(user7))
print(f' Triples user8: ', triples(user8))
print(f' Triples user9: ', triples(user9))
print(f' Triples user10: ', triples(user10))


#%% Find the 10 most common triplets and count the occurrences of each triplet 

from collections import Counter
total=triples(user1) + triples(user2)+ triples(user3) + triples(user4) + triples(user5) + triples(user6) + triples(user7) + triples(user8) + triples(user9) + triples(user10)
print(total)
print(type(total))
contador=Counter(total)
final= contador.most_common(10)

for i in range(len(final)):
    k= final[i][0]
    j= final[i][1]
    print (f'the triple', k,'occurred',j, 'times')

   









