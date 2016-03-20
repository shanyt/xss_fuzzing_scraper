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
        return {'html_16':html_entity_encode_16(c),
                'html_10':html_entity_encode_10(c),
                'js_10':js_encode_10(c),
                'js_16':js_encode_16(c),
                'url_16':url_encode(c),
                'html_entity':html_entities[c]} 
    else:
        return {'html_16':html_entity_encode_16(c),
                'html_10':html_entity_encode_10(c),
                'js_10':js_encode_10(c),
                'js_16':js_encode_16(c),
                'url_16':url_encode(c)  
                }      

re_html_code_10 = r'\&\#[\d]{2,3};?'
re_html_code_16 = r'\&\#x[1234567890ABCDEFabcdef]{2,4};?'
re_html_entity = r'\&\#[a-zA-Z]{2,10};'

re_js_code_16 = r'\\x[1234567890ABCDEFabcdef]{2}'
re_js_code_10 = r'\\[\d]{3}'
re_js_unicode = r'\\u[1234567890ABCDEFabcdef]{2}'


def pck_html_char(target):
    if not isinstance(target, str):
        raise TypeError('[!] Need a str, but get a %s' % type(target))
    char_list = []
    
    if len(target) <= 1:
        return ''
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
        return ''
    else:
        char_list = char_list + re.findall(pattern = re_js_code_10 , string = target)   
        char_list = char_list + re.findall(pattern = re_js_code_16 , string = target)
        char_list = char_list + re.findall(pattern = re_js_unicode , string = target)
        
    return char_list    
        
        
        

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
        after_escape = re.findall("zzz.*zzuf", target_str)[0][3:-4]
        before_escape = re.findall('zzz.*zzuf', stylet)[0][3:-4]
        
        code_before = re.findall('zzuf.*zzz', stylet)[0][4:-3]
        code_after = re.findall('zzuf.*zzz', target_str)[0][4:-3]

        if len(after_escape) <= len(before_escape):
            for index in range(len(before_escape)):
                c = before_escape[index]
                """TODO!!!"""
            
          
            
            
                    
        
        