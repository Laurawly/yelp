import os
import random
import networkx as nx
import numpy as np
import pickle

#local
import parse
import social
import community

def loadBipartite():
  if os.path.exists('bipartite.gpickle'):
    print "Reading from pickle file"
    G = nx.read_gpickle('bipartite.gpickle')
  else:
    print "Parsing raw JSON"
    G = parse.parseReviewFile('data/yelp_academic_dataset_review.json')

    # write to file to save for later
    nx.write_gpickle(G, 'bipartite.gpickle')
    # nx.write_dot(G, 'yelp_data.dot')

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

  return G

def main():
  # load file
  G = social.loadSocialNetwork()
  B = loadBipartite()
  C = social.loadCommunity(G)
  Biz = loadBusinesses()




  # analysis
  # gutils.avgDegree(G)
  nodes = G.nodes()
  iteration = 10000

  diff_peer = []
  diff_yelp = []
  num_peers = []
  for _ in range(iteration):
    while True:
      # loop until we find an acceptable user-business pair

      rand_node = random.choice(nodes)
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
      avg_peer_value = total / len(peers)
      # print "avg value of peers(%s): %s" % (len(peers), avg_peer_value)

      # compare the values
      edge = B.get_edge_data(rand_node, business)
      # print "my value: %s" % edge['stars']

      num_peers.append(len(peers))
      diff_peer.append(abs(edge['stars'] - avg_peer_value))
      diff_yelp.append(abs(edge['stars'] - Biz[business]))


      # found succesful!
      break

  print np.mean(num_peers)
  print np.std(num_peers)
  print np.mean(diff_peer)
  print np.std(diff_peer)
  print np.mean(diff_yelp)
  print np.std(diff_yelp)






if __name__ == '__main__':
  main()