# !/usr/bin/env python3
# -*- coding:utf8 -*-

#基于用户的协同过滤
def UserCF(user, train, W):
    #build inverse table for item_users
    pass
    """
    rank = dict()
    iteracted_items = train[user]
    for v, wuv in sorted(W[u].items, key = itemgetter(1), reverse=True
                         )[0:K]:
        for i, rvi in train[v].items:
            if i in iteracted_items:
            rank[i] += wuv*rvi
        return rank
    """