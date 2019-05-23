#!/usr/bin/env python
# -*- coding:utf8 -*-


def is_missed_key(required_keys, data):
    for key in required_keys:
        if key not in data.keys():
            return True, {'message': u"缺失参数 '{}'".format(key)}
    return False, {}

