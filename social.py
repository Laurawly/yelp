import json
import networkx as nx
import os
import sys
import pickle
import random

import numpy as np
import matplotlib.pyplot as plt

from collections import defaultdict

# local

import gutils
import User
import community
import parse

def loadSocialNetwork():
  if os.path.exists('social_network.gpickle'):
    print "Reading from pickle file"
    G = nx.read_gpickle('social_network.gpickle')
  else:
    print "Parsing raw JSON"
    G = parse.parseUserFile('data/yelp_academic_dataset_user.json')

    # write to file to save for later
    nx.write_gpickle(G, 'social_network.gpickle')

  print 'done'
  return G

def loadCommunity(graph, filename = 'communitiy.pickle'):
  if os.path.exists(filename):
    print "Reading community from pickle file"
    with open(filename, "r") as fp:
      C = pickle.load(fp)
  else:
    print "Calculating community"
    C = parse.calcCommunities(graph)

    # write to file to save for later
    with open(filename, "w") as fp:
      pickle.dump(C, fp)

  print 'done'
  return C

def main():
  # load file
  G = loadSocialNetwork()
  C = loadCommunity(G)

  # analysis
  # gutils.avgDegree(G)
  nodes = g.nodes()
  iters = 10

  for _ in range(iters):
    rand_node = random.choice(nodes)

    # find a random business this user has rated

    # calculate the avg rating of this user's friends who rated this business

    # compare the values








if __name__ == '__main__':
  main()