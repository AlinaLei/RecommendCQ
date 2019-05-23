#!/usr/bin/env python3
# -*- coding:utf8 -*-
import random
import pandas as pd
import numpy as np

def SplitData(data, M, k, seed):
    """
    拆分数据集为测试集和训练集
    :param data:
    :param M:
    :param k:
    :param seed:
    :return:
    """
    test = []
    train = []
    random.seed(seed)
    for user, item in data:
        if random.randint(0, M) == k:
            test.append(user, item)
        else:
            train.append(user, item)
    return train, test



###按照用户ID来进行物品的一个汇总，生成一个用户分组后的物品列表
def create_item_list_by_user(df,user_name,item_name):
    """
    df: DataFrame数据源
    user_name: 按照用户列名来划分
    item_name: 对应的物品列名比如是物品ID
    return: 返回结果为按照用户ID 和对应的物品ID列表的字典形式
    """
    res={}
    """
    for i in  range(df.shape[0]):
        k=test.loc[i,user_name]
        temp=test.loc[i,item_name]
        res.setdefault(k,[]).append(temp)
        """
    for i in df.itertuples():
        res.setdefault(getattr(i,user_name),[]).append(getattr(i,item_name))
    return res

##生成物品同现矩阵
def create_item_list(item_dict):
    item_list =[]
    for i in item_dict.keys():
        #print(item_test[i])
        #print(type(item_test[i]))
        item_list.append(item_dict[i])
    return item_list

def create_item_matrics(items,item_len,item_name_list):
    """
    items 物品集合
    item_len 总物品数
    return : 返回物品同现矩阵，此处实际返回为DataFrame类型
    """
    item_matrix =pd.DataFrame(np.zeros((item_len,item_len)),index=item_name_list,columns=item_name_list)
    for im in items:
        for i in range(len(im)):
            #print(i)
            for j in range(len(im)-i):
                item_matrix.loc[im[i],im[j+i]] +=1
                item_matrix.loc[im[j+i],im[i]] = item_matrix.loc[im[i],im[j+i]]
    return item_matrix

##生成用户对物品的评分表
def user_item_score(df,user_name,item_name,score_name):
    """
    df:数据源
    user_name:  用户列名
    item_name:  物品列名
    score_name: 评分列名
    user_n:     总用户数
    item_n:     总物品数
    return:     返回用户对物品的评分矩阵,此处实际返回为DataFrame类型
    """
    user_names=df[user_name].unique()
    item_names=df[item_name].unique()
    user_n=len(user_names)
    item_n=len(item_names)
    zero_test=pd.DataFrame(np.zeros((user_n,item_n)),index=user_names,columns=item_names)
    for i in df.itertuples():
        zero_test.loc[getattr(i,user_name),getattr(i,item_name)]=getattr(i,score_name)
    return zero_test

#生成推荐结果
def get_itemCF(item_matrix,user_score):
    """
    item_matrix: 物品同现矩阵，DataFrame类型
    user_score:  用户评分矩阵，DataFrame类型,某一个指定的用户的评分矩阵
    """
    columns=item_matrix.columns
    user_score = user_score[columns]
    item_matrix=np.mat(item_matrix.as_matrix(columns=None))
    user_score=np.mat(user_score.as_matrix(columns=None)).T
    result=item_matrix * user_score
    return pd.DataFrame(result,index=columns)






