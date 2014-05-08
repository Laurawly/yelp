import json
import networkx
import os

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
    d[user['user_id']] = user

  return d

def main():

  if os.path.exists('social_network.gpickle'):
    print "Reading from pickle file"
    G = networkx.read_gpickle('social_network.gpickle')
  else:
    print "Parsing raw JSON"
    users = parseUser('data/yelp_academic_dataset_user.json')
    # users = parseUser('data/mini_10.json')

    G = networkx.Graph()

    # add all nodes
    for user_id, user in users.iteritems():
      G.add_node(user_id, user)

    # add edges
    for user_id, user in users.iteritems():
      for friend_id in user['friends']:
        # Note: we double add each edge, but that seems to be okay?
        G.add_edge(user_id, friend_id)

    # write to file to save for later
    networkx.write_gpickle(G, 'social_network.gpickle')

  print G.number_of_nodes()
  print G.number_of_edges()


if __name__ == '__main__':
  main()