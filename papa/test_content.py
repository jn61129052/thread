#!/usr/bin/python
#-*- coding: gbk -*-
#coding=gbk 
# 
# import time
# import threading
# import Queue
#  
# class Worker(threading.Thread):
#     def __init__(self, name, queue):
#         threading.Thread.__init__(self)
#         self.queue = queue
#         self.start()
#  
#     def run(self):
#         # ��������ѭ������֤��������һ������
#         while True:
#             # ����Ϊ�����˳��߳�
#             if self.queue.empty():
#                 break
#  
#             # ��ȡһ����Ŀ
#             foo = self.queue.get()
#  
#             # ��ʱ1Sģ����Ҫ��������
#             time.sleep(1)
#  
#             # ��ӡ
#             print self.getName(),':', foo
#  
#             # ����ϵͳ˵�������
#             self.queue.task_done()
#  
# # ����
# queue = Queue.Queue()
#  
# # ����100���������
# for i in range(100):
#     queue.put(i)
#  
# # ��10���߳�
# for i in range(10):
#     threadName = 'Thread' + str(i)
#     Worker(threadName, queue)
#  
# # �����߳�ִ����Ϻ�ر�
# queue.join()

import random

def Getseed(num):
    
    return random.sample(range(2,num),3)
    
array = Getseed(100000)
result = []
list = []
c = 1
d = 3
while c <= d:
    print '��ǰ�� %d ��' % c
    for i in range(len(array)):
        print 'array is',array[i]
        list.extend(Getseed(array[i]))
        result.extend(list)
        array = []
        array.extend(list)
    c += 1    
print len(result)
    



        



