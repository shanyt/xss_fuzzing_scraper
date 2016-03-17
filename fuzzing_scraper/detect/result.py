#encoding:utf-8

"""
result fields:

is_in_tag
is_in_text
"""

class Result:
    def __init__(self, request = None, is_in_tag = False, is_in_text = False):
        
        self.is_in_tag = is_in_tag
        self.is_in_text = is_in_text