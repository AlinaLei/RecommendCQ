#!/usr/bin/env python3
# -*- coding:utf8 -*-
from api.core import app
from ModelFunction.ItemCF import *
from ModelFunction.booktest import *
from ModelFunction.UserCF import *

if __name__ == '__main__':
    #app.run(debug=True, host='0.0.0.0', port=8018)
    test = pd.read_excel("C:\\Users\\admin\\Desktop\\test.xlsx")
    """ #基于物品的协同过滤
    W = ItemCommonLike(test)
    item_list = W.create_item_list_by_user('user', 'item')
    item_name_list = test['item'].unique()
    item_metric = W.create_item_matrics(item_list, len(item_name_list), item_name_list)
    user_score=W.user_item_score('user','item','rating')
    res = W.base_cosine_alpha_similarity(item_metric,user_score)
    ress = W.get_itemCF(res, user_score, 'A', 3)
    print("the mine is:\n", ress)
    """

    #基于用户的协同过滤
    W=UserCommonLike(test)
    user_list = W.create_user_list_by_item('user','item')
    user_name_list = test['user'].unique()
    user_metrics = W.create_user_matrics(user_list, len(user_name_list),user_name_list)

    user_score =W.user_item_score('user', 'item', 'rating')
    """
    res = W.item_similarity(user_metrics)

    result = W.get_userCF( res, user_score, 'A', 3)
    print(" user list is :\n",result )
    """
    result = {'A': {'1': 3, '2': 2, '3': 3, '4': 4},
              'B': {'1': 3, '2': 5},
              'C': {'4': 5, '5': 3, '3': 2, '2': 4},
              'D': {'4': 5},
              'E': {'5': 2, '2': 5, '3': 3, '4': 2},
              'F': {'1': 4, '6': 5}
              }
    book_user_score = np.mat(user_score.as_matrix(columns=None))
    book_result = recommend(book_user_score ,1, estMethod=svdEst)
    #commom = defItemIndex(result)
    print(" the right result is :\n",book_result)

    #data_res = handle_data(test, 'user', 'item', 'rating')
    #print("data result is :",data_res)