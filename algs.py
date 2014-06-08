import subprocess
import os
import tempfile

CWD = os.path.dirname(os.path.realpath(__file__))

class Copra():
  '''
  FUUUCK. This program can't handle Yelp data. GG.

  http://www.cs.bris.ac.uk/~steve/networks/software/copra.html
  '''
  def __init__(self, G, bipartite=False):
    self.graph = G
    self.bipartite = bipartite

  def run(self):
    # Write graph to a tempfile
    fp = tempfile.NamedTemporaryFile(delete=False)
    for e in self.graph.edges():
      # write "user_id bus_id"
      fp.write("%s %s\n" % (e[0], e[1]))

    cmd = "java -cp %s COPRA %s %s -mo" % \
          (os.path.join(CWD, 'algorithms', 'copra.jar'), fp.name,
           '-bi' if self.bipartite else '')

    print cmd
    subprocess.call(cmd, shell=True)

    # f.close()
    pass



