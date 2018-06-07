#!/usr/bin/python 
#-*- coding:utf-8 -*- #设置源码文件编码为utf-8 
# /usr/local/zabbix_agents/bin/tomcat_status.py

# 参考:https://github.com/martinblech/xmltodict
# 参考:PYTHON实践50-用XMLTODICT将XML转换成字典 http://www.zengyuetian.com/?p=2699

import sys

reload(sys)
sys.setdefaultencoding( "utf-8" )

def get_error_count(var1,var2):
        #print var1,var2
        import requests
        api_url="http://"+var1+":"+var2+"/status?XML=true"
        #print api_url
        #auth=('admin','123456')
        result=requests.get(api_url)
        #return result.status_code,result.content
        return result.content

if __name__=="__main__":
        var1=str(sys.argv[1]) #ip
        var2=str(sys.argv[2]) #port
        var3=str(sys.argv[3]) #var
        #print var1
        #print var2
        #print var3 
        import xmltodict
        doc = xmltodict.parse(get_error_count(var1,var2))
        #print(doc['status']['jvm']['memory']['@free'])
        if var3 == 'maxThreads':print(doc['status']['connector'][1]['threadInfo']['@maxThreads'])
        if var3 == 'currentThreadCount':print(doc['status']['connector'][1]['threadInfo']['@currentThreadCount'])
        if var3 == 'currentThreadsBusy':print(doc['status']['connector'][1]['threadInfo']['@currentThreadsBusy'])

# ./tomcat_status.py 192.168.4.17 8086 currentThreadCount
# ./tomcat_status.py 192.168.4.18 8086 currentThreadCount
