import networkx as nx
import pickle
import numpy as np
import matplotlib.pyplot as plt

# local
import social
import bipartite
import algs
import parse




def main():
  with open('social_network_community.pickle', 'r') as fp:
    C = pickle.load(fp)

  sizes = [len(C['byGroup'][i]) for i in C['byGroup'] if len(C['byGroup'][i]) > 10]
  # n, bins = np.histogram(sizes, bins=100)

  # ugly bars
  # width = 0.7 * (bins[1] - bins[0])
  # center = (bins[:-1] + bins[1:]) / 2
  # plt.bar(center, n, align='center', width=width)
  # plt.xlabel('degree')
  # plt.ylabel('# of people')
  # plt.show()

  plt.hist(sizes, 50, log=True)
  plt.savefig('networkx_community_dist.png')
  plt.close()

  with open('copra10_bipart.txt.pickle', 'r') as fp:
    C = pickle.load(fp)

  sizes = [len(C['byGroup'][i]) for i in C['byGroup'] if len(C['byGroup'][i]) > 10]
  # n, bins = np.histogram(sizes, bins=100)


  plt.hist(sizes, 50, log=True)
  plt.savefig('copra_community_dist.png')
  plt.close()

  with open('social_network_community.pickle', 'r') as fp:
    C = pickle.load(fp)

  sizes = [len(C['byGroup'][i]) for i in C['byGroup'] if len(C['byGroup'][i]) > 10]
  # n, bins = np.histogram(sizes, bins=100)


  plt.hist(sizes, 50, log=True)
  plt.savefig('social_community_dist.png')
  plt.close()

  return

  # load file
  B = bipartite.loadBipartite()
  print B.number_of_nodes()
  print B.number_of_edges()

  B = bipartite.shrinkNetworkx(B, 10, 10)
  print B.number_of_nodes()
  print B.number_of_edges()

  proj = bipartite.loadProjection(B)
  print "projection stats"
  print proj.number_of_nodes()
  print proj.number_of_edges()

  fast_greedy = algs.IGEdgeBetweennes(proj)
  fast_greedy.run()


  # copra = algs.Copra(proj, filename='copra10.txt')
  # copra.run()
  # comm = copra.loadCommunity()
  # print len(comm.keys())
  # print len(comm.values())




if __name__ == '__main__':
  main()