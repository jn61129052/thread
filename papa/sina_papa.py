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
import chardet
start = time.clock()
url = "http://www.sina.com.cn"  # must add "http://"
htmlline = urllib.urlopen(url).read()
print htmlline.count('href')
def get_response_charset(charset):   
    charset = charset.lower()
    if charset == 'utf-8':
        return  'utf-8'
    elif charset == 'gb2312' or charset == 'gbk':
        return 'gbk'
def get_charset(url):      #Determine the URL-encoded
    fopen1 = urllib.urlopen(url)
    charset = fopen1.info().getparam('charset')
    if charset is not None:
        charset = get_response_charset(charset)
        return charset
    else:
        #charset = fopen1.headers['Content-Type'].split(' charset=')[1].lower()
        charset = chardet.detect(fopen1.read())['encoding']  
        charset = get_response_charset(charset)
        return charset
soup = BeautifulSoup(htmlline.decode(get_charset(url)))  
links = soup.findAll('a')
regex = re.compile(r'([A-z0-9]+[_\-]?[A-z0-9]+\.)*[A-z0-9]+\-?[A-z0-9]+\.[A-z]{2,}(\/.*)*\/?') 
count = 0
def output_file(href_link): 
    file_object = open('D:/1.txt','a')
    try:
        for i in range(0,len(href_link)-1):
            file_object.writelines(href_link[i])
    except IOError:
        print "IO Error!"
    finally:
        file_object.close()
href_link = []
for item in links:
    if 'href' in str(item):
        if regex.search(str(item)):
            linkname = item.string
            linkaddr = item['href'] 
            if 'NoneType' in str(type(linkname)):
                href_link.append(linkaddr+'\n')
                count += 1
            else: 
                href_link.append(linkname+':'+linkaddr+'\n')
                count += 1
output_file(href_link)
end = time.clock()
print end-start



