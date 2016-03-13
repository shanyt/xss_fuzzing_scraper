#encoding:utf-8
import urlparse
import urllib

stin_ = "zzz|xssfuzztest<>'\":\\}{&@;/|zzz"

class FUZZ_HeadersTemplate:
    """This class is to create HeadersTemplate fuzzing template"""
    def __init__(self, headers = {}, mark = "{{zzuf}}"):
        if not isinstance(headers, dict):
            raise TypeError("Need a dict , but get a %s" % type(headers))
        
        self.headers = headers
        self.headers_templates = []
        self.raw_headers_template = []
        
        self.mark = mark
        self._flg_finished = False
        
        
        
    def __analyze_headers(self):
        if self._flg_finished == True:
            self._flg_finished = False
        
        if self.headers == {}:
            raise StandardError('Empty Headers <-- FUZZ_HeadersTemplate')
        
        else:
            ret = self.headers.copy()
            for key in ret:
                ret[key] = self.mark
                self.headers_templates.append(ret)
                ret = self.headers.copy()
                
            
            if self._flg_finished == False:
                self._flg_finished = True
            return 1
        
    def get_headers_fuzz_template(self):
        while self._flg_finished == False:
            flg = self.__analyze_headers()
            if flg == 1:
                break
            else:
                pass
            
        return self.headers_templates
    
    def convert_to_raw(self):
        """
        Convert headers form dict to raw string
        you can use it by socket
        """
        if self.headers_templates == []:
            self.__analyze_headers()
        
        if self.headers_templates == []:
            return []
        
        ret = ""
        for i in self.headers_templates:
            for ii in i.items():
                tmp = ii[0] + ':' + ii[1] + '\r\n'
                ret = ret + tmp
            self.raw_headers_template.append(ret)
            ret = ''
            
        return self.raw_headers_template
            
        
class URLTemplate:
    """This class is to create a urltest template"""
    def __init__(self, url = "", mark = "{{zzuf}}"):
        """Input a url with the form 'https?://xx.xx/xx/x/x/x?ss=1&x=x#fragment'"""
        self.url = url
        self.scheme = ""
        self.netloc = ""
        self.path = ""
        self.query = ""
        self.fragment = ""
        flag = self.__init_url()
        self._flg_init_finished = False
        if flag != 1:
            raise StandardError("Fail to parse url")
        else:
            self._flg_init_finished = True
        
        self.marked_path = []
        self.marked_fragment = []
        self.marked_query = []
        self.marked_url = []
        
        self.fuzz_mark = mark
        
    def __init_url(self):
        """urlparser to parse url"""
        if self.url == "":
            return 0
        else:
            url_item = urlparse.urlparse(self.url)
            if url_item.scheme != "":
                self.scheme = url_item.scheme
            
            if url_item.netloc != "":
                self.netloc = url_item.netloc
                
            if url_item.path != "":
                self.path = url_item.path
                
            if url_item.query != "":
                self.query = url_item.query
                
            if url_item.query != "":
                self.fragment = url_item.fragment
            
            return 1
        
        
    """
    __mark_xxx method can mark the param(you want to fuzz)
    """
    
    def __mark_path(self):
        """mark path fuzz part"""
        path_list = self.path.split('/')[1:]
        for i in range(len(path_list)):
            ret = path_list[i]
            path_list[i] = self.fuzz_mark
            self.marked_path.append(self.__joint_path(path_list=path_list))
            path_list[i] = ret
            
        return self.marked_path
        
    def __joint_path(self, path_list = []):
        """Joint path_list to create a path"""
        path_str = ""
        for i in range(len(path_list)):            
            path_str = path_str + '/' + path_list[i]
        return path_str
    
    def __mark_query(self):
        """Mark kv-value"""
        pairs = self.query.split('&')
        for i in range(len(pairs)):
            k_v_list = pairs[i].split('=')
            ret = pairs[i]
            if k_v_list ==[]:
                return
            k_v_list[1] = self.fuzz_mark
            pairs[i] = k_v_list[0] + '=' + k_v_list[1]
            self.marked_query.append(self.__joint_query(pairs=pairs))
            pairs[i] = ret
            
        return self.marked_query
            
        
    def __joint_query(self, pairs=[]):
        query_str = ""
        for i in range(len(pairs)):
            if i == 0:
                query_str = pairs[i]
            else:
                query_str = query_str + '&' + pairs[i]
        return query_str
    
    def __mark_fragment(self):
        self.marked_fragment.append(self.fuzz_mark)
    
    def __stick_urls(self):
        if self.url != '':
            base = self.scheme + '://' + self.netloc
            for path in self.marked_path:
                url = base + path + '?' + self.query + "#" + self.fragment
                self.marked_url.append(url)
            
            for query in self.marked_query:
                url = base + self.path + '?' + query + '#' + self.fragment
                self.marked_url.append(url)
                
            for fragment in self.marked_fragment:
                url = base + self.path + '?' + self.query + '#' + fragment
                self.marked_url.append(url)
                
                        
        else:
            raise StandardError('Empty target url!!!')
    
        return self.marked_url
    def get_url_fuzz_template(self):
        
        if self._flg_init_finished != True:
            return []
        else:
            self.__mark_fragment()
            self.__mark_path()
            self.__mark_query()
            return self.__stick_urls()
        
def main():
    headers_template = FUZZ_HeadersTemplate(headers={'k1':'v1',
                                                     'k2':"v2",
                                                     "k3":"v3",
                                                     'k4':'v5',})
    for i in headers_template.get_headers_fuzz_template():
        print i.items()

    print "------------------------------------------------"

    for i in headers_template.convert_to_raw():
        print i
        
if __name__ == "__main__":

    tmp_builder = URLTemplate('http://sss.ss/path/id/has.html?ss=1&s=2&sss=3#ssssasdfa')
    print tmp_builder.query
    for i in tmp_builder.get_url_fuzz_template():
        print i

    main()