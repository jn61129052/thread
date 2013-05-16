'''
Created on 2013-4-28

@author: Administrator
'''
import re
from bs4 import BeautifulSoup
import time
from string import strip
import requests
import chardet
import doctest
start = time.clock()
with open("J://1.txt","r") as url_line:
    for line in url_line:
        if line.strip():
            print line
            try:
                 htmlline = requests.get(line.strip())#,timeout = 2)
            except:
                #break
                continue
#             except requests.exceptions.TooManyRedirects,e:
#                 print e
#                 continue
            def get_response_charset(charset):   
                if charset.lower() == 'utf-8' or charset.lower == 'utf8':
                    return  'utf-8'
                elif charset.lower() == 'gb2312' or charset.lower() == 'gbk' or charset.lower() == 'iso-8859-1':
                    return 'gb18030'
            if htmlline.text is not None:
                try:
                    print htmlline.encoding
                    htmlline.encoding = get_response_charset(htmlline.encoding)
                    soup = BeautifulSoup(htmlline.content.decode(htmlline.encoding,'ignore'))
                except UnicodeEncodeError,e:
                    #regex1 = r'<meta.+?charset=([-\w]+)'
                    regex1 = r'<meta.*(?:(?:charset\s*=\s*["|\']?)|(?:charset.*content\s*=\s*["|\']\s*))([\d|\w|\-]+)[;|"|\'|\s]'
                    code = re.search(regex1,htmlline.content)
                    result = code.group(1)
                    print result
                    print e
                    htmlline.encoding = result
                    htmlline.encoding = get_response_charset(htmlline.encoding)
                    soup = BeautifulSoup(htmlline.text.decode(htmlline.encoding,'ignore'))
                except TypeError,e:
                    htmlline.encoding = chardet.detect(htmlline.content)['encoding']
                    htmlline.encoding = get_response_charset(htmlline.encoding)
                    print htmlline.encoding
                    soup = BeautifulSoup(htmlline.content.decode(htmlline.encoding,'ignore'))
                finally:
                    links = soup.find_all('a',href=re.compile('^http|^/'))
            regex = re.compile(r'(https?|ftp|mms):\/\/([A-z0-9]+[_\-]?[A-z0-9]+\.)*[A-z0-9]+\-?[A-z0-9]+\.[A-z]{2,}(\/.*)*\/?')  
            count = 0
            def output_file(href_link): 
                try:
                    with open('J:/2.txt','a') as file_object:
                        for i in range(len(href_link)):
                            try:
                                file_object.write(href_link[i])
                            except UnicodeEncodeError,e:
                                pass
                except IOError:
                    print "IO Error!"
            href_link = []
            def character_filter(character):
                character = character.replace(u'\xa0',' ').strip(u'\r\n').strip(u'\n') #BeautifulSoup can not encode ;&nbsp so replace it to ' '
                return character   
            for item in links:
                if 'href' in str(item):
                    if regex.search(str(item)):
                        linkname = item.string
                        try:
                            linkaddr = item['href']
                        except KeyError :
                            pass
                        if linkname is not None:  
                            character_filter(linkname)
                            character_filter(linkaddr)
                            if 'NoneType' in str(type(linkname)):
                                href_link.append(linkaddr+'\n')
                                count += 1
                            else: 
                                #href_link.append(linkname+':'+linkaddr+'\n')
                                href_link.append(linkaddr+'\n')
                                count += 1
            print count
            output_file(href_link)    # do something here
doctest.testmod()
end = time.clock()
print end-start     