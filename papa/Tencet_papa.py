'''
Created on 2013-4-18

@author: Administrator
'''
#coding=utf-8
import sys
import urllib2
import re
import os
 
def extract_url(info):
     rege="http://news.qq.com/a/\d{8}/\d{6}.htm"
     re_url = re.findall(rege, info)
     return re_url
 
def extract_sub_web_title(sub_web):
     re_key = "<title>.+</title>"
     title = re.findall(re_key,sub_web)
     return title
 
def extract_sub_web_content(sub_web):
     re_key = "<div id=\"Cnt-Main-Article-QQ\".*</div>"
     content = re.findall(re_key,sub_web)
     return content
 
def filter_tags(htmlstr):
     re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #ƥ��CDATA
     re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
     re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
     re_p=re.compile('<P\s*?/?>')#������
     re_h=re.compile('</?\w+[^>]*>')#HTML��ǩ
     re_comment=re.compile('<!--[^>]*-->')#HTMLע��
     s=re_cdata.sub('',htmlstr)#ȥ��CDATA
     s=re_script.sub('',s) #ȥ��SCRIPT
     s=re_style.sub('',s)#ȥ��style
     s=re_p.sub('\r\n',s)#��<p>ת��Ϊ����
     s=re_h.sub('',s) #ȥ��HTML ��ǩ
     s=re_comment.sub('',s)#ȥ��HTMLע��  
     blank_line=re.compile('\n+')#ȥ������Ŀ���
     s=blank_line.sub('\n',s)
     return s
 
 #get news
content = urllib2.urlopen('http://news.qq.com').read()
 
 #get the url
get_url = extract_url(content)
 
 #generate file
f = file('result.txt','w')
i = 15            #������ʼλ�ã�ǰ�漸����ʽ��һ��
flag = 30
while True:
     f.write(str(i-14)+"\r\n")
     
     #get the sub web title and content
     sub_web = urllib2.urlopen(get_url[i]).read()
     sub_title = extract_sub_web_title(sub_web)
     sub_content = extract_sub_web_content(sub_web)
 
     #remove html tag
     if sub_title != [] and sub_content != []:
         re_content = filter_tags(sub_title[0]+"\r\n"+sub_content[0])
         f.write(re_content.decode("gb2312").encode("utf-8"))
         f.write("\r\n")
     else:
         flag = flag +1
     
     if i == flag:
         break
  
     i = i + 1
     print "Have finished %d news" %(i-15)
f.close()
