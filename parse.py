import json
import networkx as nx
import os
import sys
import pickle
import copy

import numpy as np
import matplotlib.pyplot as plt

from collections import defaultdict

# local

import gutils
import User
import Review
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
    users[user['user_id']] = review.Review(user)

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



def parseReviewFile(filename):
  # kinda weird cause I'm generating users/businesses from here rather than
  # the users of business files...

  reviews = list()
  users = set()
  businesses = set()

  with open(filename) as fp:
    lines = fp.readlines()

  for line in lines:
    # remove newlines
    line = line.strip()
    review = parseJSON(line)
    reviews.append(Review.Review(review))

  G = nx.Graph()

  # add all nodes
  for r in reviews:
    # check if new user
    if r['user_id'] not in users:
      users.add(r['user_id'])
      G.add_node(r['user_id'], bipartite=0)

    # check if new business
    if r['business_id'] not in businesses:
      businesses.add(r['business_id'])
      G.add_node(r['business_id'], {'stars': 3.4}, bipartite=1)

    # add the edge
    G.add_edge(r['user_id'], r['business_id'], stars=r['stars'])

  return G


def parseBusinessFile(filename):
  Biz = {}

  with open(filename) as fp:
    lines = fp.readlines()

  for line in lines:
    # remove newlines
    line = line.strip()
    business = parseJSON(line)
    Biz[business['business_id']] = business['stars']

  return Biz


def calcCommunities(graph):
  partition = community.best_partition(graph)
  communities = {}
  communities['byUser'] = partition.copy()
  communities['byGroup'] = {}

  size = float(len(set(partition.values())))
  print "Total communities are: " + str(size)
  count = 0
  for com in set(partition.values()) :
      list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
      communities['byGroup'][count] = list_nodes
      count = count + 1

  return communities


