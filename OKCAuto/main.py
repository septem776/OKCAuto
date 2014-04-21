#!/usr/bin/env python
#coding=utf8

import urllib.request, json
import time
import hashlib


def getBTCTicker():
    response = urllib.request.urlopen('https://www.okcoin.com/api/ticker.do')
    print(response.status)
    data = response.read().decode('utf-8')
    jsondata = json.loads(data)
    return jsondata

def getBTCTickerVol():
    jdata = getBTCTicker()
    return jdata['ticker']['vol']

def getDepth(httpClient):
    pass

def readUserInfo():
    # TODO: read partner and secretKey from file
    partner = ''
    pri_key = ''
    sign = ''
    return (partner, sign)

if __name__ == '__main__':
    try:

        (partner, sign) = readUserInfo()
        data = urllib.parse.urlencode({'partner' : partner, 'sign' : sign})
        data = data.encode('utf-8')
        request = urllib.request.Request('https://www.okcoin.com/api/userinfo.do')
        request.add_header("Content-Type","application/x-www-form-urlencoded;charset=utf-8")
        f = urllib.request.urlopen(request, data)
        print(f.status)
        print(f.read())
        # for i in range(1):
        #     GetTicker(httpClient)
        #     time.sleep(0.5)
    except Exception as e:
        print(e)
    finally:
        pass
