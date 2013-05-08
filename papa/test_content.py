'''
Created on 2013-4-24

@author: Administrator
'''
from bs4 import BeautifulSoup
import requests
import re
def character_filter(character):
    character = character.replace(u'\xa0',' ').strip(u'\r\n').strip(u'\n') #BeautifulSoup can not encode ;&nbsp so replace it to ' '
    return character  
def get_response_charset(charset):   
        if charset.lower() == 'utf-8' or charset.lower() == 'utf8':
            return  'utf-8'
        elif charset.lower() == 'gb2312' or charset.lower() == 'gbk' or charset.lower() == 'iso-8859-1':
            return 'gb18030'
url = 'http://www.sina.com.cn/'
html = requests.get(url)
#print html.headers['content-type'].split('charset=')[-1]
regex1 = r'<meta.*(?:(?:charset\s*=\s*["|\']?)|(?:charset.*content\s*=\s*["|\']\s*))([\d|\w|\-]+)[;|"|\'|\s]'
code = re.search(regex1,html.content)
result = code.group(1)
html.encoding = result
html.encoding = get_response_charset(html.encoding)
soup = BeautifulSoup(html.content.decode('utf-8','ignore'))
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
href_link = []
def character_filter(character):
    character = character.replace(u'\xa0',' ').strip(u'\r\n').strip(u'\n') #BeautifulSoup can not encode ;&nbsp so replace it to ' '
    return character  
for item in links:
        if 'href' in str(item):
            if regex.search(str(item)):
                linkname = item.string
                linkaddr = item['href']
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
output_file(href_link,count)
print count
