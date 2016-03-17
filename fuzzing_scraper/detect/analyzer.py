#encoding:utf-8

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



class Analyzer():
    def __init__(self, in_tag_str_list = [], stylet = '', pattern = ''):
        
        self.target_url = []
        for tag in in_tag_str_list:
            if isinstance(tag, str):
                self.target_url.append(tag)
                
        self.stylet = stylet
        self.pattern = pattern
        
    def __find_tag_name():
        
        
        