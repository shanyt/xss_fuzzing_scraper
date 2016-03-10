#encoding:utf-8
from url_template import FUZZ_URLTemplate

class AttackRender:
    """create many """
    def __init__(self, xss_fuzz_db = ""):
        self.xss_fuzz_db = xss_fuzz_db

class StyletRender:
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
        
        
def main():
    test_data = ["asdfasdfdsf{{zzuf}}sdfad",
                 "sssssss{{zzuf}}sdadfa"]
    render = StyletRender()
    for i in render.get_stylet_payload(test_data):
        print i

if __name__ == "__main__":
    main()
