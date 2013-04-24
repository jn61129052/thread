'''
Created on 2013-4-17

@author: Administrator
'''

from bs4 import BeautifulSoup
import urllib2
import re
 
def grabHref(url):
     html = urllib2.urlopen(url).read()
     html = unicode(html,'gb2312','ignore').encode('utf-8','ignore')
     content = BeautifulSoup(html).findAll('a')
     pat = re.compile(r'href="([^"]*)"')
     pat2 = re.compile(r'http')
     for item in content:
         h = pat.search(str(item))
         href = h.group(1)
         if pat2.search(href):
             ans = href
         else:
             ans = url+href
         print ans
def main():
     url = "http://www.163.com"
     grabHref(url)
if __name__=="__main__":
     main()     