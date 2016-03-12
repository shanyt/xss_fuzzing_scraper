#encoding:utf-8


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
    main()