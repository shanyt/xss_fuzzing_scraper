import urlparse

url = "http://gihub.com/VIllanCh/scraplat.git?ss=1&sss=112#fragmentsss"

o = urlparse.urlparse(url)
print o.scheme
print o.path
print o.netloc
print o.query
print o.fragment
