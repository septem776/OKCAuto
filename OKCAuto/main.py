#!/usr/bin/env python
#coding=utf8

import http.client, json
import time

def GetData(httpClient, url):
    try:
        httpClient.request('GET', url)
        response = httpClient.getresponse()
        data = response.read().decode('utf-8')
        jsondata = json.loads(data)
        return jsondata
    except Exception as e:
        print(e)
        return None

def GetTicker(httpClient):
    url = '/api/ticker.do?symbol=ltc_cny'
    jaondata = GetData(httpClient, url)
    print(jaondata)
    pass

def GetDepth(httpClient):

    pass


if __name__ == '__main__':
    httpClient = None

    try:
        httpClient = http.client.HTTPConnection('www.okcoin.com', 80, timeout=30)
        for i in range(1):
            GetTicker(httpClient)
            time.sleep(0.5)
    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()
