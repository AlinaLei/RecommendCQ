#!/usr/bin/env python3
# -*- coding:utf8 -*-
from api.core import app
from ModelFunction.ItemCF import *
from ModelFunction.booktest import *

if __name__ == '__main__':
    #app.run(debug=True, host='0.0.0.0', port=8018)
    test = pd.read_excel("C:\\Users\\admin\\Desktop\\test.xlsx")
    W = CommonLike(test)
    item_list = W.create_item_list_by_user('user', 'item')
    item_name_list = test['item'].unique()
    item_metric = W.create_item_matrics(item_list, len(item_name_list), item_name_list)
    user_score=W.user_item_score('user','item','rating')
    res = W.base_cosine_alpha_similarity(item_metric,user_score)
    print("the mine is:\n", res)

    result = {'A': {'1': 3, '2': 2, '3': 3, '4': 4},
              'B': {'1': 3, '2': 5},
              'C': {'4': 5, '5': 3, '3': 2, '2': 4},
              'D': {'4': 5},
              'E': {'5': 2, '2': 5, '3': 3, '4': 2},
              'F': {'1': 4, '6': 5}
              }
    commom = ItemSimilarity_alpha(result)
    print(" the right result is :\n",commom)

    #data_res = handle_data(test, 'user', 'item', 'rating')
    #print("data result is :",data_res)