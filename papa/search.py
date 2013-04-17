'''
Created on 2013-4-15
@author: Administrator
'''
#! /usr/bin/env python
# -*- coding: <utf-8> -*-
import urllib2 as url
import string
import urllib
import re
from string import join
import time
import MySQLdb
import sys
key = raw_input("Please input a keyword:")
page_num = int(raw_input("Please input what number you want:"))
def baidu_search(keyword):
    result = []
    for i in range(page_num):
        i = str(i)+'0'
        p = {'wd': keyword,'pn': i}
        html = url.urlopen("http://www.baidu.com/s?"+urllib.urlencode(p)).read()
        result.append(html)
        html = ' '.join(result)
    return html
def getList(regex,text):
    arr = []
    res = re.findall(regex, text)
    if res:
        for r in res:
            arr.append(r)
    return arr
def getMatch(regex,text):
    res = re.findall(regex, text)
    if res:
        return res[0]
    return ""
def clearTag(text):
    p = re.compile(u'<[^>]+>')
    retval = p.sub("",text)
    return retval
start = time.clock()
html = baidu_search(key)
content = unicode(html, 'utf-8','ignore')
arrList = getList(u"<table.*?class=\"result\".*?>.*?<\/a>", content)
for item in arrList:
    regex = u"<h3.*?class=\"t\".*?><a.*?href=\"(.*?)\".*?>(.*?)<\/a>"
    link = getMatch(regex,item)
    if len(link)>0:
        url = link [0]
        title = clearTag(link[1]).encode('UTF-8').decode('UTF-8')
    else:
        print "This record is wrong!"
    try:
        conn = MySQLdb.connect(host='localhost',user='root',passwd='root',db='test',port=3306,charset='utf8')
        cursor = conn.cursor()
        value = [ title,url ]
        sql = "insert into url(id,title,url) values (NULL,%s,%s)"
        cursor.execute(sql,value)
    except MySQLdb.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        conn.commit()
        cursor.close()
        conn.close()
    print url
    print title
end = time.clock()
print end-start
