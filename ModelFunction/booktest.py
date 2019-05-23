# /usr/bin/env python3
# -*- coding:utf8 -*-
import math

def handle_data(df, user_col, item_col, rating_col):
    """
    :param df: DataFrame数据源
    :return:  处理成书本中的字典格式
    """
    #TODO 生成不出来
    result ={}
    tmp = {}
    print(type(df))
    for i in df.itertuples():
        print('i is :',i)
        result[getattr(i, user_col)] = tmp
        if getattr(i,user_col) not in result.keys():
            if getattr(i,item_col) not in tmp.keys():
                tmp[getattr(i,item_col)] = getattr(i,rating_col)

    return result


def ItemSimilarity(df):
    """

    :param df: 形式如下，可以得到和上面一样的相似度矩阵
    result = {'A': {'1': 3, '2': 2, '3': 3, '4': 4},
              'B': {'1': 3, '2': 5},
              'C': {'4': 5, '5': 3, '3': 2, '2': 4},
              'D': {'4': 5},
              'E': {'5': 2, '2': 5, '3': 3, '4': 2},
              'F': {'1': 4, '6': 5}
              }
    :return:
    """
    C = dict() #物品两两同时被购买次数
    W = dict() #物品相似度矩阵
    N = dict() #物品被购买用户数
    for u ,items in df.items():
        for i in items.keys():
            if i not in N.keys():
                N[i] = 0
            N[i] +=1
            for j in items.keys():
                if i==j:
                    continue
                if i not in C.keys():
                    C[i] = dict()
                if j not in C[i].keys():
                    C[i][j]=0
                C[i][j]+=1
    for i ,related_items in C.items():
        if i not in W.keys():
            W[i] = dict()
        for j , cij in related_items.items():
            W[i][j] = cij /math.sqrt(N[i]*N[j])
    return W

def ItemSimilarity_cos(df):
    C = dict()  # 物品两两同时被购买次数
    W = dict()  #物品相似分数
    N = dict()  # 物品被购买用户数
    for u, items in df.items():
        for i in items.keys():
            if i not in N.keys():
                N[i] = 0
            N[i] += items[i]*items[i]
            for j in items.keys():
                if i == j:
                    continue
                if i not in C.keys():
                    C[i] = dict()
                if j not in C[i].keys():
                    C[i][j] = 0
                C[i][j] += items[i]*items[j]
    for i, related_items in C.items():
        if i not in W.keys():
            W[i] = dict()
        for j, cij in related_items.items():
            W[i][j] = cij / (math.sqrt(N[i])*math.sqrt(N[j]))
    return W

#针对热门物品进行惩罚
def  ItemSimilarity_alpha(df ,alpha= 0.3):
    C = dict()  # 物品两两同时被购买次数
    W = dict()  # 物品相似分数
    N = dict()  # 物品被购买用户数
    for u, items in df.items():
        for i in items.keys():
            if i not in N.keys():
                N[i] = 0
            N[i] += items[i] * items[i]
            for j in items.keys():
                if i == j:
                    continue
                if i not in C.keys():
                    C[i] = dict()
                if j not in C[i].keys():
                    C[i][j] = 0
                C[i][j] += items[i] * items[j]
    for i, related_items in C.items():
        if i not in W.keys():
            W[i] = dict()
        for j, cij in related_items.items():
            W[i][j] = cij / (math.pow(N[i],alpha) * math.pow(N[j],1-alpha))
    return W

def Recommend(df, user_id, W, K):
    rank = dict()
    ru = df[user_id]
    for i, pi in ru.items():
        tmp = W[i]
        for j ,wj in sorted(tmp.items(), key = lambda d: d[1], reverse= True )[0:K]:
            if j not in rank.keys():
                rank[j]=0
            if j in ru:
                continue
            rank[j]+= pi*wj
    return rank 