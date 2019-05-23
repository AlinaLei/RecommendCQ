#!/usr/bin/env python
# -*- coding:utf8 -*-

# 文件目录
FILE_PARENT_DIR = '/data/www/ivp/'
IMAGES_PATH='/data/www/images/'

# 每次提取数据记录数大小
FETCH_SIZE = 10000
# 输出文本文件分隔符
TXT_DELIMITER = '\t'
# 输出文本文件是否添加表头
IS_HEADER_ADDING = True

TARGET_TABLE = 'dynamic_code_set'
TIME_FIELD_NAME = 'operate_month'

# 过滤掉的sql关键字符，可以手动添加
SQL_BAD_STR = (
    "exec|execute|insert|delete|update|select|count|drop|truncate|*|chr|mid"
    "|master|char|declare|sitename|net user|xp_cmdshell|;|-|+|,|--|//|/|#|--|"
    "table|from|grant|use |group_concat|column_name|"
    "information_schema.columns|table_schema|union|where|order|by|table"
)

# 过滤掉的sql关键字符，可以手动添加
SQL_BAD_STR = (
    "exec|execute|insert|delete|update|select|count|drop|truncate|*|chr|mid"
    "|master|char|declare|sitename|net user|xp_cmdshell|;|-|+|,|--|//|/|#|--|"
    "table|from|grant|use |group_concat|column_name|"
    "information_schema.columns|table_schema|union|where|order|by|table"
)

# 文件类型
FILE_TYPE = "txt|TXT"
