#encoding:utf-8
import re

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

def html_entity_encode(c):
    ret = ord(c).__str__()
    return '&#' + ret

def js_encode_10(c):
    ret = ord(c).__str__()
    return '\\0' + ret

def js_encode_16(c):
    ret = hex(ord(c))[1:]
    return '\\' + ret

def is_hex_digit(c):
    if not isinstance(c, str):
        return False
    else:
        if len(c) == 1:
    

class Analyzer():
    def __init__(self, in_tag_str_list = [], stylet = '', pattern = ''):
        
        self.target_output = []
        for tag in in_tag_str_list:
            if isinstance(tag, str):
                self.target_output.append(tag)
                
        self.stylet = stylet
        self.pattern = pattern
        
        self.result = {}
        
    def __find_tag_name(self, target_str):
        target_name = ''
        for c in target_str:
            if c != " " or c != '>':
                target_name = target_name + i
            else:
                break
        
        if target_name not in all_tags:
            self.result['tag_name'] = 'Unknow target : ' + target_name
        else:
            self.result['tag_name'] = target_name
            
        return target_name
    
    def __find_filted_char(self, stylet = '', target_str = ''):
        after_escape = re.findall("zzz.*zzufzzz", target_str)[0][3:-7]
        before_escape = re.findall('zzz.*zzufzzz', stylet)[0][3:-7]

        for index in range(len(before_escape)):
            c = before_escape[index]
            
            if before_escape[index] == '%':
                if before_escape[index + 1].isdigit() == False:
                    pass
                elif ord(before_escape[index + 1]) < ord('A') or ord(before_escape[index + 1] > ord(
                                                                                                   'F')):
                    pass
                elif ord(before_escape[index + ])
                    
                    if before_escape[index + 2].isdigit():
                        c = before_escape[index:index+2][-2:]
            
            
                    
        
        
        
        