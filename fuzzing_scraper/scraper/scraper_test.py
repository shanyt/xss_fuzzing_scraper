#encoding:utf-8
from scraper import *
import Queue
import time
import sys
import bs4

test_obj = Scraper(single_page=False, workers_num=15)
test_obj.feed(['http://freebuf.com'])
time.sleep(5)
z = test_obj.get_result_urls_queue()

while True:
    try :
        print z.get(timeout=4)
    except:
        pass
    