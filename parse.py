import json
import networkx as nx
import os
import sys
import pickle

import numpy as np
import matplotlib.pyplot as plt

from collections import defaultdict

# local

import gutils
import User
import community


# OPTIONS

# delete nodes that are friendless
OPT_DELETE_FRIENDLESS = True

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
    d[user['user_id']] = User.User(user)

  return d


def parseUserFile(filename):
  """
  Load filename and parse into dictionary
  """
  users = {}

  with open(filename) as fp:
    lines = fp.readlines()

  users = {}
  for line in lines:
    # remove newlines
    line = line.strip()
    user = parseJSON(line)
    users[user['user_id']] = User.User(user)

  G = nx.Graph()

  # add all nodes
  for user_id, user in users.iteritems():
    if OPT_DELETE_FRIENDLESS and len(user['friends']) != 0:
      # Don't add nodes without any friends
      G.add_node(user_id, user)

  # add edges
  for user_id, user in users.iteritems():
    for friend_id in user['friends']:
      # Note: we double add each edge, but that seems to be okay?
      G.add_edge(user_id, friend_id)

  return G

def calcCommunities(graph):
  partition = community.best_partition(graph)
  communities = {}

  size = float(len(set(partition.values())))
  print "Total communities are: " + str(size)
  count = 0.
  for com in set(partition.values()) :
      count = count + 1.
      list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
      communities[count] = list_nodes

  return communities


