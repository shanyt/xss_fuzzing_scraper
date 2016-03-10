#encoding:utf-8
import socket
from url_template import FUZZ_URLTemplate
from headers_template import FUZZ_HeaderTemplate

class RawSender:
    """use socket to deal with http connection"""
    def __init__(self, url, headers)
