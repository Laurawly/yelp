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
      TotalWeight = 0
      newStar = 0
      for j in R.neighbors(i):
        newStar += u[j]*(R.get_edge_data(j,i)['stars'])
        TotalWeight += u[j]
      newStar = newStar/(TotalWeight)
      if abs(b[i]-newStar)/float(b[i]) <= 0.01: 
        score_diff += 1
      b[i] = newStar
    # scale user credibility to a max of 5
    max_val=max(u.values())
    for i in u:
      u[i]=u[i]/float(max_val) * 5
    # Stopping Criteria
    if score_diff / float(len(business)) >= 0.95:
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

def hits(G,max_iter=100,tol=1.0e-8,nstart=None):
    if type(G) == nx.MultiGraph or type(G) == nx.MultiDiGraph:
        raise Exception("hits() not defined for graphs with multiedges.")

    # choose fixed starting vector if not given
    h=dict.fromkeys(G,1.0/G.number_of_nodes())
    i=0
    while True: # power iteration: make up to max_iter iterations
        hlast=h
        h=dict.fromkeys(hlast.keys(),0)
        a=dict.fromkeys(hlast.keys(),0)
        # this "matrix multiply" looks odd because it is
        # doing a left multiply a^T=hlast^T*G 
        for n in h:
            for nbr in G[n]:
                a[nbr]+=hlast[n]*G[n][nbr].get('weight',1)
        # now multiply h=Ga
        for n in h:
            for nbr in G[n]:
                h[n]+=a[nbr]*G[n][nbr].get('weight',1)
        # normalize vector 
        s=1.0/sum(h.values())
        for n in h: h[n]*=s
        # normalize vector 
        s=1.0/sum(a.values())
        for n in a: a[n]*=s
        # check convergence, l1 norm            
        err=sum([abs(h[n]-hlast[n]) for n in h])
        if err < tol:
            break
        if i>max_iter:
            raise NetworkXError(\
            "HITS: power iteration failed to converge in %d iterations."%(i+1))
        i+=1
    return h,a


if __name__ == '__main__':
  main()
