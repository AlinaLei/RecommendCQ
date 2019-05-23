# !/usr/bin/env python3
# -*- coding:utf8 -*-
import numpy as np
import pandas as pd
import math

#基于共同喜欢物品计算相似度
class CommonLike():
    def __init__(self,df):
        self.df = df

    ###按照用户ID来进行物品的一个汇总，生成一个用户分组后的物品列表
    def create_item_list_by_user(self,df, user_name, item_name):
        """
        df: DataFrame数据源
        user_name: 按照用户列名来划分
        item_name: 对应的物品列名比如是物品ID
        return: 返回结果为按照用户ID 和对应的物品ID列表的字典形式
        """
        res = {}
        for i in df.itertuples():
            res.setdefault(getattr(i, user_name), []).append(getattr(i, item_name))
        return res

    def create_item_matrics(self,items, item_len, item_name_list):
        """
        items 物品集合
        item_len 总物品数
        return : 返回物品同现矩阵，此处实际返回为DataFrame类型
        """
        item_matrix = pd.DataFrame(np.zeros((item_len, item_len)), index=item_name_list, columns=item_name_list)
        for im in items:
            for i in range(len(im)):
                # print(i)
                for j in range(len(im) - i):
                    item_matrix.loc[im[i], im[j + i]] += 1
                    item_matrix.loc[im[j + i], im[i]] = item_matrix.loc[im[i], im[j + i]]
        return item_matrix


    def item_similarity(self,item_matrix):
        """
        计算物品相似度矩阵
        :param item_matrix:  物品同现矩阵
        :return: 物品相似度矩阵，为DataFrame类型
        """
        res = pd.DataFrame(np.zeros(item_matrix.shape), index=item_matrix.index, columns=item_matrix.columns)
        for i in range(item_matrix.shape[0]):
            for j in range(item_matrix.shape[0] - i):
                res.iloc[i, j + i] = round(
                    item_matrix.iloc[i, j + i] / math.sqrt(item_matrix.iloc[i, i] * item_matrix.iloc[j + i, j + i]),
                    4)  # 保留四位小数
                res.iloc[j + i, i] = res.iloc[i, j + i]
        return res

def ItemSimilarity(self,df):
    """"""
    C = dict() #物品两两同时被购买次数
    W = dict() #物品相似度矩阵
    N = dict() #物品被购买用户数
    for u , items in df.items():
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