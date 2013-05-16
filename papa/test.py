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
class Crawler(object):
    def __init__(self,Url,Dbfile):#,ThreadNum,Key,Depth,Dbfile):
        self.url = Url
#         self.threadnum = ThreadNum
#         self.key = Key
#         self.depth = Depth
        self.dbfile = Dbfile
        self.database = DataBase(self.dbfile)
        
    def get_response_charset(self,charset):
        if charset.lower() == 'utf-8' or charset.lower == 'utf8':
            return  'utf-8'
        elif charset.lower() == 'gb2312' or charset.lower() == 'gbk' or charset.lower() == 'iso-8859-1':
            return 'gb18030'
        
    def character_filter(self,character):
        character = character.replace(u'\xa0',' ').strip(u'\r\n').strip(u'\n') #BeautifulSoup can not encode ;&nbsp so replace it to ' '
        return character   
        
    def Spider(self):
        if url.strip():
            try:
                htmlline = requests.get(url.strip(),timeout = 30 )
            except Exception,e:
                print e
            if htmlline.content:
                try:
                    htmlline.encoding = self.get_response_charset(htmlline.encoding)
                    soup = BeautifulSoup(htmlline.content.decode(htmlline.encoding,'ignore'))
                except UnicodeEncodeError,e:
                    #regex1 = r'<meta.+?charset=([-\w]+)'
                    regex_charset = r'<meta.*(?:(?:charset\s*=\s*["|\']?)|(?:charset.*content\s*=\s*["|\']\s*))([\d|\w|\-]+)[;|"|\'|\s]'
                    code = re.search(regex_charset,htmlline.content)
                    htmlline.encoding = code.group(1)
                    htmlline.encoding = self.get_response_charset(htmlline.encoding)
                    soup = BeautifulSoup(htmlline.content.decode(htmlline.encoding,'ignore'))
                except TypeError,e:
                    htmlline.encoding = chardet.detect(htmlline.content)['encoding']
                    htmlline.encoding = self.get_response_charset(htmlline.encoding)
                    soup = BeautifulSoup(htmlline.content.decode(htmlline.encoding,'ignore'))
                finally:
                    #soup = BeautifulSoup(htmlline.content.decode(htmlline.encoding,'ignore'))
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
                                    #href_link.append(linkname+':'+linkaddr+'\n')
                                    href_link.append(linkaddr)
                self.database.insert_data(href_link)
                self.database.conn_stop()
                print len(href_link)
#                 for i in xrange(len(href_link)):
#                     link_url = href_link[i]
#                     print link_url
                                    
                    
class DataBase(object):
    def __init__(self,dbfile):
#         if os.path.isfile(dbfile):
#             os.remove(dbfile)
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
        self.conn.commit()
    def conn_stop(self):
        self.conn.close()
    
    
    
start = time.clock()
with open('D:/1.txt','r') as file_object:
    for url in file_object:
        print url
        Spider = Crawler(url,'D:/sql.db')
# insert = DataBase("J:/sqllite.sql")
# insert.insert_data(Spider.Spider())
        Spider.Spider()
    
end = time.clock()
print end-start