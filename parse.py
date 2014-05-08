import json
import networkx
import os


import numpy as np
import matplotlib.pyplot as plt

from collections import defaultdict

def parseJSON(line):
  return json.loads(line.replace('\r', '\\r').replace('\n', '\\n'))

def parseUser(filename):
  """
  Load filename and parse into dictionary
  """
  with open(filename) as fp:
    lines = fp.readlines()

  d = {}
  for line in lines:
    # remove newlines
    line = line.strip()
    user = parseJSON(line)
    d[user['user_id']] = user

  return d


def saveGEXF(graph, filename):
  if not os.path.exists(filename):
    networkx.write_gexf(graph, filename)


def avgDegree(G):
  print "Nodes: ",
  print G.number_of_nodes()
  print "Edges: ",
  print G.number_of_edges()

  # avg degree
  degrees = defaultdict(int)
  total = 0
  for node in G.nodes():
    neighbors = G.neighbors(node)
    degrees[len(neighbors)] += 1
    total += len(neighbors)

  max_degree = max(degrees.keys())
  degrees_arr = (max_degree+1) * [0]
  for index, count in degrees.iteritems():
    degrees_arr[index] = count

  plt.plot(range(max_degree+1), degrees_arr, '.')
  plt.xscale('log', basex=2)
  plt.xlabel('degree')
  plt.yscale('log', basex=2)
  plt.ylabel('# of people')
  plt.savefig('degree_distribution.png')
  plt.close()

def main():

  # if os.path.exists('social_network.gpickle'):
  #   print "Reading from pickle file"
  #   G = networkx.read_gpickle('social_network.gpickle')
  # else:
  #   print "Parsing raw JSON"
  #   users = parseUser('data/yelp_academic_dataset_user.json')
  #   # users = parseUser('data/mini_10.json')

  #   G = networkx.Graph()

  #   # add all nodes
  #   for user_id, user in users.iteritems():
  #     G.add_node(user_id, user)

  #   # add edges
  #   for user_id, user in users.iteritems():
  #     for friend_id in user['friends']:
  #       # Note: we double add each edge, but that seems to be okay?
  #       G.add_edge(user_id, friend_id)

  #   # write to file to save for later
  #   networkx.write_gpickle(G, 'social_network.gpickle')


  print "Parsing raw JSON"
  users = parseUser('data/yelp_academic_dataset_user.json')
  # users = parseUser('data/mini_10.json')

  G = networkx.Graph()

  # add all nodes
  for user_id, user in users.iteritems():
    if len(user['friends']) != 0:
      G.add_node(user_id)

  # add edges
  for user_id, user in users.iteritems():
    for friend_id in user['friends']:
      # Note: we double add each edge, but that seems to be okay?
      G.add_edge(user_id, friend_id)
  networkx.write_gpickle(G, 'social_network_bare.gpickle')

  # avgDegree(G)
  networkx.write_dot(G, 'yelp_data.dot')







if __name__ == '__main__':
  main()