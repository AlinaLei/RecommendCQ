# !/usr/bin/env python3
# -*- coding:utf8 -*-
#import numpy as np
#import pandas as pd
import math
#基于共同喜欢物品计算相似度
class CommonLike():
    def __init__(self):


    def ItemSimilarity(train):
        """"""
        C = dict() #物品两两同时被购买次数
        W = dict() #物品相似度矩阵
        N = dict() #物品被购买用户数
        for u , items in train.items():
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
        print("C is :",C)
        print("N is :",N)
        return W