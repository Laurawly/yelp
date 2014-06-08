class Review(dict):
  def __init__(self, args):
    dict.__init__(self, args)
    self.remove_keys()

  def remove_keys(self):
    keep = ['user_id', 'review_id', 'stars', 'business_id']
    keys = ['votes', 'date', 'text', 'type']
    for key in keys:
      del self[key]

    # add 'u' and 'b' to end of ids
    self['user_id'] +=  'u'
    self['business_id'] +=  'b'




 #    {
 # "user_id": "xAVu2pZ6nIvkdHh8vGs84Q"
 # "review_id": "DusrkpkTGPGkqK13xO1TZg"
 # "stars": 3
 # "date": "2011-11-26"
 # "text": "Standard Chipotle fare - consistently good; not bad for corporate food - if you have a few minutes
 # there are a number of good local offerings within walking distance."
 # "type": "review"
 # "business_id": "WcGTSRku3mrVK7V9GKq4UQ"}