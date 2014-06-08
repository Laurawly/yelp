import networkx as nx
import igraph as ig

def toIGraph(G):
  new = ig.Graph()
  print 'adding nodes'
  new.add_vertices(G.nodes())
  print 'adding edges'
  edges = G.edges()
  new.add_edges(edges)

  print 'adding weights'
  weights = G.edges(data=True)
  new.es['weight'] = [edge[2]['weight'] for edge in weights]

  return new
