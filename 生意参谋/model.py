from Setting import *
from CurrencyModule import *
from 淘宝.test2 import *


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
            raise '转化出错'
        print(extData)
        return extData

    # 市场大盘月度获取
    def market_info(self, cateid, dts_cookie, start_month, end_month, cookie):
        url = "https://sycm.taobao.com/mc/mq/supply/mkt/overview.json"
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'bx-ua': '223!g26SXoDgz6jgGCgyyg67xMFGrOX+xO6SoGmrPzgp4xKlhxinwCesBKUnSbimidGEIVO+2aXHN5kJuLpiqzcI/HTUYupq+PIvygG12GKNzsypKm5HKUT/PCRycK4je194rjR1zJUd+6Q4cgRTSeT/rXRu/Omqe1Q1+QMYiwYg/I38xNpC5oCkujRycAcq+x9tLljUz3x/e634cQQpWUT/rCWycAEs+1C4rQQ4hdg48PuIt5u+qlG08h+W6I+XzwVGiEV9M4UvjkFZbyyMCwoAewVlfc87oupGK0bR/DiiRJmrJjezelK4Lt97iHSv2Db+VooF8PRnBmwbrkey3k487VnRnKR63KI1nVBK46TL+/xICKRissuMhLJI5c0xciZi/2WMX6Id3EHYHIosGWH7xDP3gZpc7ZyV6jSDK3NLJ4ISa0Kcsuq1/3wo6kS12pPclfyzaqCFpHbknnpvpq6y25kY8l0QK9vO+dtFXDwrhVcEfeqdqKRFb4X8XgDyx8++9nIQDQp0tq7u6l+6C9u+Y027Ok8LIblJ8rRzrVfD54GpIFmra6jtyFi+xIRA0shHKsR9jigEOU/9/HbN1FFsQ1vVLkx97Dq1sZI95gxfYFpx7u8Hge33c8WIWMbMEsOHNn+AYNj4ZUMq4qerGzb0U7juFZtPrAJrPgo85AOG83a0SntcYrUKe7qeYnepb3F4zHq7Txn3IVendj8eTkNf+hKa5EhuvB9FL8HgT8DEh5GJMUGN1yfHZxyTbBMQGgJnL2jEDU2h68j8+A+rULsOkPZ5jgOS+NcVQVTWpFZLljnTkhm7GKJBpWLV/vSmCLldt61hRf43hxfThVtWFBfo+kTYC6TqXNUNexg7p5xj2idXjI5v9gmRTcIhdjVha6dCBOQW1U/w2xftXBLwWRs8vV8yqv5LCH/lU8vHnmWL6dgbh/KOh1YLO5IlOx+leAlzZof+c9Z0ePVaRu5oOOsXWtWDyLiMZTWFsL2r4mS91yU5FZOlfSxNxGM7bNKX1LNBpeXMEHj3gtZ5CnpU5Mdif9aBJSTnHIUjfPpd1wwc3Vabl9fkItr1F+3fPdtnbv5oN8cFwu2sNpDY/uFwctMSgO8qcBy7eAzqIbU3yZpn5YzmKPcop/bo1pyYNDbApC==',
            'bx-umidtoken': 'G177E93F22AAEC8FD54AC794C5414A09A51194D00E6FB63190F',
            'bx-v': '2.2.3',
            'cache-control': 'no-cache',
            'cookie': cookie,
            'onetrace-card-id': 'sycm-mc-mq-market-overview.sycm-mc-mq-cate-trend',
            'pragma': 'no-cache',
            'referer': 'https://sycm.taobao.com/mc/mq/overview?cateFlag=1&cateId=50014812&dateRange=2022-09-17%7C2022-09-17&dateType=day&sellerType=-1&spm=a21ag.11815228.LeftMenu.d590.671a50a53Y0VvJ',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sycm-query': 'dateType=day',
            'sycm-referer': '/mc/mq/overview',
            'transit-id': 'K+PS/ycpE5fo6EkCYK0yiuODtUU1kig4maD6Na+9e6eONIFCFxXbFYEnM0emQdcLmUgn2ylHoxpjoGqmAhjqcl5Zl15jhlCW25yJw5nOJsNQJ23rrdy8RCrXy9S7aEuZOIabPbfBMnosWMhVg7aHGIvgZ2FEoaEmL5EtCHpvEXU=',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        params = {
            'dateType': 'month',
            'dateRange': f'{start_month}-01|{get_before_day(get_after_month(start_month) + "-01")}',
            'cateId': cateid,
            'device': '0',
            'sellerType': '-1',
            '_': '1663654362374',
            'token': 'f5b822396'
        }
        response = requests.get(url=url, headers=headers, params=params).json()
        datas = response['data']
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
            value.append(change_info(cateid, [info, int(datas[info]['value'])], dts_cookie))
        values = [start_month.replace('-', ''), cateid] + value + [seIpvUvHits, sePvIndex, uvHits, pvHot, cltHits, cltHot, cartHits, cartHot, payByrCntIndex, tradeIndex]
        self.sql_server.save_message('贝德美.dbo.市场大盘_全网_类目_月', [tuple(values)])

    # 获取市场大盘的所有类目
    def get_ids(self, cookie):
        '''
        获取所有类目id结构
        '''
        url = 'https://sycm.taobao.com/mc/common/getShopCate.json?leaf=true&edition=pro&_=1655882260326&token=25ef342ef'
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'bx-ua': '216!LLDI4ymrqUQzNLIfxDsf0ogDv0p3pYsclQbsfKwKQvHmzbnWwQcUzy5SwfRdo6IQU4P4hEmfWa45g13/hLFIt8mEHEN0Q9jzWeF2zYMBXjdyHi9Mn2lmJJRhahtZ1fm0hYv1deiCaNegB48ZBdDwqQ1/SIREpIYozaMFv7m8z3i8jvE5OrP3CbtvYxXK/0WZSHhGvEgAdF8b0EPuC5cHugMy52beeOW5zihVMijAt3ez9GnMLUguU3ZkUf6m12WZnD1o3v5AJgmqnIWAXV0VRBY/Kp7HuqQf98U8skDJ1G2RdB9lIbEVb7e8X29JVDLFZImYRqzJyFGzHKbl0whMnXB0fJloPIiTUMMZ6DHx0yjLqEvueIqsgGpARoYe7SVs6Z5V4OdylYnlzladCTfytEaP5mF0O54y3NrvvMTLh7DWCUMeWH1dRPDqiJypssj+XY6euvjn8sZEI/MeW2nTxDgoiJypssj+XY6eLvq3V3Z6ILsA4LLlBQKQLDD5jnVmocEi90PtdAA7YOkYNQj0WfFw9imIVbL8AByx+pV1WLjKjycT1OuVIIC0Y0bwX2f0GCiQ+2MO22bLSLEhmxdDUMZOCMze2jN2WPReOR3WeQ190GvseIYByQOYJ+aZ8hFaEWwYr3nFrSAsSjaLiY1BjyZGgfft7Ouu79vDmDrZPD1ki1IZmRxkAkIj91DZEchgD1TjscCKBwo7YIPqsOd25l7WJPzJFNjLKOHvrtfpauFnxH/xQmNQXDBwFhJ/YPjN+NThJlSeuF4VAAa9zbFsHD8VsQxvH8cS07Op2Wtzjp+0XU8kEHxSZ52rBcHzMgAmph8vpKzro1fL57U8DQBRoO30j1wkpTbnOeaBcRXfKolvHtrsB3D8UPjxCY7JBlK/RjMcIR2vTKbgwywDKGuCOdy3cdAWi01HV5R8XEuJWC8VxAup3vbRPH5E/rvBWNv9LNSOCGzGJVb4mpXcEZkrPh3qTt0ydiFuu+UDZFDnOCmGsfbKukmPjdkjpuk6r56ceUPzLTZskaszYXWSnRM62dXu9+9WuCkTBJ0bHkjFe9BmhqZRt47U3J5jlauuOHJjnrrl3vczzseKk/vK9rSfx6GQkGehREaeFlcPzks72jj5SkO=',
            'bx-umidtoken': 'T2gAPn2YgI69ZtbgW5AJGdJR1qe10urkx_lTtIqntXXYSEb8RnTG3Yxcefe_Ovyfqhw=',
            'cache-control': 'no-cache',
            'cookie': cookie,
            'pragma': 'no-cache',
            'referer': 'https://sycm.taobao.com/mc/mq/overview?cateId=50012841&dateRange=2021-10-01%7C2021-10-31&dateType=month&parentCateId=50016455&sellerType=-1&spm=a21ag.11815228.LeftMenu.d590.43bf50a5tlJmAo',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sycm-query': 'dateType=month',
            'sycm-referer': '/mc/mq/overview',
            'transit-id': 'Jh6LE8LsALMuuloeYdnN9jznn/2d0SVuYf/Ygl/HdGWuuURSHKAw/twGkSynpiyGcKigtIUFokPPIaSiB97DALnjitja2441L1n6ksQDfNL7BEgSL3mWjDDa8hAq/cZQ8xkUwtQwNdNrYnEkSSYJvscnh9bVQt+bYWRK8U26P/c=',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        response = requests.get(url=url, headers=headers).json()['data']
        print(response)
        return response

    # 市场大盘_全网_类目_月
    def market_network_category_month_start(self, childid, end_month, start_month, dts_cookie, cookie):
        all_childid_ids = self.get_ids(cookie)
        print(all_childid_ids)
        if childid == 50014812 or childid == 50022517:
            print(f'一级类目：{childid}')
            self.market_info(childid, dts_cookie, start_month, end_month, cookie)
        else:
            for i in all_childid_ids:
                print(i[0], i[1], childid)
                print(i)
                if i[0] == childid:
                    print(f'二级类目：{childid} ------> {i[2]} {i[1]}')
                    self.market_info(i[1], dts_cookie, start_month, end_month, cookie)
                    time.sleep(10)
                if i[1] == childid:
                    print(f'叶子类目：{childid} ------> {i[2]} {i[1]} {i[-1]}')
                    self.market_info(i[1], dts_cookie, start_month, end_month, cookie)
                    time.sleep(20)


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

    # dts_cookie = 'Hm_lvt_623a6e6c9e21142aa93edc3fffb24a30=1663579827; token=80265f3e-7127-4e7a-af6b-5d3f450d00b5; Hm_lpvt_623a6e6c9e21142aa93edc3fffb24a30=1663583486'
    # cookie = 't=da03a3a2ff72f7a25e393fbd232e1134; cookie2=121ead4360c93f87765c152c6653fe17; _tb_token_=389583a0e66ae; _samesite_flag_=true; XSRF-TOKEN=acd73bc1-09ac-4719-9f17-828c35aea530; _m_h5_tk=dbddd03a9291277daff1922ca6ac0205_1663819051599; _m_h5_tk_enc=afc5228bc7cc37d15f85037abd6f2a2b; xlly_s=1; sgcookie=E100yv7RbXLvc7adXfbk08znRzcJiiD2UkP7oJSIrr%2BJ3i5tgHy8eR0xqVTgGOAsowh9m3c6awVsbqeTmJPcjYJ9jcoHVkocTOqgiYwfqmBpCgM%3D; unb=2212628883848; sn=dyyyz99%3A%E7%BB%83%E5%BA%86%E9%BE%99%E9%A3%9E; uc1=cookie14=UoeyDbC4V6ww2g%3D%3D&cookie21=VT5L2FSpdiBh; csg=397e0046; cancelledSubSites=empty; skt=b334e9cd84cae9e0; _cc_=WqG3DMC9EA%3D%3D; _euacm_ac_l_uid_=2212628883848; 2212628883848_euacm_ac_c_uid_=4224382495; 2212628883848_euacm_ac_rs_uid_=4224382495; _portal_version_=new; cc_gray=1; v=0; cna=jWCxGw8o4HwCAXPG25PMGsWZ; _euacm_ac_rs_sid_=231244751; JSESSIONID=50E6CAEEAC7DFBDBACECF35646779797; l=fBE4J76mTrlClhfaXOfwPurza77OSIRAguPzaNbMi95POJXe5CZdW6oM5DtwC3GVF6yJR3lMfBR8BeYBqIcvHW3MakQWBdHmnmOk-Wf..; tfstk=cs7VBPTtxrUV1NQsGU8NzZ1it5ufZ8Ccs4RBmJKvW_t_4CtcitD9ZKOvaCGrInf..; isg=BJKSV_3DJQYqt1l7_tZs9er441h0o5Y9vkUn0lzrvsUwbzJpRDPmTZiJ38vTHw7V'
    # ba.market_network_category_month_start(122854005, '2022-08', '2022-08', dts_cookie, cookie)