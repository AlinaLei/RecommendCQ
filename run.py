#!/usr/bin/env python3
# -*- coding:utf8 -*-
from api.core import app
from ModelFunction.ItemCF import *

if __name__ == '__main__':
    #app.run(debug=True, host='0.0.0.0', port=8018)
    Train_data ={
        'A':{'i1':1,'i2':3,'i4':4},
        'B':{'i1':1,'i4':1},
        'C':{'i1':1,'i2':1,'i5':1},
        'D':{'i2':1,'i3':1},
        'E':{'i3':1,'i5':1},
        'F':{'i2':1,'i4':1}
    }
    W= ItemSimilarity(Train_data)
    print(W)