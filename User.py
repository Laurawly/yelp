class User(dict):
  def __init__(self, args):
    dict.__init__(self, args)
    self.remove_keys()

  def remove_keys(self):
    keys = [u'yelping_since', u'votes', u'review_count', u'name',
            u'type', u'fans', u'average_stars', u'compliments', u'elite']
    for key in keys:
      del self[key]