# !/usr/bin/env python3
# -*- coding:utf8 -*-
import numpy as np
import pandas as pd
import math
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

#建立物品倒排索引表
class UserCommonLike():
    def __init__(self, df):
        """
        :param df: 数据源 ，初始化，使用该类都需要有数据源
        """
        self.df = df

    ###按照用户ID来进行物品的一个汇总，生成一个用户分组后的物品列表
    def create_user_list_by_item(self, user_name, item_name):
        """
        :param user_name: 按照用户列名来划分
        :param item_name: 对应的物品列名比如是物品ID
        :return : 返回结果为按照物品ID 和对应的用户ID列表的字典形式 以及单纯的用户列表汇总
        """
        res = {}
        user_list = []
        for i in self.df.itertuples():
            res.setdefault(getattr(i, item_name), []).append(getattr(i,user_name ))
        #生成除去物品ID后的用户列表汇总
        for i in res.keys():
            user_list.append(res[i])
        return user_list

    def create_user_matrics(self, users, user_len, user_name_list):
        """
        :param items 用户集合
        :param item_len 总用户数
        :return : 返回物品同现矩阵，此处实际返回为DataFrame类型
        """
        user_matrix = pd.DataFrame(np.zeros((user_len, user_len)), index=user_name_list, columns=user_name_list)
        for u in users:
            for i in range(len(u)):
                # print(i)
                for j in range(len(u) - i):
                    user_matrix.loc[u[i], u[j + i]] += 1
                    user_matrix.loc[u[j + i], u[i]] = user_matrix.loc[u[i], u[j + i]]
        return user_matrix

    ##生成用户对物品的评分表
    def user_item_score(self, user_name, item_name, score_name):
        """
        :param df:数据源
        :param user_name:  用户列名
        :param item_name:  物品列名
        :param score_name: 评分列名
        :return :     返回用户对物品的评分矩阵,此处实际返回为DataFrame类型,行为用户，列为item
        """
        user_names = self.df[user_name].unique()
        item_names = self.df[item_name].unique()
        user_n = len(user_names)
        item_n = len(item_names)
        zero_test = pd.DataFrame(np.zeros((user_n, item_n)), index=user_names, columns=item_names)
        for i in self.df.itertuples():
            zero_test.loc[getattr(i, user_name), getattr(i, item_name)] = getattr(i, score_name)
        return zero_test

    def item_similarity(self,user_matrix):
        """
        计算物品相似度矩阵 这里的计算物品相似度公式为：
        分子为同时购买物品i和j的用户数，分母为购买物品i的用户数与购买物品j的用户数的乘积开根号
        :param user_matrix:  用户同现矩阵
        :return: 物品相似度矩阵，为DataFrame类型
        """
        res = pd.DataFrame(np.zeros(user_matrix.shape), index=user_matrix.index, columns=user_matrix.columns)
        for i in range(user_matrix.shape[0]):
            for j in range(user_matrix.shape[0] - i):
                res.iloc[i, j + i] = round(
                    user_matrix.iloc[i, j + i] / math.sqrt(user_matrix.iloc[i, i] * user_matrix.iloc[j + i, j + i]),
                    4)  # 保留四位小数
                res.iloc[j + i, i] = res.iloc[i, j + i]
        return res

    def get_userCF(self, user_matrix, user_score,user_id,K,col_name='rank'):
        user_matrix = user_matrix.loc[user_id, :]
        print("user matrix is : \n", user_matrix)
        columns = user_score.columns

        user_matrix = user_matrix[user_score.index]
        print("user_score is : \n",user_score)
        # 过滤掉用户曾经看过的电影
        tmp = user_score.loc[user_id, :]
        user_item = tmp[tmp.values == 0].index
        print("user item is:\n",user_item)
        user_matrix = np.mat(user_matrix.as_matrix(columns=None))
        user_score = np.mat(user_score.as_matrix(columns=None))
        print("user score is:\n",user_score)

        result_score = (user_matrix * user_score).T
        print("resule score is :\n",result_score)
        result = pd.DataFrame(result_score, index=columns, columns=['rating'])
        result[col_name] = columns
        result = result.sort_values(by='rating', ascending=False)
        return result[result.index.isin(user_item)].head(K)