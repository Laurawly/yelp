import networkx as nx

# local
import social
import bipartite
import algs
import parse


def main():
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