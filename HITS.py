import os
import networkx as nx
from networkx.algorithms import bipartite
from networkx.exception import NetworkXError

#local
import parse
import social
import bipartite

def hits_score(R,B):

  user = set(n for n,d in R.nodes(data=True) if d['bipartite']==0)
  business = set(R) - user
  
  u = dict.fromkeys(user,0)
  b = dict.fromkeys(business,0)
  for c in b:
    b[c] = B[c]
  n = 0
  while True: # make up to 90% businesses' score won't change by 5%
    score_diff = 0
    # Business to User
    for i in u:
      TotalDiff = 0
      for j in R.neighbors(i):
        TotalDiff += abs(R.get_edge_data(i,j)['stars']-b[j])
      u[i] = 1.0/(1.0+TotalDiff)
    s = 1.0/sum(u.values())
    for i in u:
      u[i]*=s
    # User to Business
    for i in b:
      TotalWeight = 0.
      newStar = 0.
      for j in R.neighbors(i):
        newStar += float(u[j]*(R.get_edge_data(j,i)['stars']))
        TotalWeight += float(u[j])
      if TotalWeight != 0:
        newStar = newStar/float(TotalWeight)
        if abs(b[i]-newStar)/float(b[i]) <= 0.001: 
          score_diff += 1
        b[i] = newStar
    # scale user credibility to a max of 5
    max_val=max(u.values())
    for i in u:
      u[i]=u[i]/float(max_val) * 5
    # Stopping Criteria
    if score_diff / float(len(business)) >= 0.99:
      print score_diff 
      print len(business)
      break
    n += 1
    print n
  return u,b



def main():
  # load file
  print "Loading Review file"
  R = bipartite.loadBipartite()
  print "Loading Business file"
  B = bipartite.loadBusinesses()

  # analysis
  u,b = hits_score(R,B)


if __name__ == '__main__':
  main()
