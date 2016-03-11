#encoding:utf-8
import socket
from url_template import FUZZ_URLTemplate
from headers_template import FUZZ_HeaderTemplate
from render import *
import threading
import Queue
import select


class FuzzerManager:
    """use socket to deal with http connection"""
    def __init__(self, url = None, headers = {}, threads = 5):
        self.urls = []
        if isinstance(url, str):
            self.urls.append(url)
        elif isinstance(url, list):
            self.urls = url
        else:
            raise TypeError("Need a str or list , but get a %s" % type(url))
            
        if not isinstance(headers, dict):
            raise TypeError("Need a dict , but get a %s" % type(headers))
        else:        
            self.headers = headers
            
        self.task_queue = Queue.Queue(10)
        
        """Create Threads"""
        self.is_filling_queue = False
        self.deamon_task_queue = threading.Thread(target=self.fill_queue)
        
        self.fuzzer_worker = []
        self.worker_num = threads
        self.__init_workers()
        
    def __init_workers(self):
        if self.fuzzer_worker == []:
            for index in range(self.worker_num):
                """TBD"""
                pass
                
    def start(self):
        self.deamon_task_queue.start()
    
    def fill_queue(self):
        if self.is_filling_queue == False:
            self.is_filling_queue = True
        
        while self.is_filling_queue == True:
            pass
        
        
        
    