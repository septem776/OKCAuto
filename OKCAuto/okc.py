#!/usr/bin/python
#coding=utf8

import sys
import configparser, hashlib, urllib, json

def getBTCTicker():
    response = urllib.request.urlopen('https://www.okcoin.com/api/ticker.do')
    print(response.status)
    data = response.read().decode('utf-8')
    jsondata = json.loads(data)
    return jsondata

def getLTCTicker():
    response = urllib.request.urlopen('https://www.okcoin.com/api/ticker.do?symbol=ltc_cny')
    print(response.status)
    data = response.read().decode('utf-8')
    jsondata = json.loads(data)
    return jsondata

def getBTCDepth():
    response = urllib.request.urlopen('https://www.okcoin.com/api/depth.do')
    data = response.read().decode('utf-8')
    jsondata = json.loads(data)
    return jsondata

def getLTCDepth():
    response = urllib.request.urlopen('https://www.okcoin.com/api/depth.do?symbol=ltc_cny')
    data = response.read().decode('utf-8')
    jsondata = json.loads(data)
    return jsondata

def getBTCTrades(since=0):
    url = 'https://www.okcoin.com/api/trades.do'
    if since > 0:
        url += '?since=' + str(since)
    print(url)
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8')
    jsondata = json.loads(data)
    return jsondata

def getLTCTrades(since=0):
    url = 'https://www.okcoin.com/api/trades.do?symbol=ltc_cny'
    if since > 0:
        url += '&since=' + str(since)
    print(url)
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8')
    jsondata = json.loads(data)
    return jsondata

class OKC:
    def __init__(self):
        self.partner = ''
        self.key = ''
        self.sign = ''
        self.free_ltc = 0.0
        self.free_btc = 0.0
        self.free_cny = 0.0
        self.freezed_ltc = 0.0
        self.freezed_btc = 0.0
        self.freezed_cny = 0.0
        self.total_assets = 0.0
        self.partner, self.sign = self.readUserInfo()
        self.accountinfo = self.getUserAccount(self.partner, self.sign)
        pass


    def _signature(self, params):
        s = ''
        for k in sorted(params.keys()):
            if len(s) > 0:
                s += '&'
            s += k + '=' + str(params[k])
        s += self.key
        return hashlib.md5(bytes(s, encoding='utf-8')).hexdigest().upper()


    def readUserInfo(self):
        # read partner and secretKey from file
        cfg = configparser.RawConfigParser()
        cfg.read('userinfo.ini')
        partner = cfg.get('userinfo', 'partner')
        pri_key = cfg.get('userinfo', 'secretkey')
        sign = hashlib.md5(
            b'partner=' + bytes(partner, encoding='utf-8') + bytes(pri_key, encoding='utf-8')).hexdigest().upper()
        # print(bytes(partner, encoding = 'utf-8'))
        # print(pri_key)
        # print(sign)
        self.partner = partner
        self.key = pri_key
        self.sign = sign
        return (partner, sign)


    def getUserAccount(self, partner, sign):
        data = urllib.parse.urlencode({'partner': partner, 'sign': sign})
        data = data.encode('utf-8')
        request = urllib.request.Request('https://www.okcoin.com/api/userinfo.do')
        request.add_header("Content-Type", "application/x-www-form-urlencoded;charset=utf-8")
        f = urllib.request.urlopen(request, data)
        print(f.status)
        jsondata = json.loads(f.read().decode('utf-8'))
        result = jsondata['result']
        if (result != True):
            print("ErrCode=%d" % jsondata['errorCode'])
            return None

        self.free_ltc = float(jsondata['info']['funds']['free']['ltc'])
        self.free_btc = float(jsondata['info']['funds']['free']['btc'])
        self.free_cny = float(jsondata['info']['funds']['free']['cny'])
        self.freezed_btc = float(jsondata['info']['funds']['freezed']['btc'])
        self.freezed_cny = float(jsondata['info']['funds']['freezed']['cny'])
        self.freezed_ltc = float(jsondata['info']['funds']['freezed']['ltc'])
        print(jsondata)
        return jsondata


    def trade(self, symbol, type, rate=None, amount=None):
        # type : 'buy' / 'sell' / 'buy_market' / 'sell_market'
        # rate : 0 < rate < 1000000 ;  if 'buy_market', set buy cny amount
        # amount : btc > 0.01, ltc > 0.1; if 'sell_market', set sell btc/ltc number
        param = {
            'partner': self.partner,
            'symbol': symbol,
            'type': type
        }
        if rate is not None:
            param['rate'] = rate
        if amount is not None:
            param['amount'] = amount
        param['sign'] = self._signature(param)
        data = urllib.parse.urlencode(param).encode('utf-8')
        req = urllib.request.Request('https://www.okcoin.com/api/trade.do')
        req.add_header("Content-Type", "application/x-www-form-urlencoded;charset=utf-8")
        f = urllib.request.urlopen(req, data)
        print(f.status)
        jsondata = json.loads(f.read().decode('utf-8'))
        print(jsondata)
        result = jsondata['result']
        if result == False:
            print("ErrCode=%d" % jsondata['errorCode'])
        else:
            print("order %s ltc success, order_id=%d" % (type, jsondata['order_id']))
        return result

    # trade ltc interface
    def buy_ltc(self, rate, amount):
        return self.trade('ltc_cny', 'buy', rate, amount)

    def sell_ltc(self, rate, amount):
        return self.trade('ltc_cny', 'sell', rate, amount)

    def buyMarket_ltc(self, rate):
        return self.trade('ltc_cny', 'buy_market', rate)

    def sellMarket_ltc(self, amount):
        return self.trade('ltc_cny', 'sell_market', amount=amount)

    # trade btc interface
    def buy_btc(self, rate, amount):
        return self.trade('btc_cny', 'buy', rate, amount)

    def sell_btc(self, rate, amount):
        return self.trade('btc_cny', 'sell', rate, amount)

    def buyMarket_btc(self, rate):
        return self.trade('btc_cny', 'buy_market', rate)

    def sellMarket_btc(self, amount):
        return self.trade('btc_cny', 'sell_market', amount=amount)

    def getOrder_ltc(self, orderid = -1):
        # get ltc orders
        param = {
            'partner' : self.partner,
            'order_id' : orderid,
            'symbol' : 'ltc_cny'
        }
        param['sign'] = self._signature(param)
        data = urllib.parse.urlencode(param).encode('utf-8')
        req = urllib.request.Request('https://www.okcoin.com/api/getorder.do')
        req.add_header("Content-Type", "application/x-www-form-urlencoded;charset=utf-8")
        f = urllib.request.urlopen(req, data)
        print(f.status)
        jsondata = json.loads(f.read().decode('utf-8'))
        print(jsondata)
        result = jsondata['result']
        if result == False:
            print("ErrCode=%d" % jsondata['errorCode'])
            return None

        orders = jsondata['orders']
        return orders

    def cancelOrder_ltc(self, orderid):
        param = {
            'partner' : self.partner,
            'order_id' : orderid,
            'symbol' : 'ltc_cny'
        }
        param['sign'] = self._signature(param)
        data = urllib.parse.urlencode(param).encode('utf-8')
        req = urllib.request.Request('https://www.okcoin.com/api/cancelorder.do')
        req.add_header("Content-Type", "application/x-www-form-urlencoded;charset=utf-8")
        f = urllib.request.urlopen(req, data)
        print(f.status)
        jsondata = json.loads(f.read().decode('utf-8'))
        print(jsondata)
        result = jsondata['result']
        if result == False:
            print(sys._getframe().f_code.co_name + ':' + sys._getframe().f_lineno)
            print("ErrCode=%d" % jsondata['errorCode'])

        return result