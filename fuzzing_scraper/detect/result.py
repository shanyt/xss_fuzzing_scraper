#encoding:utf-8

"""
result fields:

is_in_tag
is_in_text
"""

class Result(object):
    def __init__(self, request = None, is_in_tag = False, is_in_text = False):
        self.can_parser = False
        self.output = ''