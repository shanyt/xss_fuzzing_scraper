#encoding:utf-8
import threadpool
import requests
import bs4
"""
Howto use threadpool
1. create 
2. put
"""
class WorkerBase:
    pass

class SocketWorker(WorkerBase):
    def __init__(self, url, headers = {}):
        pass

class RequestsWorker(WorkerBase):
    def __init__(self, url, headers = {}):
        self.url = url
        self.headers = headers
        self.soup = None
        self.response = None
    
    def handle_request(self):
        try:
            return requests.get(url = self.url, headers = self.headers, params=None)
        except:
            raise ValueError("[!] Error ! Bad response")
        
    def handle_response(self):
        self.response = self.handle_request()
        if not isinstance(self.response, requests.Response):
            raise TypeError("[!] Error ! response is not a requests.Response")
        if self.response.status_code.__str__().startswith('2'):
            self.soup = bs4.BeautifulSoup(self.response.text)
        else:
            pass
        
        all_tags = self.soup.findAll(attrs = {'':''})
        
        
        
    
    def execute(self):
        pass


class Fuzzer(object):
    def __init__(self, urls = [], headers = [] , num_workers = 5):
        self.pool = threadpool.ThreadPool(num_workers)
        self.target_urls = urls
        self.target_headers = headers
        
    def start():
        pass
    
    
        
        
    
        
    