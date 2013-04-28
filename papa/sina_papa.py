'''
Created on 2013-4-16

@author: Administrator
'''
#! /usr/bin/env python
import re
import urllib2 as url
import urllib
from bs4 import BeautifulSoup
import time
from string import strip
#import chardet
import requests
start = time.clock()
url = "http://www.sina.com.cn/"  # must add "http://"
htmlline = requests.get(url)
def get_response_charset(charset):   
    if charset.lower() == 'utf-8':
        return  'utf-8'
    elif charset.lower() == 'gb2312' or charset.lower() == 'gbk' or charset.lower() == 'iso-8859-1':
        return 'gb18030'
htmlline.encoding = get_response_charset(htmlline.encoding)
soup = BeautifulSoup(htmlline.text.decode(htmlline.encoding,'ignore'))  
links = soup.findAll('a')
regex = re.compile(r'([A-z0-9]+[_\-]?[A-z0-9]+\.)*[A-z0-9]+\-?[A-z0-9]+\.[A-z]{2,}(\/.*)*\/?')  
count = 0
def output_file(href_link,count): 
    file_object = open('J:/1.txt','a')
    try:
        for i in range(0,count):
            try:
                file_object.write(href_link[i])
            except UnicodeEncodeError,e:
                print e
    except IOError:
        print "IO Error!"
    finally:
        file_object.close()
href_link = []
def character_filter(character):
    character = character.replace(u'\xa0',' ').strip(u'\r\n').strip(u'\n')
    return character   
for item in links:
    if 'href' in str(item):
        if regex.search(str(item)):
            linkname = item.string
            linkaddr = item['href']
            if linkname is not None:  #BeautifulSoup can not encode ;&nbsp so replace it to ' '
                character_filter(linkname)
                character_filter(linkaddr)
                if 'NoneType' in str(type(linkname)):
                    href_link.append(linkaddr+'\n')
                    count += 1
                else: 
                    href_link.append(linkname+':'+linkaddr+'\n')
                    count += 1
output_file(href_link,count)
end = time.clock()
print end-start