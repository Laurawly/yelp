import collections
import os
import random
import networkx as nx
import numpy as np
import pickle

#local
import parse
import social
import community
import algs
import HITS

def loadBipartite(ratio=1.0):
  if os.path.exists('bipartite.pickle'):
    print "Reading from pickle file"
    G = nx.read_gpickle('bipartite.pickle')
  else:
    print "Parsing raw JSON"
    G = parse.parseReviewFile('data/yelp_academic_dataset_review.json', ratio)

    # write to file to save for later
    nx.write_gpickle(G, 'bipartite.pickle')
    # nx.write_dot(G, 'yelp_data.dot')

  print 'done'
  return G


def loadBusinesses():
  filename = 'businesses.pickle'
  if os.path.exists(filename):
    print "Reading from pickle file"
    with open(filename, "r") as fp:
      G = pickle.load(fp)
  else:
    print "Parsing raw JSON"
    G = parse.parseBusinessFile('data/yelp_academic_dataset_business.json')

    # write to file to save for later
    with open(filename, "w") as fp:
      pickle.dump(G, fp)

  print 'done'
  return G


def calculateJaccard(adj_matrix, B, user1, user2):
  intersect = adj_matrix[user1][user2]
  union = len(B.neighbors(user1)) + len(B.neighbors(user2))
  return float(intersect) / union


def userProject2(B, users, bizes, threshold=0.1):
  """
  iterating over businsses
  """
  G = nx.Graph()
  D = {}

  # add all users to the graph

  for user in users:
    G.add_node(user)
    D[user] = collections.defaultdict(int)

  for count, biz in enumerate(bizes):
#print "%s / %s" %(count, len(bizes))
    reviewers = B.neighbors(biz)

    for i in range(len(reviewers)):
      for j in range(len(reviewers)):
        D[reviewers[i]][reviewers[j]] += 1

  # set all i==j to be zero
  for user in users:
    del D[user][user]

  for i, user in enumerate(users):
#print "u%s / %s" %(i, len(users))
    edges = []
    for other in D[user]:
      jac = calculateJaccard(D, B, user, other)
      if jac > threshold:
        edges.append((user, other, jac))
    G.add_weighted_edges_from(edges)


  # remove nodes without any edges?
  outdeg = G.degree()
  to_remove = [n for n in outdeg if outdeg[n] == 0]
  G.remove_nodes_from(to_remove)

    # edges = [(user, other, D[user][other] ) for other in D[user]]
    # G.add_weighted_edges_from(edges)
    # for other in D[user]:
      # G.add_edge(user, other, weight=D[user][other])

  return G



def userProject(B, users, bizes):
  '''
  Takes forever
  '''
  G = nx.Graph()
  users = set(users)
  print len(users)


  # add all users to the graph
  for user in users:
    G.add_node(user)

  # for each user, add an edge if we share any businesses
  for i, user in enumerate(users):
    print i
    # remove users we are already connected to
    # cur_neighbors = set(G.neighbors(user))
    # leftover = users - cur_neighbors
    for candidate in users:
      # how many businesses do we share?
      bus1 = set(B.neighbors(user))
      bus2 = set(B.neighbors(candidate))
      intersect = bus1.intersection(bus2)
      if len(intersect):
        G.add_edge(user, candidate, weight=len(intersect))

  return G


def loadProjection(B, filename = 'bi_proj.pickle'):
  """
  Convert networkx bipartite graph to a one-mode projection.
  """
  if os.path.exists(filename):
    print "Reading proj from pickle file"
    G = nx.read_gpickle(filename)
  else:
    print "Calculating Projection"
    # ratio?
    user_nodes = set(n for n,d in B.nodes(data=True) if d['bipartite']==0)
    biz_nodes = set(B) - user_nodes
    G = userProject2(B, user_nodes, biz_nodes)
    # G = nx.algorithms.bipartite.weighted_projected_graph(B, user_nodes)

    # write to file to save for later
    nx.write_gpickle(G, filename)

  print 'done'
  return G

def roundrating(x): return 0.5 * round(2.0 * x)


def shrinkNetworkx(G, user_threshold=10, business_threshold=10):
  '''
  remove nodes less than a certain degree
  in: G networkx graph
  out: networkx graph
  '''
  it = G.degree_iter()
  for node, degree in G.degree_iter():
    if node[-1] == 'u':
      if degree < user_threshold:
        G.remove_node(node)
    else:
      if degree < business_threshold:
        G.remove_node(node)
  return G




def main():
  # load file
  B = loadBipartite()
#B = shrinkNetworkx(B)
  proj = loadProjection(B)
  # C = social.loadCommunity(proj, 'B_community.pickle')
  Biz = loadBusinesses()

  copra = algs.Copra(proj, filename='copra10.txt')
  copra.run()
  C = copra.loadCommunity()

  # user_nodes = [n for n,d in B.nodes(data=True) if d['bipartite']==0]
  # biz_nodes = set(B) - set(user_nodes)
  user_nodes = proj.nodes()

  user_credibility, b_new_score = HITS.hits_score(B,Biz)


  # analysis
  iteration = 1000

  diff_peer = []
  diff_yelp = []
  num_peers = []
  for _ in range(iteration):
    while True:
      # loop until we find an acceptable user-business pair

      rand_node = random.choice(user_nodes)
      community = C['byUser'][rand_node]

      # 1. find a random business this user has rated
      businesses = B.neighbors(rand_node)
      if not businesses:
        # this user hasn't rated anyone
        continue
      business = random.choice(businesses)


      # 2. calculate the avg rating of this user's friends who rated this business
      raters = B.neighbors(business)
      peers = []

      for rater in raters:
        if rater == rand_node:
          continue
        if rater in C['byGroup'][community]:
          # found a match!
          peers.append(rater)

      if len(peers) == 0:
        # didn't find any friends who rated this place
        continue

      total = 0.
      totalCredibility = 0.
      for p in peers:
        totalCredibility += user_credibility[p]
        
      for p in peers:
        edge = B.get_edge_data(p, business)
        total += edge['stars']*user_credibility[p]/totalCredibility
# avg_peer_value = roundrating(total / len(peers))
      avg_peer_value = total
      # print "avg value of peers(%s): %s" % (len(peers), avg_peer_value)

      # compare the values
      edge = B.get_edge_data(rand_node, business)
      # print "my value: %s" % edge['stars']

      num_peers.append(len(peers))
      diff_peer.append(abs(edge['stars'] - avg_peer_value))
      diff_yelp.append(abs(edge['stars'] - Biz[business]))


      # found succesful!
      break

  print np.median(num_peers),
  print np.mean(num_peers),
  print np.std(num_peers)

  print np.median(diff_peer),
  print np.mean(diff_peer),
  print np.std(diff_peer)
  
  print np.median(diff_yelp),
  print np.mean(diff_yelp),
  print np.std(diff_yelp)






if __name__ == '__main__':
  main()
