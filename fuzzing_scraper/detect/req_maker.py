#encoding:utf-8
import urlparse

methods = ['get', 'head', 'put', 'post', 'options', 'delete', 'trace', 'connect']
schemes = ['https', 'http', 'ftp']

class Req(object):
    def __init__(self, 
                 method = "get", 
                 url = '', 
                 cookies = '', 
                 headers = {} , 
                 stylet = '',
                 post_data = ''):
        
        if method not in methods:
            raise ValueError('Invalid Method')
        
        self.method = method
        self.url = url
        self.cookies = cookies
        self.stylet = stylet
        
        if not isinstance(headers, dict):
            raise TypeError("[!] Need a dict, but get a %s" % type(headers))
        
        self.headers = headers
        self.post_data = post_data
        
    
        


class MultiReqMaker(object):
    def __init__(self, 
                 methods = 'get',
                 urls = None, 
                 headers = None, 
                 cookies = None,
                 post_data = None,
                 stylet = ""):
        
        self.method = 'get' #default_method
        self.method_list = []
        
        self.reqs = []

        self.stylet = ""
        
        if not isinstance(stylet, str):
            raise TypeError('[!] Need a str, but get a %s' % type(stylet))
        else:
            self.stylet = stylet
        
        if isinstance(methods, str):
            if self.__check_method(methods):
                self.method = methods
        elif isinstance(method, list):
            for method in methods:
                if self.__check_method(method):
                    if method not in self.method_list:
                        self.method_list.append(method)
                        
        
        if self.method not in self.method_list:
            self.method_list.append(self.method)
            
        self.urls = None
        self.urls_list = []
        if isinstance(urls, str):
            if urls == '':
                raise ValueError("[!] url can't be empty!")
            else:
                self.urls = urls
                if urls not in self.urls_list:    
                    self.urls_list.append(self.urls)
                else:
                    pass
                
        elif isinstance(urls, list):
            for url in urls:
                if self.__check_url(url):
                    if url not in self.urls_list:
                        self.urls_list.append(url)
        
        if self.urls not in self.urls_list:
            self.urls_list.append(self.urls)
        else:
            pass
        
        self.headers = {}
        self.headers_list = []
        if isinstance(headers, dict):
            if headers not in self.headers_list:
                self.headers_list.append(headers)
            else:
                pass
        elif isinstance (headers, type(None)):
            pass
        elif isinstance (headers, list):
            for header in headers:
                if isinstance(header, dict):
                    if header not in self.headers_list:
                        self.headers_list.append(header)
                    else:
                        pass
                else:
                    pass
        if self.headers not in self.headers_list:
            self.headers_list.append(self.headers)
        else:
            pass
                
        self.cookies = ""
        self.cookies_list = []
        if isinstance(cookies, dict):
            if cookies not in self.cookies_list:
                self.cookies_list.append(cookies)
            else:
                pass
        elif isinstance (cookies, list):
            for cookie in cookies:
                if isinstance(cookie, dict):
                    if cookie not in self.cookies_list:
                        self.cookies_list.append(cookie)
                    else:
                        pass
                else:
                    pass
        if self.cookies not in self.cookies_list:
            self.cookies_list.append(self.cookies)
        else:
            pass
        
        self.post_data = ''
        self.post_data_list = []
        if isinstance(post_data, str):
            if post_data not in self.post_data_list:
                self.post_data_list.append(post_data)
            else:
                pass
        elif isinstance(post_data, list):
            for post_data_sub in post_data:
                if isinstance (post_data_sub, dict):
                    if post_data_sub not in self.post_data_list:
                        self.post_data_list.append(post_data_sub)
                    else:
                        pass
                else:
                    pass
        if self.post_data not in self.post_data_list:
            self.post_data_list.append(self.post_data)
        
    
    
    def __check_method(self,method):
        """Check_method correct"""
        if method in methods:
            return True
        else:
            return False
        
        
    def __check_url(self,url):
        obj = urlparse.urlparse(url)
        if obj.scheme not in schemes:
            return False
        else:
            return True
        
    def get_reqs(self):
        """
        Create different Requests
        return a req list
        """
        for method in self.method_list:
            for url in self.urls_list:
                for headers in self.headers_list:
                    for cookies in self.cookies_list:
                        for post_data in self.post_data_list:
                            ret = Req(method=method, 
                                      url=url, 
                                      cookies=cookies, 
                                      headers=headers, 
                                      post_data=post_data)
                            self.reqs.append(ret)
        
        return self.reqs
        
        
                            
if __name__ == '__main__':
    target_list = ['http://villanch.top/?p=zzz$^%&%^<>?zzuf&#354zzz']
    stylet = 'zzz$^%&%^<>?zzuf&#354zzz'
    
    obj = MultiReqMaker(stylet=stylet,urls=target_list)
    request_list = obj.get_reqs()
    print request_list