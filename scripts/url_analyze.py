#encoding:utf-8
import urlparse

url = "http://bbs.csdn.net/topics/390908212"
url = 'http://192.168.1.102/xss/example1.php?name=hacker'
#url = 'http://192.168.1.102/'
o = urlparse.urlparse(url)
print o.path
path_items = o.path.split('/')[1:]

print path_items

payload_path = ""
for i in path_items:
    payload_path = payload_path + "/" + i
print payload_path