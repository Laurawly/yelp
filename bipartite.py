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


def userProject2(B, users, bizes):
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
    print "%s / %s" %(count, len(bizes))
    reviewers = B.neighbors(biz)

    for i in range(len(reviewers)):
      for j in range(i+1, len(reviewers)):
        D[reviewers[i]][reviewers[j]] += 1

  for i, user in enumerate(users):
    print "u%s / %s" %(i, len(users))
    edges = [(user, other, D[user][other] ) for other in D[user]]
    G.add_weighted_edges_from(edges)
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
    if i == 50:
      import sys
      sys.exit(1)
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

def main():
  # load file
  B = loadBipartite(0.2)
  proj = loadProjection(B)
  C = social.loadCommunity(proj, 'B_community.pickle')
  Biz = loadBusinesses()

  user_nodes = [n for n,d in B.nodes(data=True) if d['bipartite']==0]
  biz_nodes = set(B) - set(user_nodes)



  # analysis
  iteration = 10000

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
      for p in peers:
        edge = B.get_edge_data(p, business)
        total += edge['stars']
      avg_peer_value = roundrating(total / len(peers))
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