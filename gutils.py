import numpy as np
import matplotlib.pyplot as plt

from collections import defaultdict

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