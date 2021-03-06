#encoding:utf-8
import re
import Queue
import threading
no_w_chars = r'!%#<>\\``\'"@$^&*()_-=+[]{}|;:,./?~'
all_tags = set(['!--', '!DOCTYPE', 
                'a', 'abbr', 'acronym', 'address', 'applet','area' , 
                'b', 'base', 'basefont', 'bdo', 'big', 'blockquote', 'body', 'br', 'button'
                'caption', 'center', 'cite' , 'code', 'col' , 'colgroup', 
                'dd', 'del', 'dfn', 'dir', 'div', 'dl', 'dt'
                'em',
                'fieldset', 'font', 'form', 'frame', 'frameset' , 
                'head', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'html'
                'i', 'iframe', 'img', 'input', 'ins'
                'kbd', 
                'label', 'legend', 
                'li', 'link',
                'map', 'menu', 'meta',
                'noscript', 
                'object', 'ol', 'optgroup', 'option',
                'p', 'param', 'pre', 
                'q',
                's', 'samp', 'script', 'select', 'small', 'span', 'strike', 'strong', 'style', 'sub', 'sup', 'table', 
                'tbody', 'td', 'textarea', 'tfoot', 'th', 'thead', 'title', 'tr', 'tt', 'u', 'ul' , 'var'
                ])

html_entities = {'<' : '&lt;',
                 '>' : '&gt;',
                 ' ' : '&nbsp;',
                 '&' : '&amp;',
                 '\'': '&apos;',
                 '"' : '&quot;'
                 }

hex_num = set(['1', 
               '2',
               '3',
               '4',
               '5',
               '6',
               '7',
               '8',
               '9',
               '0',
               'A', 'a',
               'B', 'b',
               'C', 'c',
               'D', 'd',
               'E', 'e',
               'F', 'f'])

dec_num = set(['1','2','3','4','5','6','7','8','9','0'])
ordinary_char = '1234567890_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
def html_entity_encode_10(c):
    ret = ord(c).__str__()
    return '&#' + ret + ';'

def html_entity_encode_16(c):
    ret = hex(ord(c))[1:]
    return '&#x' + ret + ';'

def js_encode_10(c):
    ret = ord(c).__str__()
    return '\\0' + ret

def js_encode_16(c):
    ret = hex(ord(c))[1:]
    return '\\' + ret

def url_encode(c):
    ret = ord(c).__str__()
    return '%' + ret

def get_encode_set(c):
    if c in html_entities.keys():
        return [html_entity_encode_16(c),
                html_entity_encode_10(c),
                js_encode_10(c),
                js_encode_16(c),
                url_encode(c),
                html_entities[c]]
    else:
        return [html_entity_encode_16(c),
                html_entity_encode_10(c),
                js_encode_10(c),
                js_encode_16(c),
                url_encode(c)  
                ]      


re_html_code_10 = r'\&\#[\d]{2,3};?'
re_html_code_16 = r'\&\#x[1234567890ABCDEFabcdef]{2,4};?'
re_html_entity = r'\&\#[a-zA-Z]{2,10};'

re_js_code_16 = r'\\x[1234567890ABCDEFabcdef]{2}'
re_js_code_10 = r'\\[\d]{3}'
re_js_unicode = r'\\u[1234567890ABCDEFabcdef]{4}'

re_url_code = r'\%[1234567890ABCDEFabcdef]{2}'

def pck_url_char(target):
    if not isinstance(target, str):
        raise TypeError('[!] Need a str, but get a %s' % type(target))
    char_list = []
    if len(target) <= 1:
        pass
    else:
        char_list = char_list + re.findall(pattern = re_url_code, string = target)
    
    return char_list
    
def pck_html_char(target):
    if not isinstance(target, str):
        raise TypeError('[!] Need a str, but get a %s' % type(target))
    char_list = []
    
    if len(target) <= 1:
        return []
    else:
        char_list = char_list + re.findall(pattern = re_html_code_10 , string = target)   
        char_list = char_list + re.findall(pattern = re_html_code_16 , string = target)
        char_list = char_list + re.findall(pattern = re_html_entity  , string = target)
        
    return char_list

def pck_js_char(target):
    if not isinstance(target, str):
        raise TypeError('[!] Need a str, but get a %s' % type(target))
    
    char_list = []
    
    if len(target) <= 1:
        return []
    else:
        char_list = char_list + re.findall(pattern = re_js_code_10 , string = target)   
        char_list = char_list + re.findall(pattern = re_js_code_16 , string = target)
        char_list = char_list + re.findall(pattern = re_js_unicode , string = target)
        
    return char_list    
        
        
        


def pck_chars(target):
    char_list = pck_js_char(target) + pck_html_char(target) + pck_url_char(
                                                                          target)
    return char_list

class Analyzer():
    """This class is for analyzing output from stinger"""
    def __init__(self, stylet = '', pattern = ''):
                
        self.stylet = stylet
        self.pattern = pattern
        self.job_queue = Queue.Queue()
        self.result = {}
        
        self.is_killed = False
        
        try:
            self.ret_thread = threading.Thread(target=self.__analyze)
            self.ret_thread.start()
        except:
            print '[!] Fail to start analyzer thread!!!'
        
        self.stylet_payload = re.findall(pattern=pattern,string=stylet)[0]
        
    """Parse the tag name"""
    def __find_tag_name(self, target_str):
        target_name = ''
        for c in target_str:
            if c != ' ' and c != '>':
                target_name = target_name + c
            else:
                break
        
        if target_name not in all_tags:
            self.result['tag_name'] = 'Unknow target : ' + target_name
            return False
        else:
            self.result['tag_name'] = target_name
            return True
            
    

    """These following method is testing 
    Perhaps I 'll delete them        
    def __find_filted_char(self, stylet = '', target_str = ''):
        after_escape = re.findall("zzz.*zzuf", target_str)[0][3:-4]
        before_escape = re.findall('zzz.*zzuf', stylet)[0][3:-4]

        for i in before_escape:
            flg_encoded = False
            alive_sym = False
            if i in after_escape:
                if flg_encoded != False:
                    flg_encoded = False
                if alive_sym != True:
                    alive_sym = True  
                    
            for z in get_encode_set(i):
                if z in after_escape:
                    self.result[i] = i + '-->' + z
                else:
                    pass
                
            if alive_sym:
                if self.result.has_key('alive') == False:
                    self.result['alive'] = []
                else:
                    self.result['alive'].append(i)
    def __find_encoded_char(self, stylet = '', target_str = ''):
        after_escape = re.findall('zzuf.*zzz', target_str)[0][4:-3]
        before_escape = re.findall('zzuf.*zzz', stylet)[0][4:-3]
        
        chars_set = set(pck_chars(before_escape))
        if chars_set != set([]):
            for char in chars_set:
                if char not in after_escape:
                    pass
                else:
                    if self.result.has_key('alive') == False:
                        self.result['alive'] = []
                    
                    self.result['alive'].append(char)
                        
        else:
            return 
    


    """
    """Parse & scan target_str into List to 
    identify any useful comparable info"""
    def __parse_str_to_list(self, target = ''):
        """
        if you want to parse text, you should know 
        what type of the encoding char,
        url encode 
            %[num]
        js encode 
            \[num] 
            \u[num] 
            \ x[num]
        html encode 
            &#[num]; 
            &#x[num]
            &#[name];
        """
        special_char = set(['%', '\\', '&'])
        char_buffer = ''
        rest_buffer = ''
        
        target_list = []
        
        skip_target = 0
        index = -1
        while len(target) > index:
            index = index + 1
            if index == len(target):
                break
            i = target[index]
            
            while i < skip_target:
                continue
            """check if a encoded exist"""
            if i in special_char:
                if i == '%':
                    rest_buffer = target[index+1:]
                    ret = self.__scan_hex_num(rest_buffer)
                    if ret == '':
                        del ret
                        target_list.append('%')
                    else:
                        target_list.append('%'+ret)
                        index = index + len(ret)
                        
                elif i == '\\':
                    prifix = ['x', 'u']
                    if target[index+1] in prifix:
                        if target[index+1] == 'x':
                            rest_buffer = target[index+2:]
                            ret = self.__scan_hex_num(rest_buffer)
                            if ret == '':
                                del ret
                                target_list.append('\\')
                                target_list.append('x')
                                index = index + 1
                            else:
                                target_list.append('\\x'+ret)
                                index = index + len(ret) + 1
                        elif target[index+1] == 'u':
                            rest_buffer = target[index+2:]
                            ret = self.__scan_num(rest_buffer)
                            if ret == '':
                                del ret
                                target_list.append('\\')
                                target_list.append('u')
                                index = index + 1
                                
                            else:
                                target_list.append('\\u'+ret)
                                index = index + len(ret) + 1
                    else:
                        rest_buffer = target[index+1:]
                        ret = self.__scan_dec_num(rest_buffer)
                        if ret == '':
                            target_list.append('\\')
                            del ret
                            
                        else:
                                target_list.append('\\'+ret)
                                index = index + len(ret)
                            
                    
                elif i == '&':
                    if target[index+1] == '#':
                        if target[index+2] == 'x':
                            rest_buffer = target[index+3:]
                            ret = self.__scan_hex_num(rest_buffer)
                            if ret == '':
                                target_list.append('&')
                                target_list.append('#')
                                target_list.append('x')
                                index = index + 2
                                
                            else:
                                target_list.append('&#x'+ret)
                                index = index + len(ret) + 2
                        else:
                            rest_buffer = target[index+2:]
                            ret = self.__scan_dec_num(rest_buffer)
                            if ret == '':
                                target_list.append('&')
                                target_list.append('#')
                                index = index + 1
                            else:
                                target_list.append('&#'+ret)
                                index = index + len(ret) + 1
                        if target[index+1] == ';':
                            index = index + 1
                            
                                           
                    else:
                        ret = self.__scan_identifier(target[index+1:])
                        if ret == '':
                            target_list.append('&')                           
                        else:
                            if target[index+len(ret)+1] == ';':
                                target_list.append('&'+ret+';')
                                index = index + len(ret) + 1
                            else:

                                pass
                else:
                    
                    pass
            elif i in no_w_chars and i not in special_char:
                target_list.append(i)
            else:
                pass

        return target_list
    
    def __scan_num(self, target):
        """scan the target str
        if the str starts with a num(hex or dec)"""
        num_buffer = ''
        for i in target:
            if i in hex_num:
                num_buffer = num_buffer+i
            else:
                break
        
        if len(num_buffer) >= 2:
            return num_buffer
        else:
            return ''
        
    def __scan_hex_num(self, target = ''):
        """By using __scan_num , 
        you can get a hex num here"""
        ret = self.__scan_num(target)
        
        if ret == '':
            return ''
        
        out_dec = 'abcdefABCDEF'
        for char in ret:
            if char in out_dec:
                return ret
            else:
                pass
        return ''
    
    
    def __scan_dec_num(self, target = ''):
        """By using __scan_num ,
        you can get a dec num here"""
        ret = self.__scan_num(target)
        
        if ret == '':
            return ''
        else:
            out_dec = 'abcdefABCDEF'
            for char in out_dec:
                if char in ret:
                    return ''
                else:
                    pass
            return ret            
        
    def __scan_identifier(self, target = ''):
        ret_buffer = ''
        for i in target:
            if i in ordinary_char:
                ret_buffer = ret_buffer + i
            else:
                break
        if len(ret_buffer) >= 2:
            return ret_buffer
        else:
            del ret_buffer
            return ''
            


    

    def   __compare(self):
        pass
    """
    Data input here!
    """
    def feed(self, targets):
        if isinstance(targets, list):
            for i in list:
                if isinstance(i, str):
                    self.job_queue.put(re.findall(pattern=self.pattern, string=i)[0])
                else:
                    pass
                
        elif isinstance(targets, str):
            
            self.job_queue.put(self.job_queue.put(re.findall(pattern=self.pattern, string=targets)[0]))
        else:
            raise TypeError("[!] Need a list or str, but get a %s" % type(
                                                                         targets))
    
    """main process for analysis"""
    def __analyze(self):
        while self.is_killed == False:
            pass
        
    def test_parse_list(self, target = ''):
        return self.__parse_str_to_list(target)
        
        
def test():
    analyzer = Analyzer()
    print analyzer.test_parse_list(target=r'#$%^&*^#%&&^&#234;\xb1\223&lt;\u123354')

        
if __name__ == '__main__':
    test()
          
            
            
                    
        

        