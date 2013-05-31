#!/usr/bin/python
#-*- coding: gbk -*-
#coding=gbk 

import Queue
import threading
import time
import requests
from bs4 import BeautifulSoup

class WorkManager(object):
    def __init__(self, work_num=1000,thread_num=2):
        self.work_queue = Queue.Queue()
        self.threads = []
        self.__init_work_queue(work_num)   #���̣߳������߳���
        self.__init_thread_pool(thread_num) #���̣߳������߳���

    """
        ��ʼ���߳�
    """
    def __init_thread_pool(self,thread_num):
        for i in range(thread_num):
            self.threads.append(Work(self.work_queue))

    """
        ��ʼ����������
    """
    def __init_work_queue(self, jobs_num):
        for i in range(jobs_num):
            self.add_job(do_job, i)

    """
        ���һ������
    """
    def add_job(self, func, *args):
        self.work_queue.put((func, list(args)))#������ӣ�Queue�ڲ�ʵ����ͬ������
    """
        ���ʣ���������
    """
    def check_queue(self):
        return self.work_queue.qsize()

    """
        �ȴ������߳��������
    """   
    def wait_allcomplete(self):
        for item in self.threads:
            if item.isAlive():item.join()

class Work(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.start()

    def run(self):
        #��ѭ�����Ӷ��ô������߳���һ�������¹ر��˳�
        while True:
            try:
                do, args = self.work_queue.get(block=False)#�����첽���ӣ�Queue�ڲ�ʵ����ͬ������
                do(args)
                self.work_queue.task_done()#֪ͨϵͳ�������
            except Exception,e:
                print str(e)
                break

#����Ҫ��������
def do_job(args):
    print args
    time.sleep(0.1)#ģ�⴦��ʱ��
    print threading.current_thread(), list(args)

if __name__ == '__main__':
    start = time.time()
    work_manager =  WorkManager(100, 20)#����work_manager =  WorkManager(10000, 20)
    work_manager.wait_allcomplete()
    end = time.time()
    print "cost all time: %s" % (end-start)
