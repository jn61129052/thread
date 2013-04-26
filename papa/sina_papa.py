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
url = "http://www.zol.com.cn/"  # must add "http://"
htmlline = urllib.urlopen(url).read()
def get_response_charset(charset):   
    if charset.lower() == 'utf-8':
        return  'utf-8'
    elif charset.lower() == 'gb2312' or charset.lower() == 'gbk':
        return 'gb18030'
def get_charset(url):      #Determine the URL-encoded
    fopen1 = urllib.urlopen(url)
    charset = fopen1.info().getparam('charset')
    if charset is not None:
        return get_response_charset(charset)
    else:
        #charset = fopen1.headers['Content-Type'].split(' charset=')[1].lower()
        charset = chardet.detect(fopen1.read())['encoding']
        return get_response_charset(charset)
soup = BeautifulSoup(htmlline.decode(get_charset(url),'ignore'))  
#soup = BeautifulSoup(htmlline.decode('gbk','ignore'))  
links = soup.findAll('a')
# for i in range(0,len(links)):
#     print links[i]
regex = re.compile(r'([A-z0-9]+[_\-]?[A-z0-9]+\.)*[A-z0-9]+\-?[A-z0-9]+\.[A-z]{2,}(\/.*)*\/?')  
count = 0
def output_file(href_link,count): 
    file_object = open('J:/1.txt','a')
    try:
        #for i in range(0,len(href_link)):
        for i in range(0,count):
            #print href_link[i]
            try:
                file_object.writelines(href_link[i])
            except UnicodeEncodeError,e:
                print e
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
            if linkname is not None:  #BeautifulSoup can not encode ;&nbsp so replace it to ' '
                linkname = linkname.replace(u'\xa0',' ')
                linkname = linkname.strip(u'\r\n') 
                linkname = linkname.strip(u'\n')
                if 'NoneType' in str(type(linkname)):
                    href_link.append(linkaddr+'\n')
                    count += 1
                else: 
                    href_link.append(linkname+':'+linkaddr+'\n')
                    count += 1
#print count
#print len(href_link)
output_file(href_link,count)
# for i in range(0,len(href_link)):
#     print href_link[i]
end = time.clock()
print end-start