#!/usr/bin/python
#-*- coding: gbk -*-
#coding=gbk 
'''
Created on 2013-5-7

@author: Administrator
'''
from bs4 import BeautifulSoup
import re
import requests
import chardet
import time
import sqlite3
import os
import hashlib
import Queue
import threading
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# 
# urlQueue = Queue.Queue()
# 
# class ThreadClass(threading.Thread):
#     def __init__(self,urlQueue):
#         self.urlQueue = urlQueue
#     
#     def run(self):
#         while True:
#             host = self.urlQueue.get()
#             self.urlQueue.task_done()
            
class Crawler(object):
    def __init__(self,Dbfile,Depth,Url):#,ThreadNum,Key):
        
        #种子URL
        self.url = Url
#         self.threadnum = ThreadNum
#         self.key = Key
        #爬行深度
        self.depth = Depth
        #当前爬行深度
        self.currentdepth = 1
        #已经访问的链接
        self.currenturls = []
        #经过处理的链接
        self.result = []
        #创建hash表，判断是否已经爬取
        self.hashmap = []
        #数据库存储文件
        self.dbfile = Dbfile
        #创建数据库处理对象
        self.database = DataBase(self.dbfile)
        
    #BeautifulSoup 无法正确处理;&nbsp这类的字符，过滤处理类
    def character_filter(self,character):
        character = character.replace(u'\xa0',' ').strip(u'\r\n').strip(u'\n') #BeautifulSoup can not encode ;&nbsp so replace it to ' '
        return character   
    #数据库关闭类
    def conn_close(self):
        self.database.conn_stop()

    #MD5处理url，用于去重
    def md5(self,urls):
        return hashlib.new("md5", urls).hexdigest()
    
    #http头检测
    def http(self,url):
        if not url.startswith('http://'):
            url = 'http://' + url
        return url

    #主爬虫类，处理
    def Spider(self,url):
        if url.strip():
            try:
                geturls = []
                global htmlline
                htmlline = requests.get(self.http(url),timeout = 3 )
            except Exception,e:
                pass
            try:
                if htmlline.text:
                    soup = BeautifulSoup(htmlline.text,from_encoding=htmlline.encoding)
                    links = soup.find_all('a',href=re.compile('^http|^/'))
                    regex = re.compile(r'(https?|ftp|mms):\/\/([A-z0-9]+[_\-]?[A-z0-9]+\.)*[A-z0-9]+\-?[A-z0-9]+\.[A-z]{2,}(\/.*)*\/?')  
                href_link = []
                for item in links:
                    if 'href' in str(item):
                        if regex.search(str(item)):
                            linkname = item.string
                            try:
                                linkaddr = item['href']
                            except KeyError :
                                pass
                            if linkname is not None:  
                                self.character_filter(linkname)
                                self.character_filter(linkaddr)
                                if 'NoneType' in str(type(linkname)):
                                    href_link.append(linkaddr)
                                else: 
                                    href_link.append(linkaddr)
                return href_link    
            except Exception,e:
                print e
                pass 
            
    #运行主爬虫类       
    def GetChildsByParent(self,parent):
        curr = self.Spider(parent)
        return curr
    
    #返回当前层url
    def GetChilds(self,parents):
        ReturnValue = []
        for i in parents:
            try:
                ReturnValue.extend(self.GetChildsByParent(i))
            except TypeError:
                pass
        return ReturnValue
    
    #去重方法
    def repeat(self,url):
        if self.md5(url) not in self.hashmap:
            self.hashmap.append(self.md5(url))
            return True
        else:
            return False
    
    #运行方法
    def start(self):

        self.currenturls.append(self.url)    #currenturls是个数组
        while self.currentdepth <= self.depth:
            print '\nCurrent depth is: %d \n' % self.currentdepth
            self.currenturls = self.GetChilds(self.currenturls)
            for i in self.currenturls:
                if self.repeat(i):
                    self.result.append(i)
            self.currentdepth += 1
        self.database.insert_data(self.result)
        self.conn_close()
          
#数据库类              
class DataBase(object):
    conn = None
    
    #创建数据库表
    def __init__(self,dbfile):
        if self.conn is None: 
            self.conn = sqlite3.connect(dbfile)
            self.conn.text_factory = str
            self.cmd = self.conn.cursor()
            self.cmd.execute('''
                create table if not exists Crawler(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url text not NULL
                    )
                ''')
            self.conn.commit()
    
    #插入数据
    def insert_data(self,href_link): 
        for i in range(len(href_link)):
            url = href_link[i]
            if url is not None:
                try:
                    self.cmd.execute("insert into Crawler (url) values(?)",(url,))
                except Exception,e:
                     print e
    #数据库关闭
    def conn_stop(self):
        self.conn.commit()
        self.conn.close()
    
    

start = time.clock()
Spider = Crawler('J:/sql.db',2,'www.sina.com.cn') 
Spider.start()
end = time.clock()
print end-start