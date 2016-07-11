#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hl_mysql
from hl_mysql import mysql_init, mysql_select

hl_mysql.mysql_debug_sql = True

mysql_init(mysql_host = '192.168.1.254', mysql_database = 'renrenbx', mysql_user = 'root', mysql_password = 'renrenbx')  

@mysql_select('select * from ui_user where id = %s')
def getUser():
  pass
  
print getUser(11)