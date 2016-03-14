#encoding:utf-8
import sys
from req import Req
import requests
import time
import bs4

class Stinger():
    def __init__(self, Req):
        self.req = Req
        self.method = Req.method
        self.url = Req.url
        self.cookies = Req.cookies
        self.headers = Req.headers
        self.post_data = Req.post_data
        
        self.response = None
        self.soup = None
        
    def detect(self):
        if self.get_web_data(): 
            self.analyze()
        
    def get_web_data(self):
        count = 0
        while True:
            try:
                req = requests.request(method = self.method, url = self.url, cookies = self.cookies,
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
        
        try:
            self.soup = bs4.BeautifulSoup(req.text)
        except:
            pass
        
        if self.soup == None:
            raise StandardError("[!] Empty soup!");
        
        return True