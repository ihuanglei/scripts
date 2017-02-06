#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import functools
import MySQLdb

mysql_debug_sql = False

mysql_charset = 'utf8'
mysql_host = '127.0.0.1'
mysql_database = ''
mysql_user = 'root'
mysql_password = ''


def mysql_init(**opts):
    global mysql_charset, mysql_host, mysql_database, mysql_user, mysql_password
    if 'mysql_charset' in opts:
        mysql_charset = opts['mysql_charset']
    if 'mysql_host' in opts:
        mysql_host = opts['mysql_host']
    if 'mysql_database' in opts:
        mysql_database = opts['mysql_database']
    if 'mysql_user' in opts:
        mysql_user = opts['mysql_user']
    if 'mysql_password' in opts:
        mysql_password = opts['mysql_password']


def _getConnect():
    connect = MySQLdb.connect(host=mysql_host, user=mysql_user,
                              passwd=mysql_password, db=mysql_database, charset=mysql_charset)
    return connect


def _query(sql, param=None):
    try:
        placeholders = []
        real_params = []
        for p in param:
            if isinstance(p, list):
                placeholders.append(','.join(['%s'] * len(p)))
                real_params.extend(p)
            else:
                real_params.append(p)
                placeholders.append('%s')
        sql = sql % tuple(placeholders)
        param = real_params
        connect = _getConnect()
        cursor = connect.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cursor.execute(sql, param)
        if mysql_debug_sql:
            print cursor._executed
        result = cursor.fetchall()
        cursor.close()
        connect.close()
        return result
    except Exception, e:
        print e


def _update(sql, param=None):
    try:
        connect = _getConnect()
        cursor = connect.cursor()
        result = cursor.execute(sql, param)
        if mysql_debug_sql:
            print cursor._executed
        cursor.close()
        connect.commit()
        connect.close()
        return result
    except Exception, e:
        connect.rollback()
        print e


def mysql_select(sql, **opts):
    result = 'return'
    if 'result' in opts:
        result = opts['result']

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = _query(sql, args)
            if result == 'param':
                kwargs['mysql_result'] = data
                func(*args, **kwargs)
            elif result == 'return':
                return data
        return wrapper
    return decorator


def mysql_update(sql):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args):
            return _update(sql, args)
        return wrapper
    return decorator
