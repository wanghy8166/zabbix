#!/usr/bin/python 
#-*- coding:utf-8 -*- #设置源码文件编码为utf-8 

import ldap
import sys
import cx_Oracle

reload(sys)
sys.setdefaultencoding( "utf-8" )

def check_db(): 
            conn = cx_Oracle.connect('zabbix/123456@10.10.10.48:1521/hdapp')
            #print conn.version
            print '已连接到 Oracle ',conn.version,'',conn.dsn
            cursor=conn.cursor()
            #cursor.execute('select loginname from fauser where iauuid is not null and loginname like \'yhq%\'')
            cursor.execute('select loginname from fauser where iauuid is not null')
            row=cursor.fetchall()
            for x in row:
                print ''
                print x[0],
                #print type(x)
                check_ldap('cn='+x[0]) 
                #print ''
            print ''
            #except:
            #pass
            #print ip,
            #continue
            cursor.close()
            conn.close()


def check_ldap(vcode): 
    try:
            l = ldap.open("10.10.10.36")
            #l = ldap.initialize('ldap://10.10.10.36:389')

            # you should  set this to ldap.VERSION2 if you're using a v2 directory
            l.protocol_version = ldap.VERSION3
            # Pass in a valid username and password to get 
            # privileged directory access.
            # If you leave them as empty strings or pass an invalid value
            # you will still bind to the server but with limited privileges.

            username = "cn=Manager,dc=mycompany,dc=com"
            password = "123456"

            # Any errors will throw an ldap.LDAPError exception 
            # or related exception so you can ignore the result
            l.simple_bind(username, password)
    except ldap.LDAPError, e:
            print e
            # handle error however you like

    ## The next lines will also need to be changed to support your search requirements and directory
    baseDN = "dc=mycompany,dc=com"
    searchScope = ldap.SCOPE_SUBTREE
    ## retrieve all attributes - again adjust to your needs - see documentation for more options
    # None表示搜索所有属性，['cn']表示只搜索cn属性
    #retrieveAttributes = None 
    #retrieveAttributes = ['cn','givenName','userPassword']
    retrieveAttributes = ['']
    # cn=员工代码
    #searchFilter = "cn=00010018"
    #searchFilter = "cn=01"
    #print vcode
    searchFilter = vcode
    #print searchFilter 

    try:
            ldap_result_id = l.search(baseDN, searchScope, searchFilter, retrieveAttributes)
            result_set = []
            while 1:
                    result_type, result_data = l.result(ldap_result_id, 0)
                    if (result_data == []):
                            #print 'error'
                            break
                    else:
                            ## here you don't have to append to a list
                            ## you could do whatever you want with the individual entry
                            ## The appending to list is just for illustration. 
                            if result_type == ldap.RES_SEARCH_ENTRY:
                                    result_set.append(result_data)
            #print result_set
            if (result_set == []):
                    print 'NoResult'
                    print ''          
    except ldap.LDAPError, e:
            print e

if __name__ == "__main__":  
    #vcode = str(sys.argv[1])
    #check_ldap(vcode)
    # 执行示例 pyldap_check02.py cn=01 
    check_db()
    # 最终脚本调用 pyldap_check.py |grep -i result|wc -l
