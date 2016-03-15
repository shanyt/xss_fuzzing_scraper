"""
import requests
try:
    response = requests.request(method = 'get', url = 'http://freebuf.com', timeout = 10)
except requests.exceptions.ReadTimeout:
    print 'Time out £¡'
print response.text.encode('gbk', 'ignore')
"""
import bs4
import re

ret = '<body><p><img src = "zzz ^*(<>: zzuf _+ zzz"></p> </body>\n\n<body><p><img src = "zzz ^*(<>: zzuf _+ zzz"></p> </body>\n\n'
contents = re.findall('[^<^>]*zzz.*zzuf.*zzz[^<^>]', ret)
print contents

