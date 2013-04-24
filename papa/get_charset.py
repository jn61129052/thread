'''
Created on 2013-4-23

@author: Administrator
'''
import urllib
url = 'http://www.163.com'
htmlline = urllib.urlopen(url).read()
print htmlline.count('href')