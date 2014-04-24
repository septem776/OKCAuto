#!/usr/bin/python
#coding=utf8

import urllib.request, json
import configparser
import time
import hashlib
from okc import *

if __name__ == '__main__':
    try:
        okcoin = OKC()
        t = getBTCTrades()
        print(len(t))
        print(t)
        #okcoin.trade_ltc('buy', 1, 0.23)
        # for i in range(1):
        #     GetTicker(httpClient)
        #     time.sleep(0.5)
    except Exception as e:
        print(e)
    finally:
        pass
