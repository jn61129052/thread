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
        
        self.count = 0
        #种子URL
        self.url = Url
#         self.threadnum = ThreadNum
#         self.key = Key
        #爬行深度
        self.depth = Depth
        #当前爬行深度
        self.currentdepth = 1
        #已经访问的链接
        self.href_link = []
        #经过处理的链接
        self.geturls = []
        #创建hash表，判断是否
        self.hashmap = []
        #数据库存储文件
        self.dbfile = Dbfile
        #创建数据库处理对象
        self.database = DataBase(self.dbfile)
        
    #编码规则化处理
    def get_response_charset(self,charset):
        if charset.lower() == 'utf-8' or charset.lower == 'utf8':
            return  'utf-8'
        elif charset.lower() == 'gb2312' or charset.lower() == 'gbk' or charset.lower() == 'iso-8859-1':
            return 'gb18030'
    #BeautifulSoup 无法正确处理;&nbsp这类的字符，过滤处理类
    def character_filter(self,character):
        character = character.replace(u'\xa0',' ').strip(u'\r\n').strip(u'\n') #BeautifulSoup can not encode ;&nbsp so replace it to ' '
        return character   
    #数据库关闭类
    def conn_close(self):
        self.database.conn_stop()
     
    #list去重，空间复杂度过大，pass
#     def unique(self,old_list):
#         return list(set(old_list))


    #MD5处理url，用于去重
    def md5(self,urls):
        return hashlib.new("md5", urls).hexdigest()
    
#     def handleEncoding(self,response):
#         if response.encoding == 'ISO-8859-1':
#             charset_re = re.compile("((^|;)\s*charset=)([^\"]*)", re.M)
#             charset=charset_re.search(response.content) 
#             charset=charset and charset.group(3) or None 
#             response.encoding = charset
#         return response.encoding
#         print response.encoding
    
    #主爬虫类，处理
    def Spider(self,url):
        
        if url.strip():
            try:
                global htmlline
                htmlline = requests.get(url.strip(),timeout = 3 )
                self.count += 1
            except Exception,e:
                print e
            try:
                if htmlline.content:
                     
                     try:
                         htmlline.encoding = self.get_response_charset(htmlline.encoding)
                         #soup = BeautifulSoup(htmlline.content.decode(htmlline.encoding,'ignore'))
                     except UnicodeEncodeError,e:
                         #regex1 = r'<meta.+?charset=([-\w]+)'
                         regex_charset = r'((^|;)\s*charset=)([^\"]*)'
                         #regex_charset = r'<meta.*(?:(?:charset\s*=\s*["|\']?)|(?:charset.*content\s*=\s*["|\']\s*))([\d|\w|\-]+)[;|"|\'|\s]'
                         code = re.search(regex_charset,htmlline.content)
                         htmlline.encoding = code.group(1)
                         htmlline.encoding = self.get_response_charset(htmlline.encoding)
                         #soup = BeautifulSoup(htmlline.content.decode(htmlline.encoding,'ignore'))
                     except TypeError,e:
                         print 'chardet'
                         htmlline.encoding = chardet.detect(htmlline.content)['encoding']
                         htmlline.encoding = self.get_response_charset(htmlline.encoding)
                         #soup = BeautifulSoup(htmlline.content.decode(htmlline.encoding,'ignore'))
                     finally:
                         soup = BeautifulSoup(htmlline.content)#
                     links = soup.find_all('a',href=re.compile('^http|^/'))
                     regex = re.compile(r'(https?|ftp|mms):\/\/([A-z0-9]+[_\-]?[A-z0-9]+\.)*[A-z0-9]+\-?[A-z0-9]+\.[A-z]{2,}(\/.*)*\/?')  
#                     href_link = []
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
                                #if 'NoneType' in str(type(linkname)):
                                
                                if self.md5(linkaddr) not in self.hashmap:                                   
                                    self.geturls.append(linkaddr)
                                    self.hashmap.append(self.md5(linkaddr))
                                #self.href_link.append(linkaddr)
                                #else: 
                                    #href_link.append(linkname+':'+linkaddr+'\n')
                                    #href_link.append(linkaddr)

            except Exception,e:
                print e
                pass  
             
    def depth_spider(self):
        while self.currentdepth <= self.depth:
            if len(self.href_link) == 0:
                self.href_link.append(self.url)
            print '\nCurrent depth is: %d \n' % self.currentdepth
            #print len(self.href_link)
            for i in self.href_link:
                #print i
                self.Spider(i)
            self.currentdepth += 1
            self.href_link = []
            self.href_link.extend(self.geturls)
            #print len(self.href_link)
        self.database.insert_data(self.geturls)
        self.conn_close()
        #print self.count                     
                    
class DataBase(object):
    
    conn = None
    def __init__(self,dbfile):
#         if os.path.isfile(dbfile):
#             os.remove(dbfile)

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
        
    def insert_data(self,href_link): 
        
        for i in range(len(href_link)):
            url = href_link[i]
            if url is not None:
                try:
                    self.cmd.execute("insert into Crawler (url) values(?)",(url,))
                except Exception,e:
                     print e
#         if self.count > 10000:
#             print "=================="
#             print self.count
#             print "=================="
#             self.conn.commit()
#             self.count = 0
        
    def conn_stop(self):
        self.conn.commit()
        self.conn.close()
    
    

start = time.clock()
# Spider = Crawler(url,'J:/sql.db')
# Spider.Spider()
# # class Save(DataBase):
# #     def __init__(self):
# #         DataBase.conn_stop(self)
# #         self.database.conn_stop()
# def main():
#     for i in range(10):
#         t = ThreadClass(urlQueue)
#         t.setDaemon(True)
#         t.start()
    




Spider = Crawler('J:/sql.db',2,'http://www.sina.com.cn') 
'''
In order to enhance the speed, the write 
the class url handler class alone method, the 
cycle so you do not need to repeatedly 
call the main method of handling database 
'''
# with open('J:/1.txt','r') as file_object:
# 
#     for url in file_object:
#         print url
Spider.depth_spider()
#     save = Save()
#     save()
        
        
    
end = time.clock()
print end-start