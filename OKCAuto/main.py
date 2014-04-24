#!/usr/bin/python
#coding=utf8

import urllib.request, json
import configparser
import time
import hashlib
from okc import *

def getBTCVol():
    totalval = 0.0
    orders = getBTCTrades()
    for ord in orders:
        totalval += float(ord['amount'])
    return totalval

if __name__ == '__main__':
    try:
        okcoin = OKC()
        total = 0.0
        num = 0
        while True:
            ticker = getBTCTicker()
            last = float(ticker['ticker']['last'])
            if last == 0.0:
                continue
            if okcoin.buyprice == 0.0:
                okcoin.buyprice = last
            cur_vol = getBTCVol()
            total += cur_vol
            num += 1
            avg = total / num
            rate = cur_vol / avg
            print("rate=%f, last=%f, buyprice=%f, sellprice=%f, vol=%f" % (rate, last, okcoin.buyprice, okcoin.sellprice, cur_vol))
            print("last/buyprice=%f" % (last / okcoin.buyprice))
            if rate > 1.3:
                okcoin.sellprice = last

            if okcoin.canSell and last / okcoin.buyprice > 1.005:
                okcoin.sellMarket_btc(1)
                print("sell 1 btc on market price")
                okcoin.canSell = False
                okcoin.getUserAccount()
                okcoin.sellprice = last

            if okcoin.canSell == False and last / okcoin.sellprice < 0.99:
                okcoin.buyMarket_btc(okcoin.free_cny)
                okcoin.canSell = True
                okcoin.getUserAccount()
                okcoin.buyprice = last
                print("buy btc on price %d" % last)

            if num > 900:
                num = 0
                total = 0.0

            time.sleep(1)
    except Exception as e:
        print(e)
    finally:
        pass
