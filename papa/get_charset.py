'''
Created on 2013-4-23

@author: Administrator
'''
import urllib
import requests
url = "http://www.sina.com.cn/"  # must add "http://"
html = requests.get(url)
def get_response_charset(charset):   
    if charset.lower() == 'utf-8':
        return  'utf-8'
    elif charset.lower() == 'gb2312' or charset.lower() == 'gbk' or charset.lower() == 'iso-8859-1':
        return 'gb18030'
#print html.text
#chardet = html.headers['content-type']
#print chardet.split(';')

#print get_response_charset(html.encoding)
html.encoding = get_response_charset(html.encoding)
print html.text
        