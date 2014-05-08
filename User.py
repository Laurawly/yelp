
class User(object):
  def __init__(self, args = {}):
    if args:
      self.yelping_since = args['yelping_since']
      self.votes = args['votes']
      self.user_id = args['user_id']
      self.name = args['name']
      self.elite = args['elite']
      self.type = args['type']
      self.compliments = args['compliments']
      self.fans = args['fans']
      self.average_stars = args['average_stars']
      self.review_count = args['review_count']
      self.friends = args['friends']
    else:
      self.yelping_since = None
      self.votes = None
      self.user_id = None
      self.name = None
      self.elite = None
      self.type = None
      self.compliments = None
      self.fans = None
      self.average_stars = None
      self.review_count = None
      self.friends = None

  @property
  def id(self):
    return self.user_id