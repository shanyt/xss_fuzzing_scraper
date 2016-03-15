#encoding:utf-8
import sys
from req import Req
import requests
import time
#import bs4
import re

class Stinger():
    def __init__(self, Req, re_partten = '[^<^>]*zzz.*zzuf.*zzz[^<^>]*'):
        self.req = Req
        self.method = Req.method
        self.url = Req.url
        self.cookies = Req.cookies
        self.headers = Req.headers
        self.post_data = Req.post_data
        
        self.response = None
        
        self.re = re_partten
        self.output_points = []
        
    def detect(self):
        if self.get_web_data(): 
            ret = self.analyze()
            self.output_points = self.output_points + ret
            return self.output_points
                
        
    def get_web_data(self):
        count = 0
        while True:
            try:
                self.response = requests.request(method = self.method, url = self.url, cookies = self.cookies,
                                                headers = self.headers, data = self.post_data,
                                                timeout = 10)
            except requests.exceptions.ReadTimeout:
                count = count + 1
                if count == 5:
                    raise StandardError('[!] Error ! cant request web')
                else:
                    print '[~] Trying a again！'
                    time.sleep(count)
                    
        del count
        
        
    def analyze(self):
        if self.response == None:
            raise StandardError('[!] No Rresponse')
        
        content = self.response.text
        in_tag = re.findall(pattern = self.re, string = content)
        
        if in_tag == []:
            print '[!] No Find Any tag matched!'
            return False
        else:
            return in_tag
        

class InTagDetective(object):
    def __init__(self, string = '', stylet = '', pattern = ''):
        self.target_str = stylet
        self.stylet = stylet
        self.pattern = pattern