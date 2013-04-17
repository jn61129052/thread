'''
Created on 2013-4-16

@author: Administrator
'''
import re
def IsURL(str_url):
    strRegex = "^((https|http)?://)"
    if getMatch(strRegex, str_url):
        return True
    else:
        return False
def getMatch(regex,text):
    res = re.findall(regex, text)
    if res:
        return res[0]
    return ""
def clearTag(text):
    p = re.compile(u'<[^>]+>')
    retval = p.sub("",text)
    return retval
item = '<a href="http://news.sina.com.cn/z/mgbsdmlsqdbz/" target="_blank">Bostion</a>'
regex = u"<a.*?href=\"(.*?)\".*?>(.*?)<\/a>"
link = getMatch(regex,item).IsURL()
if len(link)>0:
    url = link [0]
    title = clearTag(link[1]).encode('UTF-8').decode('UTF-8')
else:
    return False
print url
print title
