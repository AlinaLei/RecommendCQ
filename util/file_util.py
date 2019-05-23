#!/usr/bin/env python
# -*- coding:utf8 -*-
from datetime import datetime


def get_ymd_dir(root_dir):
    current_time = datetime.now()
    year = current_time.strftime('%Y')
    month = current_time.strftime('%Y%m')
    date = current_time.strftime('%Y%m%d')
    return root_dir + year + '/' + month + '/' + date + '/'

