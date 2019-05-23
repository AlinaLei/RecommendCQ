#!/usr/bin/env python
# -*- coding:utf8 -*-

from sqlalchemy import create_engine
from sqlalchemy import text
from conf.db_conf import SQL_DATABASE_URI, SQL_ECHO
import math
import codecs
import csv
from conf import main_conf
import traceback
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


class MysqlClient(object):
    def __init__(self):  # 构造函数
        self.db = create_engine(SQL_DATABASE_URI, echo=SQL_ECHO)

    def get_connection(self):
        return self.db.connect()
        
    def execute(self, sql):
        """
            执行SQL
        :param sql:
        :return:
        """
        try:
            self.db.execute(text(sql))
        except Exception as e:
            traceback.print_exc()
            print("Happen: ", repr(e))
            raise e

    def ddl(self, sql):
        try:
            self.db.execute(text(sql))
        except Exception as e:
            traceback.print_exc()
            print("Happen: ", str(e))
            raise e

    def ddl_pro(self, sql):
        try:
            self.db.execute(sql)
        except Exception as e:
            traceback.print_exc()
            print("Happen: ", str(e))
            raise e

    def insert(self, sql, params=None):
        """
            插入数据库
        :param sql:
        :param params:
        :return:
        """
        try:
            insert_sql = sql
            if params:
                insert_sql = sql.format(**params)
            # 执行sql语句
            result_proxy = self.db.execute(text(insert_sql))
            # rowcount = result_proxy.rowcount
            # new_id = result_proxy.lastrowid
            result_proxy.close()
        except Exception as e:
            traceback.print_exc()
            print("Happen: ", str(e))
            raise e
        #return new_id

    def dml(self, sql, params=None):
        """
            更新或删除数据
        :param sql:
        :param params:
        :return:
        """
        try:
            # 执行sql语句
            result_proxy = self.db.execute(text(sql.format(**params)))
            effect_row = result_proxy.rowcount
            result_proxy.close()
        except Exception as e:
            traceback.print_exc()
            print("Happen: ", str(e))
            raise e
        return effect_row

    def count(self, sql, params=None):
        """统计记录数"""
        result = 0
        try:
            query_sql = sql
            if params:
                query_sql = sql.format(**params)
            print(query_sql)
            result_proxy = self.db.execute(text('select count(*) as cnt from (' + query_sql + ') A'))
            result = result_proxy.fetchone()[0]
            result_proxy.close()
        except Exception as ex:
            traceback.print_exc()
            print('Happen:', ex)
            raise ex
        return result

    def query(self, sql, params=None):
        """ 查询数据库：显示 1个结果 """
        result = None
        try:
            query_sql = sql
            if params:
                query_sql = sql.format(**params)
            print(query_sql)
            result_proxy = self.db.execute(text(query_sql))
            rowcount = result_proxy.rowcount
            # rowcount = self.count(query_sql)  # 需优化
            if rowcount > -1:
                result = dict(result_proxy.fetchone())
            result_proxy.close()
        except Exception as ex:
            traceback.print_exc()
            print('Happen:', ex)
            raise ex
        return result

    def query_all(self, sql, params=None):
        """
            查询数据库：多个结果集
        :param sql: 接收全部的返回结果行.
        :param params: 传入参数列表
        :return:
        """
        result = []
        try:
            query_sql = sql
            if params!=None:
                query_sql = sql.format(**params)
            print(query_sql)
            result_proxy = self.db.execute(text(query_sql))
            if result_proxy.returns_rows:
                for row in result_proxy.fetchall():
                    result.append(dict(row))
            result_proxy.close()
        except Exception as ex:
            traceback.print_exc()
            print('Happen:', ex)
            raise ex
        return result

    def query_list_to_txt(self, query_str, filename):
        """
            据指定SQL查询出数据写入到指定文本文件中
        :param query_str: 查询字符串
        :param filename: 写入文件名，可以为绝对文件路径，为文件名时是相对项目路径
        :return:
        """
        with codecs.open(filename=filename, mode='w', encoding='utf-8') as f:
            # 读取配置参数
            fetch_size = main_conf.FETCH_SIZE
            delimiter = main_conf.TXT_DELIMITER
            is_headers_adding = main_conf.IS_HEADER_ADDING
            # 创建csv的一个writer， 其中分隔符取配置值
            writer = csv.writer(f, dialect='excel', delimiter=delimiter)
            try:
                result_proxy = self.db.execute(text(query_str))
                cur = result_proxy.cursor
                # 判断是否带有表头
                if is_headers_adding:
                    headers = [t[0] for t in cur.description]
                    writer.writerow(headers)

                row_cnt = self.count(query_str)  # 取得记录数
                print(row_cnt)
                fetch_times = int(math.ceil(row_cnt/fetch_size) + 1)
                for i in range(fetch_times):
                    rows = result_proxy.fetchmany(fetch_size)
                    for row in rows:
                        writer.writerow(row)
                result_proxy.close()
            except Exception as ex:
                traceback.print_exc()
                print('Happen:', ex)
                raise ex

    # def page_list(self, count_sql_prefix, page_sql_prefix, page_index, page_size, order_by, where_clause=None):
    #     result = {'total': 0, 'records': 0, 'rows': []}
    #     try:
    #         count_sql = count_sql_prefix
    #         page_sql = page_sql_prefix
    #         if where_clause is not None and where_clause.strip() != '':
    #             count_sql += ' WHERE {}'.format(where_clause)
    #             page_sql += " WHERE {}".format(where_clause)
    #         total = self.query(count_sql)['cnt']
    #         if total > 0:
    #             page_index = 1 if page_index is None else page_index
    #             page_size = 10 if page_size is None else page_size
    #             if order_by is not None and order_by != '':
    #                 page_sql += ' ORDER BY {} DESC'.format(order_by)
    #             page_sql += ' LIMIT {} OFFSET {}'.format(page_size, (page_index - 1) * page_size)
    #             print('[Page SQL]=>', page_sql)
    #             ret = self.query_all(page_sql)
    #             result.update({'total': total, 'records': len(ret), 'rows': ret})
    #     except Exception as e:
    #         traceback.print_exc()
    #         raise e
    #     return result

    def page_list(self, count_sql_prefix, page_sql_prefix, page_index, page_size, order_by, where_clause=None):
        result = {'total': 0, 'records': 0, 'rows': []}
        try:
            count_sql = count_sql_prefix
            page_sql = 'SELECT A.*,ROWNUM AS RN FROM (' + page_sql_prefix + ' ) A '
            if where_clause is not None and where_clause.strip() != '':
                count_sql += " WHERE {}".format(where_clause)
                page_sql += " WHERE {}".format(where_clause)
            total = self.query(count_sql)['cnt']
            if total > 0:
                page_index = 1 if page_index is None else page_index
                page_size = 10 if page_size is None else page_size
                if where_clause is None or where_clause.strip() == '':
                    page_sql += ' WHERE ROWNUM <= {}'.format(page_index * page_size)
                else:
                    page_sql += ' AND ROWNUM <= {}'.format(page_index * page_size)
                if order_by is not None and order_by != '':
                    page_sql += ' ORDER BY {} DESC'.format(order_by)
                page_sql = 'SELECT * FROM ({}) WHERE RN >= {}'.format(page_sql, (page_index - 1) * page_size)
                print('[Page SQL]=>', page_sql)
                ret = self.query_all(page_sql)
                result.update({'total': total, 'records': len(ret), 'rows': ret})
        except Exception as e:
            traceback.print_exc()
            raise e
        return result


