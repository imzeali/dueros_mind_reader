# -*- coding: utf-8 -*-
# © 2018 WE Technology
# Authored by: Zhi Li (zealiemai@gmail.com)
import json
import urllib
import urllib2
import cookielib
HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept-Language": "'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:58.0) Gecko/20100101 Firefox/58.0",
    "Referer": "http://dueros.baidu.com",
    "X-Requested-With": "XMLHttpRequest",
}


def post(url, data, headers=None):
    if not headers:
        headers = HEADERS

    try:
        data = urllib.urlencode(data)
        urllib2.HTTPCookieProcessor()
        req = urllib2.Request(url, data=data, headers=headers)
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
        print response
        if response:
            response = json.loads(response)
            if response['ret'] == 200:
                return response['data']
            else:
                print response
        else:
            print response
    except Exception as e:

        print e


def get(url, headers=None):
    if not headers:
        headers = HEADERS

    try:
        req = urllib2.Request(url, headers=headers)
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
        return response
    except Exception as e:
        print e
