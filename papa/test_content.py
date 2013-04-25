'''
Created on 2013-4-24

@author: Administrator
'''
import re
import urllib2
from bs4 import BeautifulSoup
def get_charset(url):      #Determine the URL-encoded
    fopen1 = urllib2.urlopen(url)
    charset_html = fopen1.headers['Content-Type'].split(' charset=')[1].lower()
    print charset_html
    charset = fopen1.info().getparam('charset')
    print charset
    if charset is None:
        charset = get_html_charset(fopen1)
        return charset
    else:
        charset = get_response_charset(charset)
        return charset
def get_html_charset(html):
    charset_html = html.headers['Content-Type'].split(' charset=')[1].lower()
    print charset_html
    charset = get_response_charset(charset_html)
    return charset
def get_response_charset(charset):
    charset = charset.lower()
    print charset
    if charset == 'utf-8':
        return charset
    elif charset == 'gb2312' or charset == 'gbk':
        charset = 'gbk'
        return charset
if __name__ == '__main__':
    url = "http://www.sina.com.cn/"
    print get_charset(url)
    