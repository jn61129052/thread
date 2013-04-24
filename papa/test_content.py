'''
Created on 2013-4-24

@author: Administrator
'''
import re
import urllib2
from bs4 import BeautifulSoup
# def get_response_charset(charset):
#     if charset == 'utf-8':
#         return charset
#     elif charset == 'gb2312' or charset == 'GBK':
#         charset = 'GBK'
#         return charset
# def get_charset(url):      #Determine the URL-encoded
#     fopen1 = urllib.urlopen(url)
#     charset = fopen1.info().getparam('charset')
#     if charset:
#         charset = get_response_charset(charset)
#         return charset
#     else:
#         charset = fopen1.headers['Content-Type'].split(' charset=')[1].lower()
#         charset = get_response_charset(charset)
#         return charset
def work(url):
    try:
        html = urllib2.urlopen(url).read()
    except UnicodeError,e:
        return None
    except Exception,e:
        return None
    soup = BeautifulSoup(html)
    links = soup.find('a')
    return links
if __name__ == '__main__':
    url = "https://github.com/"
    print work(url)
    