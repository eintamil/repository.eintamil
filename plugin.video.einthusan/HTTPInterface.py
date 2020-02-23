import os
import urllib.request
import urllib.parse
import urllib.error

import requests

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.74 Safari/537.36'}

def http_get(url, headers=None, cook=None):
    try:
        r = requests.get(url, headers=headers, cookies=cook).content
        return r
    except urllib.error.URLError as e:
        return ''

def http_post(url, cookie_file='', postData={}, data=''):
    try:
        if (data != ''):
            postData = dict(urllib.parse.parse_qsl(data))
        net = Net(cookie_file=cookie_file)
        return net.http_POST(url,postData).content
    except urllib.error.URLError as e:
        return ''
