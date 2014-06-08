class Business(dict):
  def __init__(self, args):
    dict.__init__(self, args)
    self.remove_keys()

  def remove_keys(self):
    keep = ['business_id', 'stars']
    for k in self.keys():
      if k not in keep:
        del self[key]
    self['business_id'] +=  'b'