#!/usr/bin/python
#coding=utf8

import configparser, hashlib, urllib

class OKC:
    def __init__(self):
        self.partner = ''
        self.sign = ''
        pass

    def readUserInfo(self):
        # read partner and secretKey from file
        cfg = configparser.RawConfigParser()
        cfg.read('userinfo.ini')
        partner = cfg.get('userinfo', 'partner')
        pri_key = cfg.get('userinfo', 'secretkey')
        sign = hashlib.md5(b'partner=' + bytes(partner, encoding = 'utf-8') + bytes(pri_key, encoding = 'utf-8')).hexdigest().upper()
        # print(bytes(partner, encoding = 'utf-8'))
        # print(pri_key)
        # print(sign)
        self.partner = partner
        self.sign = sign
        return (partner, sign)

    def getUserAccount(self, partner, sign):
        data = urllib.parse.urlencode({'partner' : partner, 'sign' : sign})
        data = data.encode('utf-8')
        request = urllib.request.Request('https://www.okcoin.com/api/userinfo.do')
        request.add_header("Content-Type","application/x-www-form-urlencoded;charset=utf-8")
        f = urllib.request.urlopen(request, data)
        print(f.status)
        return f.read()