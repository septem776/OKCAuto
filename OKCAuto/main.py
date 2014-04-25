#!/usr/bin/python
#coding=utf8

import urllib.request, json
import configparser
import time
import hashlib
from okc import *

g_lasttid = 0
g_totalvol = 0.0
g_maxprice = 0.0
g_minprice = 999999.999999

def getLTCPrice():
    global g_lasttid, g_totalvol, g_maxprice, g_minprice
    orders = getLTCTrades()
    lownum = 0
    highnum = 0
    actualnum = 0
    for ord in orders:
        if g_lasttid < ord['tid']:
            actualnum += 1
            g_lasttid = int(ord['tid'])
            g_totalvol += float(ord['amount'])
            if g_minprice > float(ord['price']) :
                g_minprice = float(ord['price'])
                lownum += 1
            if g_maxprice < float(ord['price']) :
                g_maxprice = float(ord['price'])
                highnum += 1

    return highnum - lownum, actualnum


if __name__ == '__main__':
    try:
        okcoin = OKC()
        total = 0.0
        num = 0
        while True:
            ticker = getLTCTicker()
            last = float(ticker['ticker']['last'])
            if last == 0.0:
                continue
            trend, actnum = getLTCPrice()
            print("trend=%d, actnum=%d" % (trend, actnum))

            time.sleep(5)
    except Exception as e:
        print(e)
    finally:
        pass
