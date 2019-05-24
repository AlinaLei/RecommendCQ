# !/usr/bin/env python3
# -*- coding:utf8 -*-
import numpy as np
import pandas as pd
import math

#基于共同喜欢物品计算相似度
class ItemCommonLike():
    def __init__(self,df):
        self.df = df

    ###按照用户ID来进行物品的一个汇总，生成一个用户分组后的物品列表
    def create_item_list_by_user(self, user_name, item_name):
        """
        :param df: DataFrame数据源
        :param user_name: 按照用户列名来划分
        :param item_name: 对应的物品列名比如是物品ID
        :return : 返回结果为按照用户ID 和对应的物品ID列表的字典形式
        """
        res = {}
        item_list = []
        for i in self.df.itertuples():
            res.setdefault(getattr(i, user_name), []).append(getattr(i, item_name))
        for i in res.keys():
            item_list.append(res[i])
        return item_list

    def create_item_matrics(self, items, item_len, item_name_list):
        """
        :param items 物品集合
        :param item_len 总物品数
        :return : 返回物品同现矩阵，此处实际返回为DataFrame类型
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
        计算物品相似度矩阵 这里的计算物品相似度公式为：
        分子为同时购买物品i和j的用户数，分母为购买物品i的用户数与购买物品j的用户数的乘积开根号
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

    def base_cosine_similarity(self,item_matrix,user_score):
        """
        这里引入用户评分数据，进行基于余弦的相似度计算
        分子为用户k对物品i的评分与物品j的评分的乘积进行累加按照用户来，分母为用户k对物品i的评分评分累加开根号乘以用户k对物品j的评分评分累加开根号
        :param item_matrix: 物品同现矩阵
        :param user_score: 用户评分矩阵
        :return res: 基于评分矩阵的 相似度矩阵
        """
        res = pd.DataFrame(np.zeros(item_matrix.shape), index=item_matrix.index, columns=item_matrix.columns)

        sum_score = lambda x, y: sum(x*y)
        for i in range(item_matrix.shape[0]):
            for j in range(item_matrix.shape[0] - i):
                result1 = 0.0
                result2 = 0.0
                result3 = 0.0
                #print('columns is :',item_matrix.columns[i])
                result1 += sum_score(user_score.loc[:,item_matrix.columns[i]] ,user_score.loc[:,item_matrix.columns[j+i]])
                result2 += sum_score(user_score.loc[:,item_matrix.columns[i]] ,user_score.loc[:,item_matrix.columns[i]])
                result3 += sum_score(user_score.loc[:,item_matrix.columns[j+i]] ,user_score.loc[:,item_matrix.columns[j+i]])
                res.iloc[i, j + i] =round( result1 /( math.sqrt(result2)* math.sqrt(result3)),4)  # 保留四位小数
                res.iloc[j + i, i] = res.iloc[i, j + i]
        return res

    def base_cosine_alpha_similarity(self,item_matrix,user_score,alpha=0.3):
        """
        这里引入用户评分数据和热门物品惩罚条件，
        分子为用户k对物品i的评分与物品j的评分的乘积进行累加按照用户来，分母为用户k对物品i的评分评分累加开根号乘以用户k对物品j的评分评分累加开根号
        :param item_matrix: 物品同现矩阵
        :param user_score: 用户评分矩阵
        :return res: 基于评分矩阵的 相似度矩阵
        """
        res = pd.DataFrame(np.zeros(item_matrix.shape), index=item_matrix.index, columns=item_matrix.columns)

        sum_score = lambda x, y: sum(x * y)
        for i in range(item_matrix.shape[0]):
            for j in range(item_matrix.shape[0] - i):
                result1 = 0.0
                result2 = 0.0
                result3 = 0.0
                # print('columns is :',item_matrix.columns[i])
                result1 += sum_score(user_score.loc[:, item_matrix.columns[i]],
                                     user_score.loc[:, item_matrix.columns[j + i]])
                result2 += sum_score(user_score.loc[:, item_matrix.columns[i]],
                                     user_score.loc[:, item_matrix.columns[i]])
                result3 += sum_score(user_score.loc[:, item_matrix.columns[j + i]],
                                     user_score.loc[:, item_matrix.columns[j + i]])
                res.iloc[i, j + i] = round(result1 / (math.pow(result2,alpha) * math.pow(result3,1-alpha)), 4)  # 保留四位小数
                res.iloc[j + i, i] = res.iloc[i, j + i]
        return res

    # 生成推荐结果
    def get_itemCF(self,item_matrix, user_score,user_id,K,col_name='rank'):
        """
        item_matrix: 物品相似度矩阵，DataFrame类型
        user_score:  用户评分矩阵，DataFrame类型,某一个指定的用户的评分矩阵
        col_name:    用户给新列指定的列名
        k : 用来指定返回TOP K 个物品
        return:      用户对对应的物品的兴趣值 得到的类型为DataFrame类型，
        """
        user_score = user_score.loc[user_id, :]

        columns = item_matrix.columns
        user_score = user_score[columns]
        # 过滤掉用户曾经看过的电影
        user_movie = user_score[user_score.values == 0].index

        item_matrix = np.mat(item_matrix.as_matrix(columns=None))
        user_score = np.mat(user_score.as_matrix(columns=None)).T
        result_score = item_matrix * user_score
        result = pd.DataFrame(result_score, index=columns, columns=['rating'])
        result[col_name] = columns
        result = result.sort_values(by='rating', ascending=False)
        return result[result[col_name].isin(user_movie)].head(K)
