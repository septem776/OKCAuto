#!/usr/bin/python
#coding=utf8

import urllib.request, json
import configparser
import time
import hashlib
from okc import *

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


if __name__ == '__main__':
    try:
        okcoin = OKC()
        orders = okcoin.getOrder_ltc()
        for ord in orders:
            okcoin.cancelOrder_ltc(ord['orders_id'])
            time.sleep(2)
        #okcoin.trade_ltc('buy', 1, 0.23)
        # for i in range(1):
        #     GetTicker(httpClient)
        #     time.sleep(0.5)
    except Exception as e:
        print(e)
    finally:
        pass
