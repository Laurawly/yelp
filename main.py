import networkx as nx
import pickle

# local
import social
import bipartite
import algs
import parse

def main():
  # load file
  B = bipartite.loadBipartite()

  proj = bipartite.loadProjection(B)

  # community = social.loadCommunity(proj, 'B_community.pickle')


if __name__ == '__main__':
  main()