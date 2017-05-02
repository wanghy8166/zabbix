#!/usr/bin/env python2.7
#coding=utf-8
import json
import urllib2
import configparser
# from datetime import datetime
import time
from collections import Counter
# import pandas as pd

class zabbixtools:
    def __init__(self, url="", user="", passwd=""):
        self.url = url
        self.header = {"Content-Type": "application/json"}
        self.user = user
        self.passwd = passwd
        self.authID = self.user_login()

    def user_login(self):
        data = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "user.login",
                    "params": {
                        "user": self.user,
                        "password": self.passwd,
                        },
                    "id": 0
                    })
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key,self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Auth Failed, Please Check Your Name And Password:",e.code
        else:
            response = json.loads(result.read())
            result.close()
            authID = response['result']
            print '认证成功,authID为:',authID
            return authID

    def get_data(self,data,hostip=""):
        request = urllib2.Request(self.url,data)
        for key in self.header:
            request.add_header(key,self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server could not fulfill the request.'
                print 'Error code: ', e.code
            return 0
        else:
            response = json.loads(result.read())
            result.close()
            # print 'get_data-response为:',response
            return response

    def host_get(self,hostid=""):
        if hostid != "":
            temp = {"hostid": [hostid]}
        else:
            temp = {}
        data = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "host.get",
                    "params": {
                        "output": ["hostid", "name", "status", "host"],
                        "filter": temp,
                        # "countOutput": True,             #返回结果数量;flag类型,要么为True,要么注释这一行
                        "sortfield": "name",
                        "sortorder": "DESC"
                        },
                    "auth": self.authID,
                    "id": 1
                })
        res = self.get_data(data)['result']
        # print 'host_get-res为:',res
        return res

    def alert_get(self):
        now = time.time()
        midnight = now - (now % 86400) + time.timezone
        # print midnight- 60 * 60 * 2,midnight
        # print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(midnight- 60 * 60 * 2)),time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(midnight))
        temp = {"esc_step": "1"}        # 只显示PROBLEM的警告
        """
        if hostid != "":
            temp2 = {"hostid": [hostid]}
        else:
            temp2 = {}
        """ 
        data = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "alert.get",
                    "params": {
                        "output": "extend",
                        # "output": ["hostids", "esc_step", "subject"],
                        "time_from": midnight - 60 * 60 * 24,
                        "time_till": midnight,
                        "filter": temp,
                        # "hostid": temp2,
                        # "countOutput": True,             #返回结果数量;flag类型,要么为True,要么注释这一行
                        # "sortfield": "name",
                        # "sortorder": "DESC"
                        },
                    "auth": self.authID,
                    "id": 1
                })
        res = self.get_data(data)['result']
        # print 'alert_get-res为:',res
        return res

if __name__ == "__main__":
    # main()
    config = configparser.ConfigParser()
    config.read("config.ini") 
    web    = config.get("api","web")
    user   = config.get("api","user")
    passwd = config.get("api","passwd")
    print 'config.ini读取结果:',web,user,'******'
    tool = zabbixtools(web, user=user, passwd=passwd)

    print '----------'
    # 显示:主机
    # print 'tool.host_get:',tool.host_get()
    # for h in tool.host_get():print h['hostid'],',', h['host'] ,',', h['name'].encode('utf-8'),',', h['status']
    # for h in tool.host_get():print h['hostid'], h['name'].encode('utf-8')
    # print '----------'

    # 显示:警告
    # print 'tool.alert_get:',tool.alert_get()
    # for a in tool.alert_get():print a
    # for a in tool.alert_get():print a['esc_step'],a['eventid']
    # print '----------'

    # 警告的去重、计数
    lst=[]
    cnt=0
    for a in tool.alert_get():
        lst.append(a['subject'])        #提取需要的字段、赋值
    # Counter类，分类统计，most_common()返回一个TopN列表
    d = Counter(lst).most_common()
    for i in d:
        print i[0],'出现了',i[1],'次。'
        cnt=cnt+i[1]
    print '合计：',cnt,'次。' 
