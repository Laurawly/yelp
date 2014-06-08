import networkx as nx

# local
import social
import bipartite
import algs
import parse
import toigraph


def main():
  # load file
  B = bipartite.loadBipartite(0.2)

  proj = bipartite.loadProjection(B)
  i_proj = toigraph.toIGraph(proj)


if __name__ == '__main__':
  main()