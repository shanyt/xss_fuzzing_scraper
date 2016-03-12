import threadpool 
import time,random 
import threading
"""
class test:
    n = 1
    print_lock = threading.Lock()
    lock = threading.Lock()    
    @classmethod
    def hello(cls, str): 
        cls.n
        cls.lock.acquire()
        cls.n = cls.n + 1
        cls.lock.release()
        time.sleep(2) 
        cls.print_lock.acquire()
        print "Hello " , cls.n
        cls.print_lock.release()
        #return str 


def print_result(request, result): 
    pass
    #print "the result is %s %r" % (request.requestID, result) 

data = [random.randint(1,10) for i in range(20)] 

pool = threadpool.ThreadPool(10) 
requests = threadpool.makeRequests(test.hello, data, print_result) 
[pool.putRequest(req) for req in requests] 
pool.wait() 
"""

import requests
url = 'http://freebuf.com/'
responses = requests.get(url, headers = {'User-Agent' : "sssss"})
print responses.status_code.__str__().startswith('2')