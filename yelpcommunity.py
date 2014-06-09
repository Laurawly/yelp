class YelpCommunity():
  def __init__(self, C):
    self.C = C

  def counts(self):
    # [len(C['byGroup'][i]) for i in C['byGroup']]
    return [len(self.C['byGroup'][i]) for i in self.C['byGroup']]

