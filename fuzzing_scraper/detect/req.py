#encoding:utf-8
methods = ['get', 'head', 'put', 'post', 'options', 'delete', 'trace', 'connect']
class Req(object):
    def __init__(self, method = "get", url = '', cookies = '', headers = {} , post_data = ''):
        if method not in methods:
            raise ValueError('Invalid Method')
        
        self.method = method
        self.url = url
        self.cookies = cookies
        
        if not isinstance(headers, dict):
            raise TypeError("[!] Need a dict, but get a %s" % type(headers))
        
        self.headers = headers
        self.post_data = post_data