# /usr/bin/env python3
# -*- coding:utf8 -*_
import numpy as np
""" precision ,recall ,roc  ,auc  
"""

def  Recommend(user,N):

    return None


#评估推荐系统
def precision_recall(test , N):
    """
    召回率和准确率
    :param test:
    :param N: 推荐列表长度
    :return: 返回在不同的N下的准确率/召回率
    """
    hit = 0
    n_recall = 0
    n_precision = 0
    for user ,items in test.item():
        rank = Recommand(user,N)
        hit += len(rank & items)
        n_recall += len(items)
        n_precision += N

    return [hit/(1.0 * n_recall) , hit /(1.0 * n_precision)]

def RMSE(records):
    """
    计算用户对物品的实际评分rui和算法的预测评分pui的均方根误差
    :param records: 存放用户评分数据 ，u为用户 ,i为物品
    :return:
    """
    result = 0
    count = 0
    for u ,i ,rui ,pui in records:
        count += 1
        result += pow(rui -pui)
    return np.sqrt(result)/count


def MAE(records):
    """
    计算用户对物品的实际评分rui和算法的预测评分pui的平均绝对误差
    :param records: 存放用户评分数据 ，u为用户 ,i为物品
    :return:
    """
    result = 0
    count = 0
    for u, i, rui, pui in records:
        count += 1
        result += abs(rui - pui)
    return result/count

#覆盖率  一般用信息熵和基尼系数来衡量
def Coverage():

    pass