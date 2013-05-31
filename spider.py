#------coding:utf-8------

import re
import os
import sys
import time
import urllib2
import sqlite3
import logging
from urlparse import urljoin
from Queue import Queue
from bs4 import BeautifulSoup
from threading import Thread
from datetime import datetime
from optparse import OptionParser
from locale import getdefaultlocale
from threadPool import ThreadPool

logger = logging.getLogger()

#椤甸潰鐖绫�
class Crawler(object):
	def __init__(self,url,depth,threadNum,dbfile,key):
		#瑕佽幏鍙杣rl鐨勯槦鍒�
		self.urlQueue = Queue()
		#璇诲彇鐨刪tml闃熷垪
		self.htmlQueue = Queue()
		#宸茬粡璁块棶鐨剈rl
		self.readUrls = []
		#鏈闂殑閾炬帴
		self.links = []
		#绾跨▼鏁�
		self.threadNum = threadNum
		#鏁版嵁搴撴枃浠跺悕
		self.dbfile = dbfile
		#鍒涘缓瀛樺偍鏁版嵁搴撳璞�
		self.dataBase = SaveDataBase(self.dbfile) 
		#鎸囩偣绾跨▼鏁扮洰鐨勭嚎绋嬫睜
		self.threadPool = ThreadPool(self.threadNum)
		#鍒濆鍖杣rl闃熷垪
		self.urlQueue.put(url)
		#鍏抽敭瀛�浣跨敤console鐨勯粯璁ょ紪鐮佹潵瑙ｇ爜
		self.key = key.decode(getdefaultlocale()[1]) 
		#鐖娣卞害
		self.depth = depth
		#褰撳墠鐖娣卞害
		self.currentDepth = 1
		#褰撳墠绋嬪簭杩愯鐘舵�
		self.state = False
		
	#鑾峰彇褰撳墠椤甸潰鐨刄RL
	def work(self,url):
		try:
			html = urllib2.urlopen(url).read()
		except UnicodeError,e:
			self.urlQueue.put(url.encode('raw_unicode_escape'))
			logger.warninng(e)
			return None
		except Exception,e:
			logger.warninng(e)
			return None
		soup = BeautifulSoup(html)	
		allUrl = soup.find_all('a',href=re.compile('^http|^/'))
		if url.endswith('/'):
			url = url[:-1]
		for i in allUrl:
			if i['href'].startswith('/'):
				i['href'] = url + i['href']
			#濡傛灉璇ラ摼鎺ヤ笉鍦ㄥ凡缁忚鍙栫殑URL鍒楄〃涓紝鎶婂畠鍔犲叆璇ュ垪琛ㄥ拰闃熷垪
			if i['href'] not in self.readUrls:
				self.readUrls.append(i['href'])
				self.links.append(i['href'])
			#	print i['href'] #鏄剧ず鑾峰彇鐨勯摼鎺�
		if html:
			self.htmlfilter(url,html)
				
	#鍖归厤鍏抽敭瀛�
	def htmlfilter(self,url,html):
		try:
			if self.key:
				soup = BeautifulSoup(html)
				re_string = key.split()
				#鏌ユ壘鍏抽敭瀛�
				if soup.findAll('meta',content = re.compile(re_string)):
					self.htmlQueue.put((url,key,html))
			else:
				self.htmlQueue.put((url,'',html))
		except Exception,e:
			logger.warninng
	def start(self):
		self.state = True
		print '\n[-] Start Crawling.........\n'
		self.threadPool.startThreads()
		#鍒ゆ柇褰撳墠娣卞害锛岀‘瀹氭槸鍚︾户缁�
		while self.currentDepth <= self.depth:
			while not self.urlQueue.empty():
				url = self.urlQueue.get()
				self.threadPool.addJob(self.work,url)	#鍚戠嚎绋嬫睜涓坊鍔犲伐浣滀换鍔�
				self.readUrls.append(url)	#娣诲姞宸茶闂殑url
				self.dataBase.save(self.htmlQueue)	#淇濆瓨鍒版暟鎹簱
				self.threadPool.workJoin()
			#鎶婅幏鍙栧綋鍓嶆繁搴︽湭璁块棶鐨勯摼鎺ユ斁鍏rl闃熷垪	
			for i in self.links:
				self.urlQueue.put(i)
			currentTime = int(time.time())	#褰撳墠鏃堕棿
			self.currentDepth += 1
		#缁撴潫浠诲姟
		self.stop()

	def stop(self):
		self.state = False
		self.threadPool.stopThreads()
		self.dataBase.stop()

#瀛樺偍鏁版嵁搴撶被
class SaveDataBase(object):
	def __init__(self,dbfile):
		#绉婚櫎鐜版湁鐨勫悓鍚嶆暟鎹簱
		if os.path.isfile(dbfile):
			os.remove(dbfile)
		#鏁版嵁搴撳垱寤洪摼鎺�
		self.conn = sqlite3.connect(dbfile)
		#璁剧疆鏀寔涓枃瀛樺偍
		self.conn.text_factory = str
		self.cmd = self.conn.cursor()
		self.cmd.execute('''
			create table if not exists data(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				url text,
				key text,
				html text
				)
		''')
		self.conn.commit()

	#淇濆瓨椤甸潰浠ｇ爜
	def save(self,htmlQueue):
		while not htmlQueue.empty():
			(url,key,html) = htmlQueue.get()
			try:
				self.cmd.execute("insert into data (url,key,html) values (?,?,?)",(url,key,html))
				self.conn.commit()
			except Exception,e:
				logger.warninng(e)
				
	#鍏抽棴鏁版嵁搴撹繛鎺�
	def stop(self):
		self.conn.close()

class printInfo(Thread):
	def __init__(self,Crawler):
		Thread.__init__(self)
		self.startTime = datetime.now()
		self.daemon = True
		self.Crawler = Crawler
		self.start()
	def run(self):
		while True:
			if self.Crawler.state == True:
				time.sleep(10)
				print '[+] CurrentDepth : %d, Totally visited %d Links.\n'%(self.Crawler.currentDepth,len(self.Crawler.readUrls))
				logger.info('CurrentDepth : %d, Totally visited %d Links.\n'%(self.Crawler.currentDepth,len(self.Crawler.readUrls)))
	def printEnd(self):
		self.endTime = datetime.now()
		print 'Crawl Depth: %d, Totally visited %d Links.\n'%(self.Crawler.currentDepth - 1,len(self.Crawler.readUrls)) 
		print 'Start at: %s' % self.startTime
		print 'End at  : %s' % self.endTime
		print 'Spend time: %s\n' % (self.endTime - self.startTime) + 'Finish!'

#鏃ュ織閰嶇疆鍑芥暟
def logConfig(logFile,logLevel):
	#绉婚櫎鐜版湁鐨勫悓鍚嶆棩蹇楁枃浠�
	if os.path.isfile(logFile):
		os.remove(logFile)
	#鏁板瓧瓒婂ぇ璁板綍瓒婅缁�
	LEVELS = {
		1:logging.CRITICAL,
		2:logging.ERROR,
		3:logging.WARNING,
		4:logging.INFO,
		5:logging.DEBUG
	}
	level = LEVELS[logLevel]
	logging.basicConfig(filename = logFile,level = level)
	formatter = logging.Formatter('%(actime)s %(levelname)s %(message)s')

#绋嬪簭鑷妯″潡
def testself(dbfile):

	print 'Starting TestSelf ......\n'
	#娴嬭瘯缃戠粶锛屼互鑾峰彇鐧惧害婧愮爜涓虹洰鏍�
	url = "http://www.baidu.com"
	netState = True		#缃戠粶鐘舵�
	pageSource = urllib2.urlopen(url).read()
	if pageSource == None:	#鑾峰彇涓嶅埌婧愮爜锛岀綉缁滅姸鎬佽涓篎alse
		print 'Please check your network.'
		netState = False
	#娴嬭瘯鏁版嵁搴�
	try:
		conn = sqlite3.connect(dbfile)
		cur = conn.cursor()
		cur.execute('''
			create table if not exists data (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			url text,
			key text,
			html text
			)
		''')
	except Exception,e:
		conn = None
	# 鍒ゆ柇鏁版嵁搴撳拰缃戠粶鐘舵�
	if conn == None:
		print 'DataBase Error!'
	elif netState:
		print 'The Crawler runs normally!'

if __name__ == '__main__':
	helpInfo = '%prog -u url -d depth'
	#鍛戒护琛屽弬鏁拌В鏋�
	optParser = OptionParser(usage = helpInfo)
	optParser.add_option("-u",dest="url",type="string",help="Specify the begin url.")
	optParser.add_option("-d",dest="depth",type="int",help="Specify the crawling depth.")
	optParser.add_option("-f",dest="logFile",default="spider.log",type="string",help="The log file path, Default: spider.log.")
	optParser.add_option("-l",dest="logLevel",default="3",type="int",help="The level(1-5) of logging details. Larger number record more details. Default: 3")
	optParser.add_option("--thread",dest="thread",default="10",type="int",help="The amount of threads. Default: 10.")
	optParser.add_option("--dbfile",dest="dbfile",default="data.sql",type="string",help="The SQLite file path. Default:data.sql")
	optParser.add_option("--key",metavar="key",default="",type="string",help="The keyword for crawling. Default: None.")
	optParser.add_option("--testself",action="store_false",dest="testself",help="TestSelf")
	(options,args) = optParser.parse_args()
	#褰撳弬鏁颁腑鏈塼estself鏃讹紝鎵ц鑷
	if options.testself:
		testself(options.dbfile)
		#exit()
	#褰撲笉杈撳叆鍙傛暟鏃讹紝鎻愮ず甯姪淇℃伅
	if len(sys.argv) < 5:
		print optParser.print_help()
	else:
		logConfig(options.logFile,options.logLevel)	#鏃ュ織閰嶇疆
		spider = Crawler(options.url,options.depth,options.thread,options.dbfile,options.key)	
		info = printInfo(spider)
		spider.start()
		info.printEnd()
