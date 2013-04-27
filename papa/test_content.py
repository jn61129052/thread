'''
Created on 2013-4-24

@author: Administrator
'''
# import re
# import urllib
# from bs4 import BeautifulSoup
# import chardet
# data = urllib.urlopen('http://www.sina.com.cn').read()
# print chardet.detect(data)['encoding']
import requests
url = 'http://www.sina.com.cn'
response = requests.get(url)
print response


