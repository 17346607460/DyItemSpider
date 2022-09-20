import time

import requests
from Setting import *
from CurrencyModule import *
from test2 import *


class BusinessAdviser:
    def __init__(self):
        self.sql_server = SqlServerConnect()

    #  贝德美.dbo.市场排行_商品_高流量_天猫_类目_月
    def get_goods_gll_main(self, start_day, cateid, cookie):
        response = self.get_goods_gll_request(cateid, start_day, cookie)
        num = 1
        for data in response:
            item_title = data['item']['title']  # 商品名称
            item_itemId = data['item']['itemId']  # 商品id
            shop_title = data['shop']['title']  # 店铺名称
            uvIndex = data['uvIndex']['value']  # 流量指数
            try:
                seIpvUvHits = data['seIpvUvHits']['value']  # 搜索人气
            except:
                seIpvUvHits = None
            tradeIndex = data['tradeIndex']['value']  # 交易指数

            value = (start_day.replace('-', ''), cateid, item_title, shop_title, item_itemId, num, self.get_change(uvIndex), self.get_change(seIpvUvHits), self.get_change(tradeIndex), uvIndex, seIpvUvHits, tradeIndex)
            self.sql_server.save_message('贝德美.dbo.市场排行_商品_高流量_天猫_类目_月', [value])
            num += 1

    def get_goods_gll_request(self, cateId, start_day, cookie):
        url = 'https://sycm.taobao.com/mc/v2/mq/mkt/rank/item/hotsearch.json'
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'bx-ua': '222!4YExHkPrhakPh99a5kas7mQ2GWNk083CHOuFzJ8jJRnlwlIwt71cHOHg4uj9q9sLhGnET946JnFjofnkVOMJrnJdPFqbvMY31K6VPkvPD0ayuU8VjklNylxkjiRE/6qPKO/9r/+SV0Vd//Y1B0QiJEDcZchQYZ4FSrmhJGM1m/SjL20jHFfOMFprY2P9rOvZJsdbZp+P6+2VhBeswC7O1SoKhDC7ph0MicalRkW0rFtJ8t6CxqEKrZ2BScNYRFAYyh2DSdrUGbpighLh2l2or/pBnhdYOYL2gK2hnr2jysN+gpIXy1zL6fyj7GSv2LsufGKZwT4BmbhX3d8TswWbFFSnZR4fDpRseIqMI5OnW4t8fFdAssrs70ToVicAENL/xypierwTgLASpdLwFY09KFHMabrVIuUfCUB00CWu6IJK116wxaXbHi2JWIuhmXhJO2aarh+TIafO3/MNAxQhmu0tD95IwcMqFx+p7CxtcZ2BF2sl+jhxxnDetresjEfCxrNdVC6HFhcgkDdY4cIS6KGDvpUyeWps+cEvC61+FDEMV/JV338gouov6I2uqe5cRj+Pq62yExPBi3kJ+6kFoAg/TDWEM6JcHD58gXET1xylY5KM8F3v49jAETgrZkw5I95zbS2NdnKf5g3R4u/ur5GjKxdKl8TCP7m4SR/z8I9aUQ4sVTZcQpJ3MjVKpgwnEZrhOdW475uKuuuJ778/gFgE/8MjkuN/khvOFgsD2izD5io8M3WX8TntBP6dMiM3a4sMsShSHtIORxwVnOnPJXA1WsF+MdVJ4HGfo4CfrLyF9n9dr6q8zNHP7ObKo3pMERxwidmU/mmB/A59Bq41VE7LPFdzfA4aSv/ComAVDQHIMelpvc7qIJ6SPIEbtoXlJsNQK0ZnCFjP0SmQV9bLBDLMlnvysfgxQZPL0io0i1KLcDILYdnRXIs+TTPiuyXmJajHW6xw9ldh9bQylP/GyjE9NyjWRjMbW2Qg5k/6RgSHKIQ0c9XsR9VtQqtBsIoFhe3BmrqEy7zoqnjhPPlk/3kZMAxQWxchNcopSjo+sffklCEn99WmBo+r6IDW2OHUoiMYTR/HdnqBvmuNolyP667LCb1NZhjR/7xhJPO1a9us7rtWqbpdHmBMQJTnrRFnBYMrVlFt8qyyw6vfj/bWeJijmL0AK3tlERoEd2HWpX2R+d4ngUdZ5MfruMxQjTawDev+0CcKYAq5gZbuXir8gvNfBqM=',
            'bx-v': '2.2.0',
            'cache-control': 'no-cache',
            'cookie': cookie,
            'onetrace-card-id': 'sycm-mc-mq-market-rank.sycm-mc-mq-item-item-search',
            'pragma': 'no-cache',
            'referer': 'https://sycm.taobao.com/mc/mq/market_rank?activeKey=item&cateFlag=2&cateId=201303304&dateRange=2022-06-01%7C2022-06-30&dateType=month&parentCateId=50022517&sellerType=1&spm=a21ag.11815245.LeftMenu.d591.3fd050a5LDGIiS',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sycm-query': 'dateType=month&activeKey=item',
            'sycm-referer': '/mc/mq/market_rank',
            'transit-id': 'R4n9lqfk/EbJXzTrSLW3ewlDujGQ4K+kks6ZoqMPuki6eDOUZYptVUz/XpqKojidNKNc5lxndEMwr5dW8CVDbojO34D6HQOlMINHksmGT5XzZ+ggOiAOlywWGdLfM+ZtRx2yZW8nK3+tmzMOf4pVsiMRFhaKVCh6SE10ZuI/A9A=',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        params = {
            'dateRange': f'{start_day}-01|{get_before_day(get_after_month(start_day)+"-01")}',
            'dateType': 'month',
            'pageSize': '10',
            'page': '1',
            'order': 'desc',
            'orderBy': 'uvIndex',
            'cateId': f'{cateId}',
            'device': '0',
            'sellerType': '1',
            'styleId': '',
            'priceSeg': '',
            'pageId': '',
            'indexCode': 'uvIndex,seIpvUvHits,tradeIndex',
            '_': '1658989562736',
            'token': '0356c6eee'
        }
        response = requests.get(url=url, headers=headers, params=params).json()
        datas = response['data']
        return datas

    def get_goods_gjy_main(self, start_day, cateId, cookie):
        response = self.get_goods_gjy_request(cateId, start_day, cookie)
        num = 1
        for data in response:
            item_title = data['item']['title']  # 商品名称
            item_itemId = data['item']['itemId']  # 商品id
            shop_title = data['shop']['title']  # 店铺名称
            tradeIndex = data['tradeIndex']['value']  # 交易指数
            # try:
            #     tradeGrowthRange = data['tradeGrowthRange']['value']  # 交易增长幅度
            # except:
            #     tradeGrowthRange = None
            payRateIndex = data['payRateIndex']['value']  # 支付转化指数

            value = (
            start_day.replace('-', ''), cateId, item_title, shop_title, item_itemId, num, self.get_change(tradeIndex), self.get_pay(payRateIndex), tradeIndex, payRateIndex)
            self.sql_server.save_message('贝德美.dbo.市场排行_商品_高交易_天猫_类目_月', [value])
            num += 1

    def get_goods_gjy_request(self, cateId, start_day, cookie):
        url = 'https://sycm.taobao.com/mc/v2/mq/mkt/rank/item/hotsale.json'
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'bx-ua': '222!OfJI49PrBA3P199a5Mas5yQ2GWNk083CHOuFzJ8jJRnlwlIwt71cHOHg4uj9q9sLhGnET946JnFjofnkVOMJrnJdPFqbvMY31K6VPkvPD0ayuU8VjklNylxkjiRE/6qPKO/9r/+SV0Vd//Y1B0jZr4IOiuvhsTRLEMM51UOK9tv2QLRJo8vCfGhwGEMrQEwd3zpAVT20mEG9i8r4XEWze9cdm2QZdeoYVvmF5PRaUFAOwk7RfgDYE5ABgKwy2j8cEtXBSKFjxlKauhlW6kH9EYLigJzD99CcEKXbSKR9PFn3y++BgpIXy1zL6WKYqHPYalBUYPD+XmgvzwKCijJ0qolJYbJxjKAkFzhQ/UKD0lk3qDtP6GgoqX3J6+qFMIui6WwWZTIw8A6cpkR6NSYUQjYUgkGwllTUqDbKPHR/iecav6Ju3QUweUfbxw0JhkCtJs2/C+4th9xZoIu/XjL5v+Hw0lCwRLP/xc+qvhmvBID7h9n7rN4tQ/OupYshSRUjll+0cY2ao/8tl6Eri0Y+G8jp9JLUlW+KUxkMuuxo47i8syxdwmunBcO23KHsFvMMDdzlyLAxsyud+zE1pceRxLTehjUcjGY0HYrcep+pdH3Pz8gaPoahdVzWV+kgywSstMxrviAInAW1aMT5otrFIze+piVMIq9k56x7ZTlMhjY3A6sixMaWamn9TKpbMVRP8gtqHYcFnvVUN9rv4wpxe0rl+DYMrUhsTDqARteUKiO8z8Jj2OFkjWkGKTSZAorO8VBO0eu0EfY4B1EJf3NFHNrKrGMGQrrjcXtsVxCaEfy1d7AbqbtEhaWXRNyIhTSB+kCz1MxZgNPRIGzyWqYShjFvOWLC7cDr2yD7tSYf8eA8DT6KBLRuEvInUucVoDpkPlckUt9wEr9Qay1ArODEHSMIkrj+AonJh+4McgWd7Nkhy0K3ONsMVmCx+SuDegPHqEbpZl/IvCnxFiVIqZ07VUeq1r6u6F+/Vwh16HT24zE+iiFUHHzGvK2dlvFhPj/ZkwkNs/A0zqwBiUThgsX3tylDsk2tU1eJr4rgHTp38lxEVi0ek9tJfMAdufXBcDrENOitlNCBP+B67rrV7kv3lwEzgTY4E7kYUefHWQjZBhdFKJgaWbJRTYlG/L37myKgZh3JQZ4Huls=',
            'bx-v': '2.2.0',
            'cache-control': 'no-cache',
            'cookie': cookie,
            'onetrace-card-id': 'sycm-mc-mq-market-rank.sycm-mc-mq-item-item-sale',
            'pragma': 'no-cache',
            'referer': 'https://sycm.taobao.com/mc/mq/market_rank?activeKey=item&cateFlag=2&cateId=121398016&dateRange=2022-06-01%7C2022-06-30&dateType=month&parentCateId=121388024&sellerType=1&spm=a21ag.11815245.LeftMenu.d591.3fd050a5LDGIiS',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sycm-query': 'dateType=month&activeKey=item',
            'sycm-referer': '/mc/mq/market_rank',
            'transit-id': 'cdA0u1bZhnlIHRxAF2jtOy3IWDHr76XrS37HjmDrSiWBukFrK4ANkd5kVVFFT+SDEdczgAFTwjfzO2Xe5bzGqAl7quI/zKlLICU1c0X8Qn9YGDAZVj4j49SNs/W0Tr0LUNZr5ABJ2Z1D+b7iqAaOvBvtOIuVRxXzDHIDVQ77qtk=',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        params = {
            'dateRange': f'{start_day}-01|{get_before_day(get_after_month(start_day)+"-01")}',
            'dateType': 'month',
            'pageSize': '10',
            'page': '1',
            'order': 'desc',
            'orderBy': 'tradeIndex',
            'cateId': f'{cateId}',
            'device': '0',
            'sellerType': '1',
            'styleId': '',
            'priceSeg': '',
            'indexCode': 'tradeIndex,tradeGrowthRange,payRateIndex',
            '_': '1658995470666',
            'token': '0356c6eee'
        }
        response = requests.get(url=url, headers=headers, params=params).json()
        return response['data']

    def get_change(self, x):
        if x == 0 or x == None:
            return 0
        url = 'https://diantoushi.com/switch'
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            # 'accept-encoding': 'gzip, deflate, br',
            # 'accept-language':' zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-length': '35',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': 'Hm_lvt_623a6e6c9e21142aa93edc3fffb24a30=1651805650; Hm_lpvt_623a6e6c9e21142aa93edc3fffb24a30=1652765584; token=eddd54d1-98b5-4f63-b864-571b29572fd5',
            'origin': 'https://diantoushi.com',
            'pragma': 'no-cache',
            'referer': 'https://diantoushi.com/index.html',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        data = {
            'values': f'[{x}]',
            'type': 'change'
        }
        response = requests.post(url, headers=headers, data=data, verify=False).json()
        print(x, response)
        return response['extData'][0]

    def get_pay(self, x):
        if x == 0 or x == None:
            return 0
        if float(x) >= 3693:
            return 1.0000
        url = 'https://diantoushi.com/switch'
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-length': '32',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': 'Hm_lvt_623a6e6c9e21142aa93edc3fffb24a30=1639360118; Hm_lpvt_623a6e6c9e21142aa93edc3fffb24a30=1639360118; token=4bfc6ee8-f98b-4ff6-8184-7b4218511527',
            'origin': 'https://diantoushi.com',
            'pragma': 'no-cache',
            'referer': 'https://diantoushi.com/index.html',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        data = {
            'values': f'["{x}"]',
            'type': 'pay'
        }
        res = requests.post(url, headers=headers, data=data, verify=False).json()
        print(res)
        try:
            extData = float(res['extData'][0].replace('%', '')) / 100
            extData = '%.4f' % extData
        except:
            print('-----------------------------------------------------------------')
            extData = get_pay(int(x))
        print(extData)
        return extData

    # 市场大盘月度获取
    def market_info(self, cateid, dts_cookie, start_month, end_month):
        # url = "https://sycm.taobao.com/mc/mq/supply/mkt/overview.json"
        # headers = {
        #     'accept': '*/*',
        #     'accept-language': 'zh-CN,zh;q=0.9',
        #     'bx-ua': '223!g26SXoDgz6jgGCgyyg67xMFGrOX+xO6SoGmrPzgp4xKlhxinwCesBKUnSbimidGEIVO+2aXHN5kJuLpiqzcI/HTUYupq+PIvygG12GKNzsypKm5HKUT/PCRycK4je194rjR1zJUd+6Q4cgRTSeT/rXRu/Omqe1Q1+QMYiwYg/I38xNpC5oCkujRycAcq+x9tLljUz3x/e634cQQpWUT/rCWycAEs+1C4rQQ4hdg48PuIt5u+qlG08h+W6I+XzwVGiEV9M4UvjkFZbyyMCwoAewVlfc87oupGK0bR/DiiRJmrJjezelK4Lt97iHSv2Db+VooF8PRnBmwbrkey3k487VnRnKR63KI1nVBK46TL+/xICKRissuMhLJI5c0xciZi/2WMX6Id3EHYHIosGWH7xDP3gZpc7ZyV6jSDK3NLJ4ISa0Kcsuq1/3wo6kS12pPclfyzaqCFpHbknnpvpq6y25kY8l0QK9vO+dtFXDwrhVcEfeqdqKRFb4X8XgDyx8++9nIQDQp0tq7u6l+6C9u+Y027Ok8LIblJ8rRzrVfD54GpIFmra6jtyFi+xIRA0shHKsR9jigEOU/9/HbN1FFsQ1vVLkx97Dq1sZI95gxfYFpx7u8Hge33c8WIWMbMEsOHNn+AYNj4ZUMq4qerGzb0U7juFZtPrAJrPgo85AOG83a0SntcYrUKe7qeYnepb3F4zHq7Txn3IVendj8eTkNf+hKa5EhuvB9FL8HgT8DEh5GJMUGN1yfHZxyTbBMQGgJnL2jEDU2h68j8+A+rULsOkPZ5jgOS+NcVQVTWpFZLljnTkhm7GKJBpWLV/vSmCLldt61hRf43hxfThVtWFBfo+kTYC6TqXNUNexg7p5xj2idXjI5v9gmRTcIhdjVha6dCBOQW1U/w2xftXBLwWRs8vV8yqv5LCH/lU8vHnmWL6dgbh/KOh1YLO5IlOx+leAlzZof+c9Z0ePVaRu5oOOsXWtWDyLiMZTWFsL2r4mS91yU5FZOlfSxNxGM7bNKX1LNBpeXMEHj3gtZ5CnpU5Mdif9aBJSTnHIUjfPpd1wwc3Vabl9fkItr1F+3fPdtnbv5oN8cFwu2sNpDY/uFwctMSgO8qcBy7eAzqIbU3yZpn5YzmKPcop/bo1pyYNDbApC==',
        #     'bx-umidtoken': 'G177E93F22AAEC8FD54AC794C5414A09A51194D00E6FB63190F',
        #     'bx-v': '2.2.3',
        #     'cache-control': 'no-cache',
        #     'cookie': '_samesite_flag_=true; cookie2=14ddb4a56cce7567b01d80c90c00b3c7; t=8017ee70287cb1ebffabe3247a6d01b6; _tb_token_=e9e673b74b6e3; XSRF-TOKEN=2f0d9d65-63ce-4438-a148-91318c6c9262; xlly_s=1; thw=cn; sgcookie=E1002mrkV1lvER5j16hjsj0pcQC302DXOmbsJsfhSKJnlD6xZ2NnCqAHKiPPyLg82zTfJXbdJUWnF9s6ra99jf%2FfgyShiFVtjjh0h6kGwPfTuus%3D; unb=2212628883848; sn=dyyyz99%3A%E7%BB%83%E5%BA%86%E9%BE%99%E9%A3%9E; uc1=cookie14=UoeyDb7nP6lhzA%3D%3D&cookie21=WqG3DMC9Eman; csg=9640dbf8; cancelledSubSites=empty; skt=732e0f84832eb7d9; _cc_=URm48syIZQ%3D%3D; cna=B86mGwVewTECAXPDhgk9aeut; _euacm_ac_l_uid_=2212628883848; 2212628883848_euacm_ac_c_uid_=4224382495; 2212628883848_euacm_ac_rs_uid_=4224382495; _portal_version_=new; cc_gray=1; v=0; _euacm_ac_rs_sid_=231244751; _m_h5_tk=48545b892a5d081ad0622993e0d0d7bd_1663664615249; _m_h5_tk_enc=4bd3dc1b51c44319a41350c5eb9bb423; x5sec=7b226f702d6d633b32223a226166303163313962663664356665356437343766313865363139383437346631434d537a705a6b47454e7630327172507135336d62526f504d6a49784d6a59794f4467344d7a67304f4473784d49754e376454352f2f2f2f2f77464141773d3d227d; JSESSIONID=4A9CC799A500137BCEBC03FF6589D8E2; tfstk=cWjhBV6BHw8QNvHiqwtQ4wbm5bRhZxiyigS1bJIzw5YkOOINiz0ZuhO8IBVbT41..; l=fBNhYW9VTEW_wyjNBO5CFurza77TEIRb8sPzaNbMiIeca6p1Lem9GNCEfreybdtjgTfbpetrshOewRFHP-438x_hQJXiua1hps96-bpU-L5..; isg=BBoappmDLTwZ5KGmu3FagEXna8A8S54lZi2_eiSTCq1wl7vRDN_eNNWhZ2MLRxa9',
        #     'onetrace-card-id': 'sycm-mc-mq-market-overview.sycm-mc-mq-cate-trend',
        #     'pragma': 'no-cache',
        #     'referer': 'https://sycm.taobao.com/mc/mq/overview?cateFlag=1&cateId=50014812&dateRange=2022-09-17%7C2022-09-17&dateType=day&sellerType=-1&spm=a21ag.11815228.LeftMenu.d590.671a50a53Y0VvJ',
        #     'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        #     'sec-ch-ua-mobile': '?0',
        #     'sec-ch-ua-platform': 'Windows',
        #     'sec-fetch-dest': 'empty',
        #     'sec-fetch-mode': 'cors',
        #     'sec-fetch-site': 'same-origin',
        #     'sycm-query': 'dateType=day',
        #     'sycm-referer': '/mc/mq/overview',
        #     'transit-id': 'K+PS/ycpE5fo6EkCYK0yiuODtUU1kig4maD6Na+9e6eONIFCFxXbFYEnM0emQdcLmUgn2ylHoxpjoGqmAhjqcl5Zl15jhlCW25yJw5nOJsNQJ23rrdy8RCrXy9S7aEuZOIabPbfBMnosWMhVg7aHGIvgZ2FEoaEmL5EtCHpvEXU=',
        #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        # }
        # params = {
        #     'dateType': 'month',
        #     'dateRange': f'{start_month}-01|{get_before_day(get_after_month(start_month) + "-01")}',
        #     'cateId': cateid,
        #     'device': '0',
        #     'sellerType': '-1',
        #     '_': '1663654362374',
        #     'token': 'f5b822396'
        # }
        # response = requests.get(url=url, headers=headers, params=params).json()
        # print(response)
        # datas = response['data']
        datas = '978A6CAB053F0786DA3FDCE8F4A06FE64A65BD9E70931938146734F166B386C09068481D93B5CCA05C1E40F5125263D74A56FDE68EBC699711F556CEE46465CA50F33B6AD009BBF4EEA20A78C3D650E011B6DB29358612395E77920FDB80DF85F3656CF0DCB3DFA94A6E7980C38FF954B6740EFB63641291F9882CF4894AF9E20B9DBC4AE0316738DFEF49C9720456426CDAA63CA8D28A7AE1E34C3415FBB6889B11E61EA4490197A2B3F7AD4D4AD098F481253B9BF66E10C63343D5871959C953B02BE6CE02859999D79AC9EED7010D2D33B190A679B8D221F19534DF8CEE93292FEB8F81BFDEDF47E8DD834CAB098E29F3DF783B69644BDD69887BDD4F8893B41725078AD03A1581803D2D88052B1380D98730A5D42F75D56CD6F635882C51CE434A8FA904D613C14D196EA89C435B3437B7D0417DB72896EB34AC1DF4F72D51FCD98D8772E12EBA800DA9D611806F93F601539771CFB6D07196F539A2A105AF1E339CE3D94A8850A5B6E7B3C60010DD6165B5DA9306594F82F1431EE201FCD1695CD4722012B72C61B60DE183CD7C653087CAF44EFA29C2839D0F5B4E527F8E0916E8F62B50EB0D2CE4F9B133A1DBA00A1F31741A5DA915315D60C04240D285A3EC4F6C2D785D3A8D43916E3625CD83E6939B1F84A40164B6927BFC317484'
        datas = decrypt(datas)
        print(datas)
        # 搜索人气 搜索热度 访问人气 浏览热度 收藏人气 收藏热度 加购人气 加购热度 客群指数 交易指数
        seIpvUvHits = datas['seIpvUvHits']['value']
        sePvIndex = datas['sePvIndex']['value']
        uvHits = datas['uvHits']['value']
        pvHot = datas['pvHot']['value']
        cltHits = datas['cltHits']['value']
        cltHot = datas['cltHot']['value']
        cartHits = datas['cartHits']['value']
        cartHot = datas['cartHot']['value']
        payByrCntIndex = datas['payByrCntIndex']['value']
        tradeIndex = datas['tradeIndex']['value']
        infos = ['seIpvUvHits', 'sePvIndex', 'uvHits', 'pvHot', 'cltHits', 'cltHot', 'cartHits', 'cartHot', 'payByrCntIndex', 'tradeIndex']
        value = []
        for info in infos:
            # print([info, int(datas[info]['value'])])
            value.append(change_info(cateid, [info, int(datas[info]['value'])], 'Hm_lvt_623a6e6c9e21142aa93edc3fffb24a30=1663579827; token=80265f3e-7127-4e7a-af6b-5d3f450d00b5; Hm_lpvt_623a6e6c9e21142aa93edc3fffb24a30=1663583486'))
        values = value + [seIpvUvHits, sePvIndex, uvHits, pvHot, cltHits, cltHot, cartHits, cartHot, payByrCntIndex, tradeIndex]
        print(values)


if __name__ == '__main__':
    ba = BusinessAdviser()
    # 贝德美.dbo.市场排行_商品_高流量_天猫_类目_月
    # cookie = '_samesite_flag_=true; cookie2=1ed98204f20c3175affff21ad4e83b6b; t=6772aade70f1266bce8e188f7b952cd2; _tb_token_=7ee3e700b1a3e; XSRF-TOKEN=46e52499-460a-4b71-9908-2dd988f0dde6; xlly_s=1; _m_h5_tk=3e62aa1291971afe42af3e25d2f0b6ee_1662017829595; _m_h5_tk_enc=8bbd129bb6015e159a7c828b91ae87c8; sgcookie=E1005Y%2B8QUoVlTBAi4FmUynJKON9I9YnColOFPy%2BWS2WXB%2BSTjQYa4Roxvv%2FFHL2%2FMcX15cbdaltJKKFV5U1sHjmFeRJzym88PqRHE0dW310rd8%3D; unb=2212628883848; sn=dyyyz99%3A%E7%BB%83%E5%BA%86%E9%BE%99%E9%A3%9E; uc1=cookie14=UoeyDHLAvEWu5Q%3D%3D&cookie21=URm48syIZx9a; csg=839c6fad; cancelledSubSites=empty; skt=d75f0eed95a42ffc; _cc_=UIHiLt3xSw%3D%3D; _euacm_ac_l_uid_=2212628883848; 2212628883848_euacm_ac_c_uid_=4224382495; 2212628883848_euacm_ac_rs_uid_=4224382495; _portal_version_=new; cc_gray=1; v=0; cna=ShmPG6F08j8CASQbaTSenDWQ; _euacm_ac_rs_sid_=null; JSESSIONID=F251A78C55A58DBF2A37DBDA1029D177; isg=BLS0piwEa_eTCP8j1U68EpUZhXImjdh3bFPBCE4TyD_XuVIDd5lmB6Q_OfFhQRDP; l=fBNYW7Y4Tjas_PMfBO5Znurza77toBRfhsPzaNbMiIeca6dy6Fij-NCEH5iRJdtjgT5q_eKrshOewR3XycULRxguO5giQOiD7TJwReM3N7AN.; tfstk=cFZcBdwjprufSeeUQoifjpsIoHXVaZtZtlr74tOJ3JXnWdEn3scDzeoS6TccOs81.'
    # start_day = '2022-08'
    # end_day = '2022-08'
    # while True:
    #     ba.get_goods_gll_main(start_day, '50012421', cookie)
    #     # 贝德美.dbo.市场排行_商品_高交易_天猫_类目_月
    #     ba.get_goods_gjy_main(start_day, '50012421', cookie)
    #     if start_day == end_day:
    #         break
    #     start_day = get_after_month(start_day)
    #     time.sleep(20)
    ba.market_info('50252001', '_samesite_flag_=true; cookie2=14ddb4a56cce7567b01d80c90c00b3c7; t=8017ee70287cb1ebffabe3247a6d01b6; _tb_token_=e9e673b74b6e3; XSRF-TOKEN=2f0d9d65-63ce-4438-a148-91318c6c9262; xlly_s=1; thw=cn; sgcookie=E1002mrkV1lvER5j16hjsj0pcQC302DXOmbsJsfhSKJnlD6xZ2NnCqAHKiPPyLg82zTfJXbdJUWnF9s6ra99jf%2FfgyShiFVtjjh0h6kGwPfTuus%3D; unb=2212628883848; sn=dyyyz99%3A%E7%BB%83%E5%BA%86%E9%BE%99%E9%A3%9E; uc1=cookie14=UoeyDb7nP6lhzA%3D%3D&cookie21=WqG3DMC9Eman; csg=9640dbf8; cancelledSubSites=empty; skt=732e0f84832eb7d9; _cc_=URm48syIZQ%3D%3D; cna=B86mGwVewTECAXPDhgk9aeut; _euacm_ac_l_uid_=2212628883848; 2212628883848_euacm_ac_c_uid_=4224382495; 2212628883848_euacm_ac_rs_uid_=4224382495; _portal_version_=new; cc_gray=1; v=0; _euacm_ac_rs_sid_=231244751; _m_h5_tk=48545b892a5d081ad0622993e0d0d7bd_1663664615249; _m_h5_tk_enc=4bd3dc1b51c44319a41350c5eb9bb423; x5sec=7b226f702d6d633b32223a226166303163313962663664356665356437343766313865363139383437346631434d537a705a6b47454e7630327172507135336d62526f504d6a49784d6a59794f4467344d7a67304f4473784d49754e376454352f2f2f2f2f77464141773d3d227d; JSESSIONID=4A9CC799A500137BCEBC03FF6589D8E2; tfstk=cWjhBV6BHw8QNvHiqwtQ4wbm5bRhZxiyigS1bJIzw5YkOOINiz0ZuhO8IBVbT41..; l=fBNhYW9VTEW_wyjNBO5CFurza77TEIRb8sPzaNbMiIeca6p1Lem9GNCEfreybdtjgTfbpetrshOewRFHP-438x_hQJXiua1hps96-bpU-L5..; isg=BBoappmDLTwZ5KGmu3FagEXna8A8S54lZi2_eiSTCq1wl7vRDN_eNNWhZ2MLRxa9', '2022-07', '2022-07')