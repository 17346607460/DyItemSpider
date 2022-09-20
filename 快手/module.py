import requests
from CurrencyModule import *
from auto_login import *
from Setting import *


class FastHand:
    def __init__(self):
        self._sql_server = SqlServerConnect()

    # 快分销_效果明细
    def effect_mingxi_main(self, start_day, end_day, cookie):
        while True:
            if not start_day:
                start_day = self._sql_server.get_start_day('贝德美.KS.快分销_效果明细', '日期', '')
                if start_day == get_before_day(get_today()):
                    print('数据获取完毕')
                    return 0
                start_day = get_after_day(start_day)
            if not end_day:
                end_day = get_before_day(get_today())
            page = 0
            while True:
                response = self.effect_mingxi_request(start_day, cookie, page)
                print(response)
                datas = response['data']
                if not datas:
                    break
                res = 0
                for data in datas:
                    totalPv = data['totalPv']  # pv
                    totalUv = data['totalUv']  # uv
                    payOrderNum = data['payOrderNum']  # 支付笔数
                    payOrderAmount = round(int(data['payOrderAmount']) / 100, 2)  # 支付gmv
                    commissionRate = round(int(data['commissionRate']) / 1000, 2)  # 佣金比例
                    commissionAmount = round(int(data['commissionAmount']) / 100, 2)  # 预估佣金
                    techServiceAmount = data['techServiceAmount']  # 技术服务费
                    itemId = data['itemId']  # 商品id
                    itemTitle = data['itemTitle']  # 商品名称
                    promoterId = data['promoterId']  # 达人id
                    if not promoterId:
                        promoterId = None
                    promoterName = data['promoterName']  # 达人名称
                    if not promoterName:
                        promoterName = None
                    if not payOrderAmount:
                        res = 1
                        continue
                    value = (start_day, totalPv, totalUv, payOrderNum, payOrderAmount, commissionRate, commissionAmount,
                             techServiceAmount, itemId, itemTitle, promoterId, promoterName)
                    self._sql_server.save_message('贝德美.KS.快分销_效果明细', [value])
                if res:
                    break
                page += 1
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)

    def effect_mingxi_request(self, start_day, cookie, page):
        url = 'https://cps.kwaixiaodian.com/distribute/pc/seller/board/list'
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cookie': cookie,
            'Host': 'cps.kwaixiaodian.com',
            'kpf': 'PC_WEB',
            'ks-s-ctn': 'a606b0e0-087e-48ee-bfef-ae7e3565c73f',
            'Pragma': 'no-cache',
            'Referer': 'https://cps.kwaixiaodian.com/pc/cps/data/effectList',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Trace-Id': '1.8369767669828067.916285111523.8337.1657182441281.6',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        print(f'{str(get_time_number(start_day + " 00:00:00")) + "000"}')
        params = {
            # 'startTime': '1657036800000',
            'startTime': f'{str(get_time_number(start_day + " 00:00:00")) + "000"}',
            'endTime': f'{str(get_time_number(start_day + " 00:00:00")) + "000"}',
            # 'endTime': '1657036800000',
            'planType': '0',
            'orderByType': '9',
            'offset': f'{page * 10}',
            'limit': '10'
        }
        response = requests.get(url=url, headers=headers, params=params).json()
        return response

    # 生意通_交易总览 核心数据
    def core_data_main(self, start_day, end_day, cookie):
        while True:
            if not start_day:
                start_day = self._sql_server.get_start_day('贝德美.KS.交易总览', '日期', '')
                if start_day == get_before_day(get_today()):
                    print('数据获取完毕')
                    return 0
                start_day = get_after_day(start_day)
            if not end_day:
                end_day = get_before_day(get_today())
            response = self.core_data_request(start_day, cookie)
            nodes = response['data']['nodes']
            rates = response['data']['rates']
            value = [start_day]
            for node in nodes:
                if node['label'] == '客单价':
                    continue
                value.append(node['value'])
            for rate in rates:
                print(rate)
                if rate == '-':
                    value.append(None)
                    continue
                value.append(float(rate['rate'].replace('%', '')) / 100)
            ex_money = self.get_ex_money(start_day, cookie)
            value.append(ex_money)
            self._sql_server.save_message('贝德美.KS.交易总览', [tuple(value)])
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)

    def core_data_request(self, start_day, cookie):
        url = 'https://kssyt.e.kuaishou.com/rest/business/analysis/shop/conversion'
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': '96',
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': cookie,
            'Host': 'kssyt.e.kuaishou.com',
            'Origin': 'https://kssyt.e.kuaishou.com',
            'Pragma': 'no-cache',
            'Referer': 'https://kssyt.e.kuaishou.com/transaction/overview',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        data = {"module": "trade_conversion", "timeRange": "CUSTOMIZED_DAY", "from": start_day, "to": start_day}
        response = requests.post(url=url, headers=headers, json=data).json()
        return response

    # 商品分析
    def commodity_analysis_main(self, start_day, end_day, cookie):
        while True:
            if not start_day:
                start_day = self._sql_server.get_start_day('贝德美.KS.商品分析_日', '日期', '')
                print(start_day)
                if start_day == get_before_day(get_today()):
                    print('数据获取完毕')
                    return 0
                start_day = get_after_day(start_day)
            if not end_day:
                end_day = get_before_day(get_today())
            page = 1
            while True:
                response = self.commodity_analysis_request(start_day, cookie, page)
                print(response)
                datas = response['data']['data']
                if not datas:
                    break
                for data in datas:
                    print(data)
                    itemId = data['itemId']  # 商品id
                    sellerId = data['sellerId']  # 用户id
                    itemName = data['itemName']  # 商品名称
                    itemUrl = data['itemUrl']  # 商品连接
                    itemVisitUv = data['itemVisitUv']  # 商品访客数
                    itemPv = data['itemPv']  # 商品浏览量
                    orderSubmitUv = data['orderSubmitUv']  # 下单买家数
                    orderSubmitGoodsNum = data['orderSubmitGoodsNum']  # 下单件数
                    orderPaidGoodsNum = data['orderPaidGoodsNum']  # 支付件数
                    orderPaidUv = data['orderPaidUv']  # 支付买家数
                    orderSubmitAmt = data['orderSubmitAmt']  # 下单金额
                    afterOrderPaidUv = data['afterOrderPaidUv']  # 支付老买家数
                    firstOrderPaidUv = data['firstOrderPaidUv']  # 支付新买家数
                    try:
                        orderSubmitCvr = float(data['orderSubmitCvr'].replace('%', '')) / 100  # 下单转化率
                    except:
                        orderSubmitCvr = None
                    orderPaidAmt = data['orderPaidAmt']  # 支付金额
                    paidAmtPerGoods = data['paidAmtPerGoods']  # 件单价
                    if not paidAmtPerGoods:
                        paidAmtPerGoods = None
                    try:
                        orderPaidCvr = float(data['orderPaidCvr'].replace('%', '')) / 100  # 支付转化率
                    except:
                        orderPaidCvr = None
                    value = (
                        start_day, itemId, sellerId, itemName, itemUrl, itemVisitUv, itemPv, orderSubmitUv,
                        orderSubmitGoodsNum,
                        orderSubmitAmt, orderPaidUv,
                        orderPaidGoodsNum, orderPaidAmt, afterOrderPaidUv, firstOrderPaidUv, orderSubmitCvr,
                        orderPaidCvr, paidAmtPerGoods)
                    self._sql_server.save_message('贝德美.KS.商品分析_日', [value])
                page += 1
                time.sleep(1)
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)
            time.sleep(2)

    def commodity_analysis_request(self, start_day, cookie, page):
        url = 'https://kssyt.e.kuaishou.com/rest/business/analysis/commodity/customize/list'
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': '1592',
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': cookie,
            'Host': 'kssyt.e.kuaishou.com',
            'Origin': 'https://kssyt.e.kuaishou.com',
            'Pragma': 'no-cache',
            'Referer': 'https://kssyt.e.kuaishou.com/goods/details',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        data = {"total": 0, "pageNum": page, "pageSize": 10,
                "queryParam": {"module": "customize_commodity_list_v2", "timeRange": "CUSTOMIZED_DAY",
                               "from": start_day, "compareFrom": get_before_day(start_day), "customizeTargetList": [
                        {"label": "商品访客数", "key": "itemVisitUv", "chosen": True, "group": ""},
                        {"label": "商品浏览量", "key": "itemPv", "chosen": True, "group": ""},
                        {"label": "下单买家数", "key": "orderSubmitUv", "chosen": True, "group": ""},
                        {"label": "下单件数", "key": "orderSubmitGoodsNum", "chosen": True, "group": ""},
                        {"label": "下单金额", "key": "orderSubmitAmt", "chosen": False, "group": ""},
                        {"label": "支付老买家数", "key": "afterOrderPaidUv", "chosen": False, "group": ""},
                        {"label": "件单价", "key": "paidAmtPerGoods", "chosen": False, "group": ""},
                        {"label": "品退订单数", "key": "refundOrderNum", "chosen": False, "group": ""},
                        {"label": "商品品退率", "key": "itemRefundCvr", "chosen": False, "group": ""},
                        {"label": "商品评价数", "key": "itemCommentNum", "chosen": False, "group": ""},
                        {"label": "支付新买家数", "key": "firstOrderPaidUv", "chosen": False, "group": ""},
                        {"label": "支付买家数", "key": "orderPaidUv", "chosen": False, "group": ""},
                        {"label": "支付件数", "key": "orderPaidGoodsNum", "chosen": False, "group": ""},
                        {"label": "下单转化率", "key": "orderSubmitCvr", "chosen": False, "group": ""},
                        {"label": "商品差评数", "key": "itemBadCommentNum", "chosen": False, "group": ""},
                        {"label": "商品差评率", "key": "itemBadCommentCvr", "chosen": False, "group": ""},
                        {"label": "支付转化率", "key": "orderPaidCvr", "chosen": False, "group": ""},
                        {"label": "支付金额", "key": "orderPaidAmt", "chosen": False, "group": ""}], "itemType": 1},
                "orderByFields": {}}
        response = requests.post(url=url, headers=headers, json=data).json()
        return response

    # 推广趋势图
    def effect_kanban_main(self, cookie, start_day, end_day):
        while True:
            if not start_day:
                start_day = self._sql_server.get_start_day('贝德美.KS.快分销_效果看板_日', '日期', '')
                if start_day == get_before_day(get_today()):
                    print('数据获取完毕')
                    return 0
                start_day = get_after_day(start_day)
            if not end_day:
                end_day = get_before_day(get_today())
            response = self.effect_kanban_request(cookie, start_day)
            print(response)
            datas = response['dataList'][0]
            pv = datas['totalPv']
            uv = datas['totalUv']
            totalPayOrderNum = datas['totalPayOrderNum']  # 支付订单
            totalPayOrderAmount = round(datas['totalPayOrderAmount'] / 100, 2)  # 支付总金额
            totalCommission = round(datas['totalCommission'] / 100, 2)  # 预估佣金
            value = (start_day, pv, uv, totalPayOrderNum, totalPayOrderAmount, totalCommission)
            self._sql_server.save_message('贝德美.KS.快分销_效果看板_日', [value])
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)

    def effect_kanban_request(self, cookie, start_day):
        url = 'https://cps.kwaixiaodian.com/distribute/pc/seller/board/trend'
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cookie': cookie,
            'Host': 'cps.kwaixiaodian.com',
            'kpf': 'PC_WEB',
            'kpn': 'undefined',
            'ks-s-ctn': '025a550e-9592-40be-a068-9baa0906b611',
            'Pragma': 'no-cache',
            'Referer': 'https://cps.kwaixiaodian.com/pc/cps/data/effectBoard',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Trace-Id': '1.8369767669828067.739613208370.1648201038272.4',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        params = {
            'startTime': start_day.replace('-', ''),
            'endTime': start_day.replace('-', '')
        }
        response = requests.get(url=url, headers=headers, params=params).json()
        return response

    # 流量
    def commodity_flow_main(self, start_day, end_day, cookie):
        while True:
            if not start_day:
                start_day = self._sql_server.get_start_day('贝德美.KS.商品流量_日', '日期', '')
                if start_day == get_before_day(get_today()):
                    print('数据获取完毕')
                    return 0
                start_day = get_after_day(start_day)
            if not end_day:
                end_day = get_before_day(get_today())
            page = 1
            while True:
                response = self.commodity_flow_request(start_day, cookie, page)
                try:
                    datas = response['data']['data']
                except:
                    break
                if not datas:
                    break
                for data in datas:
                    itemId = data['itemId']  # id
                    itemName = data['itemName']  # 名称
                    itemType = data['itemType']  # 类型
                    sourcePage = data['sourcePage']  # 流量来源
                    itemShowCnt = data['itemShowCnt']  # 商品曝光次数
                    itemClkCnt = data['itemClkCnt']  # 商品访问次数
                    itemOrderCnt = data['itemOrderCnt']  # 商品下单量
                    itemPayCnt = data['itemPayCnt']  # 商品下支付量
                    itemPayAmt = round(data['itemPayAmt'] / 100, 2)  # 商品成交支付金额
                    value = (
                        start_day, itemId, itemName, itemType, sourcePage, itemShowCnt, itemClkCnt, itemOrderCnt,
                        itemPayCnt, itemPayAmt)
                    try:
                        self._sql_server.save_message('贝德美.KS.商品流量_日', [value])
                    except:
                        pass
                    for i in data['children']:
                        itemId = i['itemId']  # id
                        itemType = i['itemType']  # 类型
                        sourcePage = i['sourcePage']  # 流量来源
                        itemShowCnt = i['itemShowCnt']  # 商品曝光次数
                        itemClkCnt = i['itemClkCnt']  # 商品访问次数
                        itemOrderCnt = i['itemOrderCnt']  # 商品下单量
                        itemPayCnt = i['itemPayCnt']  # 商品下支付量
                        itemPayAmt = round(i['itemPayAmt'] / 100, 2)  # 商品成交支付金额
                        value = (
                            start_day, itemId, itemName, itemType, sourcePage, itemShowCnt, itemClkCnt,
                            itemOrderCnt,
                            itemPayCnt, itemPayAmt)
                        try:
                            self._sql_server.save_message('贝德美.KS.商品流量_日', [value])
                        except:
                            pass
                page += 1
                time.sleep(1)
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)
            time.sleep(2)

    def get_ex_money(self, start_day, cookie):
        url = 'https://kssyt.e.kuaishou.com/rest/business/analysis/aftersale/overview'
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': '103',
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': cookie,
            'Host': 'kssyt.e.kuaishou.com',
            'Origin': 'https://kssyt.e.kuaishou.com',
            'Pragma': 'no-cache',
            'Referer': 'https://kssyt.e.kuaishou.com/service/afterSales',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        data = {"timeRange": "CUSTOMIZED_DAY", "from": start_day, "to": start_day, "module": "aftermarket_overview_v2"}
        response = requests.post(url=url, headers=headers, json=data).json()
        print(response)
        for data in response['data']:
            if '退款金额' in data['label']:
                return data['value']
        return 0

    def commodity_flow_request(self, start_day, cookie, page):
        url = 'https://kssyt.e.kuaishou.com/rest/business/analysis/flow/v2/item/detail'
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': '136',
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': cookie,
            'Host': 'kssyt.e.kuaishou.com',
            'Origin': 'https://kssyt.e.kuaishou.com',
            'Pragma': 'no-cache',
            'Referer': 'https://kssyt.e.kuaishou.com/flow/goods',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        data = {"pageNum": page, "pageSize": 10, "queryParam": {"timeRange": "CUSTOMIZED_DAY", "from": start_day,
                                                                "compareFrom": get_before_day(start_day)}}
        response = requests.post(url=url, headers=headers, json=data).json()
        return response

    # 磁力金牛
    def magnetic_taurus_customer_compass_day_main(self, start_day, end_day, cookie):
        while True:
            if not start_day:
                start_day = self._sql_server.get_start_day('贝德美.KS.磁力金牛_客户罗盘_日', '日期', '')
                if start_day == get_before_day(get_today()):
                    print('数据获取完毕')
                    return 0
                start_day = get_after_day(start_day)
            if not end_day:
                end_day = get_before_day(get_today())
            response = self.get_acctids(cookie)
            acctids = []
            for acc in response['data']:
                acctids.append(acc['accountId'])
            page = 1
            while True:
                print(start_day)
                response = self.magnetic_taurus_customer_compass_day_request(start_day, acctids, page, cookie)
                cots = 0
                values = []
                try:
                    datas = response['data']
                    print(datas)
                except:
                    break
                if not datas:
                    break
                for data in datas:
                    accountId = data['accountId']
                    adDspCost = data['adDspCost']  # 花费
                    cots += adDspCost
                    # eventOrderPaiedPurchaseAmount = data['eventOrderPaiedPurchaseAmount']  # 花费
                    eventOrderPaiedPurchaseAmountPage = data['eventOrderPaiedPurchaseAmountPage']  # 交易
                    value = (start_day, accountId, adDspCost, eventOrderPaiedPurchaseAmountPage)
                    values.append(value)
                response = self.get_all_cots(start_day, acctids, page, cookie)
                all_adDspCost = response['data']['adDspCost']
                print(all_adDspCost, cots)
                if abs(cots - all_adDspCost) < 1:
                    self._sql_server.save_message('贝德美.KS.磁力金牛_客户罗盘_日', values)
                page += 1
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)
            time.sleep(2)

    def get_all_cots(self, start_day, acctids, page, cookie):
        url = 'https://luopan.e.kuaishou.com/rest/web/account/analyse/global/info'
        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'ACCOUNT-ID': '13377905',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': '200',
            'Content-Type': 'application/json',
            'Cookie': cookie,
            'Host': 'luopan.e.kuaishou.com',
            'Origin': 'https://luopan.e.kuaishou.com',
            'Pragma': 'no-cache',
            'Referer': 'https://luopan.e.kuaishou.com/analysis/account?__accountId__=13377905',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }

        data = {"timeAggrType": 1, "appIds": [1, 10], "productNames": [], "accountIds": acctids,
                "startTime": str(get_time_number(f'{start_day} 00:00:00')) + '000',
                "endTime": str(get_time_number(f'{start_day} 23:59:59')) + '999', "pageNo": page, "pageSize": 9,
                "sortField": "adDspCost", "sortType": "DESC",
                "dspCostType": 3}
        response = requests.post(url=url, headers=headers, json=data).json()
        print(response)
        return response

    def get_acctids(self, cookie):
        url = 'https://luopan.e.kuaishou.com/rest/web/account'
        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'ACCOUNT-ID': '13377905',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Cookie': cookie,
            'Host': 'luopan.e.kuaishou.com',
            'Origin': 'https://luopan.e.kuaishou.com',
            'Pragma': 'no-cache',
            'Referer': 'https://luopan.e.kuaishou.com/home?__accountId__=13377905',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        response = requests.post(url=url, headers=headers).json()
        return response

    def magnetic_taurus_customer_compass_day_request(self, start_day, acctids, page, cookie):
        url = 'https://luopan.e.kuaishou.com/rest/web/account/analyse/detail/info'
        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'ACCOUNT-ID': '13377905',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': '200',
            'Content-Type': 'application/json',
            'Cookie': cookie,
            'Host': 'luopan.e.kuaishou.com',
            'Origin': 'https://luopan.e.kuaishou.com',
            'Pragma': 'no-cache',
            'Referer': 'https://luopan.e.kuaishou.com/analysis/account?__accountId__=13377905',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        data = {"timeAggrType": 1, "appIds": [1, 10], "productNames": [], "accountIds": acctids,
                "startTime": str(get_time_number(f'{start_day} 00:00:00')) + '000',
                "endTime": str(get_time_number(f'{start_day} 23:59:59')) + '999', "pageNo": page, "pageSize": 9,
                "sortField": "adDspCost", "sortType": "DESC",
                "dspCostType": 3}
        response = requests.post(url=url, headers=headers, json=data).json()
        print(response)
        return response

    def account_flow_main(self, start_day, end_day, cookie):
        user_infos = self.get_acc_info()
        while True:
            for user_info in user_infos:
                accountId = user_info['accountId']
                url = 'https://niu.e.kuaishou.com/rest/esp/finance/account/flow?kuaishou.ad.esp_ph=47833b38c901043cc797f378ec30712c010e'
                headers = {
                    'Accept': 'application/json',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'ACCOUNT-ID': f'{accountId}',
                    'Cache-Control': 'no-cache',
                    'Connection': 'keep-alive',
                    'Content-Length': '103',
                    'Content-Type': 'application/json;charset=UTF-8',
                    'Cookie': cookie,
                    'Host': 'niu.e.kuaishou.com',
                    'Origin': 'https://niu.e.kuaishou.com',
                    'Pragma': 'no-cache',
                    'Referer': 'https://niu.e.kuaishou.com/finance/accountFlow?__accountId__=13378522',
                    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': "Windows",
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-origin',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
                    'x-nonce': '0.1580417693233589',
                    'x-timestamp': '1655793899652'
                }
                data = {"startDate": int(str(get_time_number(start_day)) + '000'),
                        "endDate": int(str(get_time_number(get_after_day(start_day))) + '999'),
                        "pageInfo": {"pageNum": 1, "pageSize": 10, "totalNum": 1}}
                # data = {"startDate":1655740800000,"endDate":1655827199999,"pageInfo":{"pageNum":1,"pageSize":10,"totalNum":1}}
                responses = requests.post(url=url, headers=headers, json=data).json()['data']['dailyCharges']['data']
                print(responses)
                for response in responses[1:]:
                    try:
                        dailyCharge = int(response['dailyCharge']) / 1000  # 总花费
                    except:
                        dailyCharge = None
                    try:
                        realCharged = int(response['realCharged']) / 1000  # 充值花费
                    except:
                        realCharged = None
                    try:
                        directRebateRealCharged = int(response['directRebateRealCharged']) / 1000  # 激励花费
                    except:
                        directRebateRealCharged = None
                    try:
                        commerceRealCharged = int(response['commerceRealCharged']) / 1000  # 电商花费
                    except:
                        commerceRealCharged = None
                    try:
                        dailyTransferIn = int(response['dailyTransferIn']) / 1000  # 转入
                    except:
                        dailyTransferIn = None
                    try:
                        realRecharged = int(response['realRecharged']) / 1000  # 充值转入
                    except:
                        realRecharged = None
                    commerceRealRecharged = int(response['commerceRealRecharged']) / 1000  # 电商转入
                    try:
                        directRebateRealRecharged = int(response['directRebateRealRecharged']) / 1000  # 激励转入
                    except:
                        directRebateRealRecharged = None
                    try:
                        realOut = int(response['realOut']) / 1000  # 转出
                    except:
                        realOut = None
                    try:
                        dailyTransferOut = int(response['dailyTransferOut']) / 1000  # 充值转出
                    except:
                        dailyTransferOut = None
                    try:
                        balance = int(response['balance']) / 1000  # 日终结余
                    except:
                        balance = None

                    value = (
                        start_day, 2677805207, accountId, dailyCharge, realCharged, None, directRebateRealCharged, commerceRealCharged,
                        dailyTransferIn, realRecharged, None, commerceRealRecharged, directRebateRealRecharged, realOut, dailyTransferOut,
                        None, None, None, balance)
                    try:
                        self._sql_server.save_message('贝德美.ks.磁力金牛_财务流水', [value])
                    except:
                        pass
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)
            time.sleep(3)

    def get_acc_info(self):
        url = 'https://id.kuaishou.com/pass/kuaishou/login/passToken'
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'ACCOUNT-ID': '13378522',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': '38',
            'Content-type': 'application/x-www-form-urlencoded',
            'Cookie': '_did=web_80548718192EC8CB; did=web_599b0f32736f0f6c4a768f2b5a79f9f0b640; userId=2677805207; userId=2677805207; passToken=ChNwYXNzcG9ydC5wYXNzLXRva2VuErABkLDuCi1HtOs5jjyDOC6HCabFMb6mlnlZWHGc1t57wfC1ELenpJxfGbhysthGyiAhbnVjcchcaEwo3f2ByXAkA9a8mjGU-Q7XLDbqCjmMjTrugftXaT1sCKUeTJevjw5Cm6gbzof61NHHq4ylaq7v_hjKa4saTUbkujrUzEVH3LHqrHDvU2cHbY0HLlJKWH6kno7OzksdyozOPBheUX6_BgdG9_SsxG7GamWmwbbLGYAaEoq67s3jCEBkvPPExxHmytZ0MCIgkf4x1UW-9aC6J6p9VmI_IVR1AODVi3e9Le2OIOns2EooBTAB',
            'Host': 'id.kuaishou.com',
            'Origin': 'https://niu.e.kuaishou.com',
            'Pragma': 'no-cache',
            'Referer': 'https://niu.e.kuaishou.com/',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        data = {
            'sid': 'kuaishou.ad.uc',
            'channelType': 'UNKNOWN'
        }
        response = requests.post(url=url, headers=headers, data=data).json()
        uc_st = response['kuaishou.ad.uc_st']
        userId = response['userId']
        print(uc_st)
        print(userId)
        new_url = f'https://uc.e.kuaishou.com/rest/web/account/list?kuaishou.ad.uc_st={uc_st}&userId={userId}'
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'ACCOUNT-ID': '13378522',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': '51',
            'Content-Type': 'application/json;charset=UTF-8',
            'Host': 'uc.e.kuaishou.com',
            'Origin': 'https://niu.e.kuaishou.com',
            'Pragma': 'no-cache',
            'Referer': 'https://niu.e.kuaishou.com/',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        data = {"appKey": "ad.adUkmConfig.adEsp", "clientType": "PC"}
        response = requests.post(url=new_url, headers=headers, json=data).json()
        for i in response['data']:
            accountId = i['accountId']
            accountName = i['accountName']
            value = (accountId, accountName)
            try:
                self._sql_server.save_message('贝德美.KS.磁力金牛_账号信息', [value])
            except:
                pass
        return response['data']

    def magnetic_taurus_professional_edition_group_report_main(self, start_day, end_day, cookie):
        while True:
            if not start_day:
                start_day = self._sql_server.get_start_day('贝德美.KS.磁力金牛_专业版_组报表', '日期', '')
                if start_day == get_before_day(get_today()):
                    print('数据获取完毕')
                    return 0
                start_day = get_after_day(start_day)
            if not end_day:
                end_day = get_before_day(get_today())
            user_datas = self.get_acc_info()
            for user_data in user_datas:
                print(user_data)
                page = 1
                goods = {}
                while True:
                    goods, res = self.get_goods_id(start_day, end_day, cookie, page, goods, user_data['accountId'])
                    if not res:
                        break
                    page += 1
                print(goods)
                if '移动' in user_data['accountName']:
                    continue
                self.magnetic_taurus_professional_edition_group_report_request(start_day, end_day, cookie,
                                                                               user_data['accountId'])
                with open(f'14.csv', 'r', errors='ignore') as f:
                    f_csv = csv.reader(f)
                    for row in f_csv:
                        if row[0].split(' ')[0] != start_day:
                            continue
                        row[0] = row[0].split(' ')[0]
                        # print(row[6])
                        if row[5] == '直播推广':
                            row.insert(3, None)
                        else:
                            try:
                                row.insert(3, goods[int(row[2])])
                            except:
                                row.insert(3, None)
                        value = []
                        for i in row:
                            if '%' in str(i):
                                try:
                                    i = float(i.replace('%', '')) / 100
                                except:
                                    i = 0
                            value.append(i)
                        value.insert(1, user_data['accountId'])
                        self._sql_server.save_message('贝德美.KS.磁力金牛_专业版_组报表', [tuple(value)])
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)
            time.sleep(2)

    # def check_zbb_cost(self):

    def get_goods_id(self, start_day, end_day, cookie, page, goods, accountId):
        url = 'https://niu.e.kuaishou.com/rest/esp/control-panel/report/search?kuaishou.ad.esp_ph=90340a0dcd59bf81b8a7496bcc5d5381283f'
        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'ACCOUNT-ID': f'{accountId}',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': '261',
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': cookie,
            'Host': 'niu.e.kuaishou.com',
            'Origin': 'https://niu.e.kuaishou.com',
            'Pragma': 'no-cache',
            'Referer': 'https://niu.e.kuaishou.com/manage?__accountId__=13378522&searchLevel=2',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'x-nonce': '0.9368399977354833',
            'x-timestamp': '1656924607703'
        }
        data = {
            "searchParam": {"promotionType": 2, "searchLevel": 2,
                            "startTime": str(get_time_number(start_day + " 00:00:00")) + "000",
                            "endTime": str(get_time_number(end_day + " 23:59:59")) + "999",
                            "status": {"campaign": {"value": []}}, "creativeListType": 1, "campaignIds": [],
                            "unitIds": [], "sceneOrientedTypes": [0], "name": ""},
            "pageInfo": {"pageNum": page, "pageSize": 10}}
        response = requests.post(url=url, headers=headers, json=data).json()
        print(response)
        datas = response['data']['data']
        print(datas)
        for data in datas:
            if data['unitId'] not in goods:
                goods[data['unitId']] = data['itemId']
        if not datas:
            return goods, 0
        return goods, 1

    def magnetic_taurus_professional_edition_group_report_request(self, start_day, end_day, cookie, accountId):
        url = 'https://niu.e.kuaishou.com/rest/esp/report/effect/download?kuaishou.ad.esp=undefined'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': '2353',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': cookie,
            'Host': 'niu.e.kuaishou.com',
            'Origin': 'https://niu.e.kuaishou.com',
            'Pragma': 'no-cache',
            'Referer': f'https://niu.e.kuaishou.com/report/basic?dataType=unit&__accountId__={accountId}',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        data = f'json=%7B%22startTime%22%3A{str(get_time_number(start_day + " 00:00:00")) + "000"}%2C%22endTime%22%3A{str(get_time_number(end_day + " 23:59:59")) + "999"}%2C%22groupType%22%3A1%2C%22viewType%22%3A3%2C%22selectors%22%3A%5B%7B%22name%22%3A%22promotionType%22%2C%22values%22%3A%5B2%5D%7D%2C%7B%22name%22%3A%22sceneOrientedType%22%2C%22values%22%3A%5B0%5D%7D%5D%2C%22selectedColumns%22%3A%5B%22reportDate%22%2C%22unitName%22%2C%22unitId%22%2C%22campaignName%22%2C%22campaignId%22%2C%22campaignTypeStr%22%2C%22ocpcActionTypeStr%22%2C%22creativeBuildTypeStr%22%2C%22speedTypeStr%22%2C%22costTotal%22%2C%22adShow%22%2C%22adShow1kCost%22%2C%22impression%22%2C%22photoClick%22%2C%22photoClickRatio%22%2C%22click%22%2C%22actionbarClick%22%2C%22actionbarClickCost%22%2C%22espClickRatio%22%2C%22actionRatio%22%2C%22adItemClickCount%22%2C%22espLivePlayedSeconds%22%2C%22playedThreeSeconds%22%2C%22play3sRatio%22%2C%22playedFiveSeconds%22%2C%22play5sRatio%22%2C%22playedEnd%22%2C%22playEndRatio%22%2C%22share%22%2C%22comment%22%2C%22likes%22%2C%22report%22%2C%22block%22%2C%22itemNegative%22%2C%22liveShare%22%2C%22liveComment%22%2C%22liveReward%22%2C%22effectivePlayCount%22%2C%22effectivePlayRatio%22%2C%22adLivePlayed1mNum%22%2C%22conversionNum%22%2C%22conversionCostEsp%22%2C%22gmv%22%2C%22t0GMV%22%2C%22t1GMV%22%2C%22t7GMV%22%2C%22t15GMV%22%2C%22t30GMV%22%2C%22roi%22%2C%22t0Roi%22%2C%22t1Roi%22%2C%22t7Roi%22%2C%22t15Roi%22%2C%22t30Roi%22%2C%22paiedOrder%22%2C%22orderRatio%22%2C%22t0OrderCnt%22%2C%22t0OrderCntCost%22%2C%22t0OrderCntRatio%22%2C%22t1OrderCnt%22%2C%22t7OrderCnt%22%2C%22t15OrderCnt%22%2C%22t30OrderCnt%22%2C%22merchantRecoFans%22%2C%22t1Retention%22%2C%22t7Retention%22%2C%22t15Retention%22%2C%22t30Retention%22%2C%22t1RetentionRatio%22%2C%22t7RetentionRatio%22%2C%22t15RetentionRatio%22%2C%22t30RetentionRatio%22%2C%22reservationSuccess%22%2C%22reservationCost%22%2C%22standardLivePlayedStarted%22%2C%22liveAudienceCost%22%2C%22liveEventGoodsView%22%2C%22goodsClickRatio%22%2C%22directAttrPlatNewBuyerCnt%22%2C%22t30AttrPlatTotalBuyerCnt%22%2C%22directAttrSellerNewBuyerCnt%22%2C%22t30AttrSellerTotalBuyerCnt%22%2C%22fansT0GMV%22%2C%22fansT1GMV%22%2C%22fansT7GMV%22%2C%22fansT15GMV%22%2C%22fansT30GMV%22%2C%22fansT0Roi%22%2C%22fansT1Roi%22%2C%22fansT7Roi%22%2C%22fansT15Roi%22%2C%22fansT30Roi%22%5D%2C%22pageInfo%22%3A%7B%22currentPage%22%3A1%2C%22pageSize%22%3A20%2C%22totalCount%22%3A203%7D%2C%22needSubDims%22%3Atrue%7D'
        response = requests.post(url=url, headers=headers, data=data).content
        print(response)
        with open('14.csv', 'wb') as w:
            w.write(response)
        w.close()


if __name__ == '__main__':
    co = ChromeOption()
    # ks = FastHand()
    cookie = co.ks_login()
    # # 快分销_效果看板
    # ks.effect_kanban_main(cookie, '2022-08-14', '2022-08-14')
    # # 快分销_效果明细
    # ks.effect_mingxi_main('2022-08-14', '2022-08-14', cookie)
    # co.__del__()

    # cookie = co.syt_login()
    # # 流量
    # ks.commodity_flow_main('', '', cookie)
    # # 商品分析_日
    # ks.commodity_analysis_main('', '', cookie)
    # # 交易总览
    # ks.core_data_main('', '', cookie)
    # co.__del__()

    # cookie = co.cllp_login()
    # # 磁力金牛
    # ks.magnetic_taurus_customer_compass_day_main('', '', cookie)
    # # 账户流水
    # ks.account_flow_main('2022-08-10', '2022-08-10', cookie)
    # # 磁力金牛_专业版_组报表
    # ks.magnetic_taurus_professional_edition_group_report_main('', '', cookie)