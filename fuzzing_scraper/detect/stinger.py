#encoding:utf-8
import sys
from req_maker import Req
import requests
import time
#import bs4
import re
import threading
import Queue


result = Queue.Queue()


class Stinger():
    def __init__(self, Req_obj, re_partten = '[^<]*zzz.*zzuf.*zzz[^>]*'):
        self.req = Req_obj
        self.method = Req.method
        self.url = Req.url
        self.cookies = Req.cookies
        self.headers = Req.headers
        self.post_data = Req.post_data
        self.stylet = Req.stylet
        
        self.response = None
        
        self.re = re_partten
        self.output_points = []
        
                
        
    def __get_web_data(self):
        count = 0
        while True:
            try:
                self.response = requests.request(method = self.method,
                                                 url = self.url, 
                                                 cookies = self.cookies,
                                                 headers = self.headers, 
                                                 data = self.post_data,
                                                 timeout = 10)
            except requests.exceptions.ReadTimeout:
                count = count + 1
                if count == 5:
                    raise StandardError('[!] Error ! cant request web')
                else:
                    print '[~] Trying a again！'
                    time.sleep(count)
                    
        del count
        return self.response
        
    def get_output_points_str_list(self):
        if self.response == None:
            self.__get_web_data()
            
        if isinstance(self.response, type(None)):
            raise ValueError("[!] Error in __get_web_data() , Response empty!")
        
        
        content = self.response.text
        in_tag = re.findall(pattern = self.re, string = content)
        
        if in_tag == []:
            meta_tags = re.findall('< ?meta[^>]*>',self.response.text)
            for meta_tag in meta_tags:
                
                raw_charset = meta_tag[meta_tag.index("charset=")+len("charset="):]
                charsets = re.findall('[^\'^\"].*[^\'^\"]')
                for charset in charsets:
                    ret_in_tag = re.findall(pattern= self.re, string = content.encode(charset, 'ignore'))
                
                if ret_in_tag == []:
                    #print '[!] No Find Any tag matched!'
                    continue
                else:
                    in_tag = in_tag + ret_in_tag
            if in_tag == []:
                print '[!] No Find Any tag matched!'
                return False
            else:
                return in_tag
        else:
            return in_tag
        
        
class MultiStingerMaker():
    def __init__(self, Req_list, re_partten = '[^<]*zzz.*zzuf.*zzz[^>]*'):
        if not isinstance(Req_list, list):
            raise ValueError('[!] Need a list , but get a %s' % Req_list)

        self.stinger_list = []
        ret = None
        
    def get_stingers(self):
        for i in Req_list:
            ret = Stinger(Req_obj = i, re_partten=re_partten)
            stinger_list.append(ret)
        return self.stinger_list

class StingerPool():
    def __init__(self, stingers = [], threads_num = 8):
        if len(stingers) == 0:
            raise ValueError('[!] stingers Mustn\'t be empty')
    
        self.joblist = Queue.Queue()
        for i in stingers:
            self.joblist.put(i)
        self.threads_num = threads_num
    
    def __init_worker(self):
        for _ in range(self.threads_num):
            ret = threading.Thread(target=self.__worker)
            ret.deamon = True
            ret.start
            
    def __worker(self):
        while True:
            if self.joblist.empty():
                pass
            else:
                with self.joblist.get() as stinger:
                    output_list = stinger.get_output_points_str_list()
                    for i in output_list:
                        result.put(i)
    
    def execute(self):
        self.__init_worker()