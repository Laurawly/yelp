import subprocess
import os
import tempfile

import cPickle as pickle



CWD = os.path.dirname(os.path.realpath(__file__))

class Copra():
  '''
  FUUUCK. This program can't handle Yelp data. GG.

  http://www.cs.bris.ac.uk/~steve/networks/software/copra.html
  '''
  def __init__(self, G, bipartite=False, filename=None, is_weighted=False):
    self.graph = G
    self.bipartite = bipartite
    self.filename = filename
    self.is_weighted = is_weighted

  def run(self):
    if os.path.exists(self.filename):
      # try to read input from file
      if os.path.exists('clusters-' + self.filename):
        return
      else:
        # we have input file but no clusters
        cmd = "java -cp %s COPRA %s %s %s" % \
              (os.path.join(CWD, 'algorithms', 'copra.jar'), self.filename,
               '-bi' if self.bipartite else '',
               '-w' if self.is_weighted else '')
        print cmd
        subprocess.call(cmd, shell=True)
    else:
      # Write graph to a tempfile
      if self.filename:
        fp = open(os.path.join(CWD, self.filename), 'w')
      else:
        fp = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
      for e in self.graph.edges(data=True):
        # write "user_id bus_id"
        fp.write("%s %s %s\n" % (e[0], e[1], e[2]['weight']*5))
      fp.close()

      cmd = "java -cp %s COPRA %s %s %s" % \
            (os.path.join(CWD, 'algorithms', 'copra.jar'), fp.name,
             '-bi' if self.bipartite else '',
             '-w' if self.is_weighted else '')

      print cmd
      subprocess.call(cmd, shell=True)
      self.filename = fp.name.split('/')[-1]


  def calcCommunities(self):
    communities = {}
    communities['byUser'] = {}
    communities['byGroup'] = {}

    # read in clusters file
    with open('clusters-' + self.filename, 'r') as fp:
      clusters = fp.readlines()

    for group_id, members in enumerate(clusters):
      communities['byGroup'][group_id] = members.split()

    for group_id, members in communities['byGroup'].iteritems():
      for user_id in members:
        communities['byUser'][user_id] = group_id

    return communities

  def loadCommunity(self):
    if os.path.exists(self.filename + '.pickle'):
      print "Reading community from pickle file"
      with open(self.filename + '.pickle', "r") as fp:
        C = pickle.load(fp)
    else:
      print "Calculating community"
      C = self.calcCommunities()

      # write to file to save for later
      with open(self.filename + '.pickle', "w") as fp:
        pickle.dump(C, fp)

    print 'done'
    return C




# class IGFastGreedy():
#   '''
#   '''
#   def __init__(self, G, filename='fast_greedy.pickle'):
#     self.graph = G
#     self.filename = filename

#   def run(self):
#     i_proj = toigraph.toIGraph(self.graph)

#     print 'computing igraph community_fastgreedy'
#     C = i_proj.community_fastgreedy()
#     print 'done'

#     # save to file
#     # write to file to save for later
#     if self.filename:
#       with open(self.filename, "w") as fp:
#         pickle.dump(C, fp)

# class IGLabelProp():
#   '''
#   '''
#   def __init__(self, G, filename='label_propagation.pickle'):
#     self.graph = G
#     self.filename = filename

#   def run(self):
#     i_proj = toigraph.toIGraph(self.graph)

#     print 'computing igraph label_propagation'
#     C = i_proj.community_label_propagation(weights='weight')
#     print 'done'

#     # save to file
#     # write to file to save for later
#     if self.filename:
#       with open(self.filename, "w") as fp:
#         pickle.dump(C, fp)


# class IGEdgeBetweennes():
#   '''
#   '''
#   def __init__(self, G, filename='edge_betweenness.pickle'):
#     self.graph = G
#     self.filename = filename

#   def run(self):
#     i_proj = toigraph.toIGraph(self.graph)

#     print 'computing igraph edge_betweenness'
#     C = i_proj.community_edge_betweenness(weights='weight')
#     print 'done'

#     # save to file
#     # write to file to save for later
#     if self.filename:
#       with open(self.filename, "w") as fp:
#         pickle.dump(C, fp)


