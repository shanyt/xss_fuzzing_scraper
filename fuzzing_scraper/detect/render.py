#encoding:utf-8
from url_template import FUZZ_URLTemplate

class Render:
    def __init__(self, stylet = "webfuzz",mark = "{{zzuf}}"):
        self.stylet = stylet
        self.mark = mark
    
    
    
    """Public method for Every Render"""
    def render(self, data, stylet, mark):
        """render (replace)"""
        if not isinstance(data, str):
            raise TypeError("Need a str type, but get a %s" % type(data))
        
        try:
            return data.replace(mark,stylet)
        except:
            raise StandardError("Error to render data")

    def dict_render(self, data = {}, stylet = "webfuzz", mark = "{{zzuf}}"):
        if not isinstance(data, dict):
            raise TypeError("Need a dict , but get a %s" % type(data))
        
        ret = data.copy()
        for subitem in ret.items():
            if mark in ret[subitem[1]]:
                ret[subitem[1]].replace(mark,stylet)
        
        return ret
    
    def get_stylet_payload(self,data):
        """Input a list or str, get a list or str with stylet payload"""
        if isinstance(data, list) == True:
            ret = []
            for sub_data in data:
                if isinstance(sub_data, str):
                    ret.append(self.render(sub_data, self.stylet, self.mark))
                elif isinstance(sub_data, dict):
                    ret.append(self.dict_render(sub_data))
            return ret
        elif isinstance(data, str)  == True:    
            return self.render(data, self.stylet, self.mark)
        
        else:
            raise TypeError("Need a str or list , but get a %s" % type(data))    
            
            

class StyletURLRender(Render):
    pass



class StyletHeadersRender(Render):
    pass
    """
    def __init__(self, stylet = "webfuzz", mark = "{{zzuf}}"):
        
        if not isinstance(headers, dict):
            raise TypeError("Need a dict , but get a %s" % type(headers))
        self.headers = headers
        self.stylet = stylet
        self.mark = mark
    """
        
class StyletPostDataRender(Render):
    pass
        
class StyletCookieRender(Render):
    pass
        
def main():
    url_list = FUZZ_URLTemplate(url="http://helloqiu.com/s/s/s/s/s/s/sssss/s/s/s/s/sss/index.html?hhh=3&ssda=3#fraggg")
    render = StyletURLRender()
    for i in render.get_stylet_payload(url_list.get_url_fuzz_template()):
        print i

if __name__ == "__main__":
    main()
