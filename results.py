import numpy as np
import random

def roundratinghalf(x): return 0.5 * round(2.0 * x)
def roundrating(x): return round(x)


def compareAll(user_nodes, C, B, Biz, D, user_credibility, b_new_score, peer_weight=0.6, friend_weight=0.3):
  diff_peer = []
  diff_yelp = []
  num_peers = []
  diff_biz = []
  diff_avgerage = []

  for user in user_nodes:
    community = C['byUser'][user]
    if len(C['byGroup'][community]) < 10:
      # only choose users that are in a reasonably large community
        continue
    if user not in D['byUser']:
      # User has no friend
        continue
    social_community = D['byUser'][user]

    for business in B.neighbors(user):
      # 2. calculate the avg rating of this user's friends who rated this business
      raters = B.neighbors(business)
      peers = []
      outsiders = []
      friends = []

      for rater in raters:
        if rater == user:
          continue
        if rater in C['byGroup'][community]:
          # found a match!
          peers.append(rater)
        else: outsiders.append(rater)
        if rater in D['byGroup'][social_community]:
          friends.append(rater)

      if len(peers) == 0:
        # didn't find any friends who rated this place
        continue
      if len(outsiders) == 0:
        continue

      total = 0.
      o_total = 0.
      r_total = 0.
      f_total = 0.
      totalCredibility = 0.
      o_totalCredibility = 0.
      f_totalCredibility = 0.
      totalCredibility = sum([user_credibility[p] for p in peers])
      o_totalCredibility = sum([user_credibility[p] for p in outsiders])
      f_totalCredibility = sum([user_credibility[p] for p in friends])

      for p in peers:
        edge = B.get_edge_data(p, business)
        total += edge['stars']*1./len(peers)
      for p in outsiders:
        edge = B.get_edge_data(p, business)
        o_total += edge['stars']*1./len(outsiders)
      for p in friends:
        edge = B.get_edge_data(p, business)
        f_total += edge['stars']*1./len(friends)
      for p in raters:
        edge = B.get_edge_data(p, business)
        r_total += edge['stars']
        # o_total += edge['stars']*user_credibility[p]/o_totalCredibility
      avg_peer_value = total*peer_weight+f_total*friend_weight+o_total*(1-peer_weight-friend_weight)

      # compare the values
      edge = B.get_edge_data(user, business)

      # num_peers.append(len(peers))
      diff_peer.append(abs(edge['stars'] - roundratinghalf(avg_peer_value)))
      # diff_yelp.append(abs(edge['stars'] - Biz[business]))
      # diff_biz.append(abs(edge['stars'] - b_new_score[business]))
      diff_avgerage.append(abs(edge['stars'] - roundratinghalf(float(r_total)/len(raters))))



  print np.median(num_peers),
  print np.mean(num_peers),
  print np.std(num_peers)

  print np.median(diff_peer),
  print np.mean(diff_peer),
  print np.std(diff_peer)

  print np.median(diff_yelp),
  print np.mean(diff_yelp),
  print np.std(diff_yelp)


  print np.median(diff_biz),
  print np.mean(diff_biz),
  print np.std(diff_biz)

  print np.median(diff_avgerage),
  print np.mean(diff_avgerage),
  print np.std(diff_avgerage)


def compareIterations(user_nodes, C, B, Biz, D, user_credibility, b_new_score, iteration=10000):
  # analysis
  diff_peer = []
  diff_yelp = []
  num_peers = []
  diff_biz = []
  for _ in range(iteration):
    while True:
      # loop until we find an acceptable user-business pair

      rand_node = random.choice(user_nodes)
      community = C['byUser'][rand_node]
      if len(C['byGroup'][community]) < 100:
          continue
      if rand_node not in D['byUser']:
        # User has no friend
        continue
      social_community = D['byUser'[rand_node]]

      # 1. find a random business this user has rated
      businesses = B.neighbors(rand_node)
      if not businesses:
        # this user hasn't rated anyone
        continue
      business = random.choice(businesses)


      # 2. calculate the avg rating of this user's friends who rated this business
      raters = B.neighbors(business)
      peers = []
      outsiders = []
      friends = []
      for rater in raters:
        if rater == rand_node:
          continue
        if rater in C['byGroup'][community]:
          # found a match!
          peers.append(rater)
        else: outsiders.append(rater)
        if rater in D['byGroup'][social_community]:
          friends.append(rater)

      if len(peers) == 0:
        # didn't find any friends who rated this place
        continue
      if len(outsiders) == 0:
        continue
      if len(friends) == 0:
        continue
    
      total = 0.
      o_total = 0.
      f_total = 0.
      totalCredibility = 0.
      o_totalCredibility = 0.
      f_totalCredibility = 0.

      for p in peers:
        totalCredibility += user_credibility[p]
      for p in peers:
        edge = B.get_edge_data(p, business)
        total += edge['stars']*user_credibility[p]/totalCredibility
      for p in outsiders:
        o_totalCredibility += user_credibility[p]
      for p in outsiders:
        edge = B.get_edge_data(p, business)
        o_total += edge['stars']*user_credibility[p]/o_totalCredibility
      for p in friends:
        f_totalCredibility += user_credibility[p]
      for p in friends:
        edge = B.get_edge_data(p, business)
        f_total += edge['stars']*user_credibility[p]/f_totalCredibility
      avg_peer_value = total*0.55+o_total*0.15+f_total*0.3
      # print "avg value of peers(%s): %s" % (len(peers), avg_peer_value)

      # compare the values
      edge = B.get_edge_data(rand_node, business)
      # print "my value: %s" % edge['stars']

      num_peers.append(len(peers))
      diff_peer.append(abs(edge['stars'] - avg_peer_value))
      diff_yelp.append(abs(edge['stars'] - Biz[business]))
      diff_biz.append(abs(edge['stars'] - b_new_score[business]))


      # found succesful!
      break
  print np.median(num_peers),
  print np.mean(num_peers),
  print np.std(num_peers)

  print np.median(diff_peer),
  print np.mean(diff_peer),
  print np.std(diff_peer)

  print np.median(diff_yelp),
  print np.mean(diff_yelp),
  print np.std(diff_yelp)


  print np.median(diff_biz),
  print np.mean(diff_biz),
  print np.std(diff_biz)

