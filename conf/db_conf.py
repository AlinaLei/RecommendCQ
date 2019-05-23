#!/usr/bin/env python
# -*- coding:utf8 -*-


# Mysql数据库连接信息

DB_MYSQL = {
    'host': '192.168.112.154',
    'user': 'aivp',
    'passwd': 'szvp12#$',
    'db': 'orcl',
    'charset': 'utf8',
    'port': 1521
}


# Redis数据库连接信息
DB_REDIS = {
    'host': '127.0.0.1',
    'port': 6379,
    'password': 'Redis@tmkj12#$',
    'db': 1,
    'decode_responses': True
}

SQL_DATABASE_URI = 'mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}?charset={charset}'.format(**DB_MYSQL)
#SQL_DATABASE_URI = 'oracle+cx_oracle://{user}:{passwd}@{host}:{port}/{db}'.format(**DB_MYSQL)

#联调API
model_url = 'http://192.168.112.150:32008'

#接口文档地址
interface_url='http://192.168.112.153'

SQL_ECHO = True
# SQL_ECHO = False
