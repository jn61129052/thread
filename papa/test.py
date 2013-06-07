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
        
        #����URL
        self.url = Url
#         self.threadnum = ThreadNum
#         self.key = Key
        #�������
        self.depth = Depth
        #��ǰ�������
        self.currentdepth = 1
        #�Ѿ����ʵ�����
        self.currenturls = []
        #�������������
        self.result = []
        #����hash���ж��Ƿ��Ѿ���ȡ
        self.hashmap = []
        #���ݿ�洢�ļ�
        self.dbfile = Dbfile
        #�������ݿ⴦�����
        self.database = DataBase(self.dbfile)
        
    #BeautifulSoup �޷���ȷ����;&nbsp������ַ������˴�����
    def character_filter(self,character):
        character = character.replace(u'\xa0',' ').strip(u'\r\n').strip(u'\n') #BeautifulSoup can not encode ;&nbsp so replace it to ' '
        return character   
    #���ݿ�ر���
    def conn_close(self):
        self.database.conn_stop()

    #MD5����url������ȥ��
    def md5(self,urls):
        return hashlib.new("md5", urls).hexdigest()
    
    #httpͷ���
    def http(self,url):
        if not url.startswith('http://'):
            url = 'http://' + url
        return url

    #�������࣬����
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
            
    #������������       
    def GetChildsByParent(self,parent):
        curr = self.Spider(parent)
        return curr
    
    #���ص�ǰ��url
    def GetChilds(self,parents):
        ReturnValue = []
        for i in parents:
            try:
                ReturnValue.extend(self.GetChildsByParent(i))
            except TypeError:
                pass
        return ReturnValue
    
    #ȥ�ط���
    def repeat(self,url):
        if self.md5(url) not in self.hashmap:
            self.hashmap.append(self.md5(url))
            return True
        else:
            return False
    
    #���з���
    def start(self):

        self.currenturls.append(self.url)    #currenturls�Ǹ�����
        while self.currentdepth <= self.depth:
            print '\nCurrent depth is: %d \n' % self.currentdepth
            self.currenturls = self.GetChilds(self.currenturls)
            for i in self.currenturls:
                if self.repeat(i):
                    self.result.append(i)
            self.currentdepth += 1
        self.database.insert_data(self.result)
        self.conn_close()
          
#���ݿ���              
class DataBase(object):
    conn = None
    
    #�������ݿ��
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
    
    #��������
    def insert_data(self,href_link): 
        for i in range(len(href_link)):
            url = href_link[i]
            if url is not None:
                try:
                    self.cmd.execute("insert into Crawler (url) values(?)",(url,))
                except Exception,e:
                     print e
    #���ݿ�ر�
    def conn_stop(self):
        self.conn.commit()
        self.conn.close()
    
    

start = time.clock()
Spider = Crawler('J:/sql.db',2,'www.sina.com.cn') 
Spider.start()
end = time.clock()
print end-start