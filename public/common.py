#!/usr/bin/env python
# -*- coding:utf8 -*-
from public import mysql_db
import json



def true_return(data, msg):
    return {
        "status": True,
        "data": data,
        "msg": msg
    }


def false_return(data, msg):
    return {
        "status": False,
        "data": data,
        "msg": msg
    }


# 写进工作流日志系统
def create_log(module_id,describe,user_id=0,source =1,status=0,error=None):
    try:
        mysql = mysql_db.MysqlClient()
        error = error.replace("'", "\\\'")
        error = error.replace('"', '\\\"')
        sql ="""insert into vp_log ( module_id,user_id,add_time,source,status,describe,error_message) values({},{},sysdate,'{}',{},'{}','{}') """.format(module_id,user_id,source,status,describe, error )
        mysql.ddl(sql)
    except Exception as e:
        print(str(e))


def create_user_log(module_id,describe,user_id=0,source =1,status=0,error=None):
    try:
        mysql = mysql_db.MysqlClient()
        error = error.replace("'", "\\\'")
        error = error.replace('"', '\\\"')
        sql = "insert into log_api ( api_id,user_id,add_time,source,status_api,describe_api,message) values({},{},sysdate,'{}',{},'{}','{}')".format(module_id,user_id,source,status,describe,error)
        print(sql)
        mysql.ddl(sql)
    except Exception as e:
        print(str(e))

