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
f = open("J://1.txt", "r")
while True:
    line = f.readline()
    if line:
        href_link = []
        try:
            htmlline = requests.get(line,timeout = 3)
            print htmlline.encoding
            print line
            def get_response_charset(charset):   
                if charset.lower() == 'utf-8' or charset.lower() == 'utf8':
                    return  'utf-8'
                elif charset.lower() == 'gb2312' or charset.lower() == 'gbk' or charset.lower() == 'iso-8859-1':
                    return 'gb18030'
            try:
                htmlline.encoding = get_response_charset(htmlline.encoding)
                soup = BeautifulSoup(htmlline.content.decode(htmlline.encoding,'ignore'))
            except UnicodeEncodeError,e:
                regex1 = r'<meta.*(?:(?:charset\s*=\s*["|\']?)|(?:charset.*content\s*=\s*["|\']\s*))([\d|\w|\-]+)[;|"|\'|\s]'
                code = re.search(regex1,htmlline.content)
                result = code.group(1)
                print result
                print e
                htmlline.encoding = result
                htmlline.encoding = get_response_charset(htmlline.encoding)
                print htmlline.encoding + '1111'
                soup = BeautifulSoup(htmlline.text.decode(htmlline.encoding,'ignore'))
            links = soup.findAll('a')
            regex = re.compile(r'(https?|ftp|mms):\/\/([A-z0-9]+[_\-]?[A-z0-9]+\.)*[A-z0-9]+\-?[A-z0-9]+\.[A-z]{2,}(\/.*)*\/?')  
            count = 0
            def output_file(href_link,count): 
                try:
                    with open('J:/2.txt','a') as file_object:
                        for i in range(0,count):
                            try:
                                file_object.write(href_link[i])
                            except UnicodeEncodeError,e:
                                pass
                except IOError:
                    print "IO Error!"
    
            def character_filter(character):
                character = character.replace(u'\xa0',' ').strip(u'\r\n').strip(u'\n') #BeautifulSoup can not encode ;&nbsp so replace it to ' '
                return character   
            for item in links:
                if 'href' in str(item):
                    if regex.search(str(item)):
                        linkname = item.string
                        linkaddr = item['href']
                        print linkaddr
                        if linkname is not None:  
                            character_filter(linkname)
                            character_filter(linkaddr)
                            if 'NoneType' in str(type(linkname)):
                                href_link.append(linkaddr+'\n')
                                count += 1
                            else: 
                               href_link.append(linkname+':'+linkaddr+'\n')
                               #href_link.append(linkaddr+'\n')
                               count += 1
#                         else:
#                             break
            output_file(href_link,count)
        except:
            pass
end = time.clock()
print end-start