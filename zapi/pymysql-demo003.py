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
# cursor.execute("select hostid,host from test.hosts where host like '%pp%' ")
for line in open("sql/pymysql-demo003.sql"):  # 从文件里一行一行的读
    print '---------- new sql query ----------'
    cursor.execute(line)
    res = cursor.fetchall()  # 所有的数据一起返回
    for x in res:
        bcnt = 0
        ecnt = len(x)        
        for i in range(bcnt, ecnt):
            if i == (ecnt-1):
                print x[i],
            else:
                print x[i],',',
        print '次'
    
cursor.close()
conn.close()