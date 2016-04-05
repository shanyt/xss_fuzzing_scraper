#encoding:utf-8
import re
import Queue
import threading

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
    Perhaps I 'll delete them"""        
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
            """TBD"""
            for char in chars_set:
                if char not in after_escape:
                    pass
                else:
                    if self.result.has_key('alive') == False:
                        self.result['alive'] = []
                    
                    self.result['alive'].append(char)
                        
        else:
            return 
    


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
            \x[num]
        html encode 
            &#[num]; 
            &#x[num]
            &#[name];
        """
        special_char = set(['%', '\\', '&'])
        char_buffer = ''
        rest_buffer = ''
        
        target_list = []
        
        for index in range(len(target)):
            i = target[index]
            
            """check if a encoded exist"""
            if i in special_char:
                if i == '%':
                    rest_buffer = target[index+1:]
                    ret = self.__scan_hex_num(rest_buffer)
                    if ret == '':
                        del ret
                        pass
                    else:
                        target_list.append('%'+ret)
                        index = index + len(ret)
                        
                elif i == '\\':
                    prifix = ['x', 'u']
                    if target[index+1] in x:
                        if target[index+1] == 'x':
                            rest_buffer = target[index+2:]
                            ret = self.__scan_hex_num(rest_buffer)
                            if ret == '':
                                del ret
                                pass
                            else:
                                target_list.append('\\x'+ret)
                                index = index + len(ret) + 2
                        elif target[index+1] == 'u':
                            rest_buffer = target[index+2:]
                            ret = self.__scan_num(rest_buffer)
                            if ret == '':
                                del ret
                                pass
                            else:
                                target_list.append('\\u'+ret)
                                index = index + len(ret) + 2
                        else:
                            rest_buffer = target[index+1:]
                            ret = self.__scan_dec_num(rest_buffer)
                            if ret == '':
                                del ret
                                pass
                            else:
                                target_list.append('\\'+ret)
                                index = index + len(ret) + 1 
                            
                    
                elif i == '&':
                    if target[index+1] == '#':
                        if target[index+2] == 'x':
                            rest_buffer = target[index+3:]
                            ret = self.__scan_hex_num(rest_buffer)
                            if ret == '':
                                pass
                            else:
                                target_list.append('&#x'+ret)
                                index = index + len(ret) + 3
                        else:
                            rest_buffer = target[index+2:]
                            ret = self.__scan_dec_num(rest_buffer)
                            if ret == '':
                                pass
                            else:
                                target_list.append('&#'+ret)
                                index = index + len(ret) + 2
                        if target[index] == ';':
                            continue
                                           
                    else:
                        ret = self.__scan_identifier(target[index+1:])
                        if ret == '':
                            pass
                        else:
                            if target[index+len(ret)+1] == ';':
                                target_list.append('&'+ret+';')
                                index = index + len(ret) + 1
                            else:
                                pass
                else:
                    
                    pass
        
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
        
        out_dec = ['abcdefABCDEF']
        for char in out_dec:
            if char in ret:
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
            out_dec = ['abcdefABCDEF']
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
            


    
    def feed(self, targets):
        if isinstance(targets, list):
            for i in list:
                if isinstance(i, str):
                    self.job_queue.put(i)
                else:
                    pass
                
        elif isinstance(targets, str):
            self.job_queue.put(targets)
        else:
            raise TypeError("[!] Need a list or str, but get a %s" % type(
                                                                         targets))
    
    """main process for analysis"""
    def __analyze(self):
        while self.is_killed == False:
            pass
        
    def test_for_parse_list(self):
        pass
def test():
    analyzer = Analyzer(in_tag_str_list=[r'img src=x zzz&^&lt;>$zzuf%23\u0034\\xb1\157zzz'], stylet=r'zzz&^%23$<zzuf%23\u0034\xb1\157zzz')
    analyzer.analyze()
        
if __name__ == '__main__':
    test()
          
            
            
                    
        

        