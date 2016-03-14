import requests
try:
    response = requests.request(method = 'get', url = 'http://freebuf.com', timeout = 10)
except requests.exceptions.ReadTimeout:
    print 'Time out £¡'
print response.text.encode('gbk', 'ignore')

import bs4

soup = bs4.BeautifulSoup(response.text)
all_tag = soup.findAll(data=re.)
for i in all_tag:
    print i