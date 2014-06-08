import networkx as nx

# local
import social
import bipartite
import algs
import parse
import toigraph


def main():
  # load file
  B = bipartite.loadBipartite(.01)
  print B.number_of_nodes()
  print B.number_of_edges()

  # B = bipartite.shrinkNetworkx(B)
  # print B.number_of_nodes()
  # print B.number_of_edges()

  return
  proj = bipartite.loadProjection(B)


  # fast_greedy = algs.IGFastGreedy(proj)
  # fast_greedy.run()


  copra = algs.Copra(proj, filename='copra10.txt')
  copra.run()
  comm = copra.loadCommunity()
  print len(comm.keys())
  print len(comm.values())




if __name__ == '__main__':
  main()