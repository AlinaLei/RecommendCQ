#!/usr/bin/env python
# -*- coding:utf8 -*-


def unicode(s):
    """
        字符串解码
    :param s:
    :return:
    """
    if isinstance(s, str):
        try:
            return s.decode('utf-8')
        except UnicodeDecodeError:
            pass
    return s

