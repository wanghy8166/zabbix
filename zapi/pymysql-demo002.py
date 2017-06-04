#!/usr/bin/env python2.7
#coding=utf-8
import pymysql

# 创建连接，指定数据库的ip地址、端口号、账号、密码、要操作的数据库、字符集
conn = pymysql.connect(host='127.0.0.1', 
                       port=3306, 
                       user='root', 
                       passwd='root', 
                       db='test',
                       charset='utf8')
# 创建游标
cursor = conn.cursor()
# cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)#需要指定游标的类型，字典类型
# 执行SQL
cursor.execute("select hostid,host from test.hosts where host like '%pp%' ")
# 获取返回结果，这个时候返回结果是一个?
# res = cursor.fetchone()#返回一条数据，如果结果是多条的话
# print(res)
res = cursor.fetchall()#所有的数据一起返回
# print res
for x in res:
    print x[1],',状态改变次数:',x[0],'次'

cursor.close()
conn.close()