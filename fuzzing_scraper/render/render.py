#encoding:utf-8
from url_template import FUZZ_URLTemplate

class AttackRender:
    """create many """
    def __init__(self, xss_fuzz_db = ""):
        self.xss_fuzz_db = xss_fuzz_db

class URLRender:
    """create a stylet to detect vul in web"""
    def __init__(self, xss_stylet = "webfuzz",mark = "{{zzuf}}"):
        self.xss_stylet = xss_stylet
        self.mark = mark
    
    def get_stylet_payload(self,data):
        """Input a list or str, get a list or str with stylet payload"""
        if isinstance(data, list) == True:
            ret = []
            for sub_data in data:
                ret.append(self.render(sub_data, self.xss_stylet, self.mark))
                
            return ret
        elif isinstance(data, str)  == True:    
            return self.render(data, self.xss_stylet, self.mark)
        
        else:
            raise TypeError("Need a str or list , but get a %s" % type(data))
    
    
    def render(self, data, stylet, mark):
        """render (replace)"""
        if not isinstance(data, str):
            raise TypeError("Need a str type, but get a %s" % type(data))
        
        try:
            return data.replace(mark,stylet)
        except:
            raise StandardError("Error to render data")

class HeadersRender:
    def __init__(self, headers = None, stylet = "webfuzz", mark = "{{zzuf}}"):
        self._flg_headers_is_dict = False
        self._flg_headers_is_str  = False
        
        if isinstance(headers, dict):
            if self._flg_headers_is_dict == False:
                self._flg_headers_is_dict = True
            else:
                pass
        if isinstance(headers, str):
            if self._flg_headers_is_str == False:
                self._flg_headers_is_str = True
            else:
                pass
        else:
            raise TypeError("Need a str or dict , but get a %s" % headers)
        
        self.stylet = stylet
        self.mark = mark
        
        if self._flg_headers_is_dict == True:
            self.dict
        elif self._flg_headers_is_str == True:
            pass
        else:
            raise TypeError("Need a str or dict , but get a %s" % headers)
        
def main():
    url_list = FUZZ_URLTemplate(url="http://helloqiu.com/s/s/s/s/s/s/sssss/s/s/s/s/sss/index.html?hhh=3&ssda=3#fraggg")
    render = URLRender()
    for i in render.get_stylet_payload(url_list.get_url_fuzz_template()):
        print i

if __name__ == "__main__":
    main()
