#!/usr/bin/env python
# -*- coding:utf8 -*-
import datetime


def get_now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

