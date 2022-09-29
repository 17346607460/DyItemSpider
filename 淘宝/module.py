import time

import execjs
import requests
import xlrd
from unit import *
from Setting import *
from CurrencyModule import *


class Dbo:
    def __init__(self):
        self._sql_server = SqlServerConnect()
        self.shops = {'babycare旗舰店': '2275046294',
                      '袋鼠妈妈旗舰店': '1625276795', '可优比旗舰店': '820521956', '全棉时代官方旗舰店': '430490406', '贝亲官方旗舰店': '478829986',
                      '戴可思旗舰店': '4147285566', '红色小象旗舰店': '2707252427', '英氏婴童洗护旗舰店': '2200552342840',
                      '好孩子官方旗舰店': '379833581', '贝德美旗舰店': '2201196082363', '子初旗舰店': '1645898031', '启初旗舰店': '1705229452',
                      'aveeno官方旗舰店': '3782289210'}

    # bilibili_三连推广效果
    def bilibili_effect_of_three_consecutive_promotion_main(self, start_day, end_day, cookie):
        if not start_day:
            start_day = self._sql_server.get_start_day('贝德美.dbo.bilibili_三连推广效果', '日期', '')
            if start_day == get_before_day(get_today()):
                print('<贝德美.dbo.bilibili_三连推广效果> 今天数据已经抓取完毕')
                return 0
            start_day = start_day
        if not end_day:
            end_day = get_before_day(get_today())
        response = self._bilibili_effect_of_three_consecutive_promotion_request(start_day, end_day, cookie)
        datas = response['result']['rtb_data']
        values = {}
        dates = datas['xaxis']
        for index, date in enumerate(dates):
            values[date.split(' ')[0]] = []
            costs = datas['cost']  # 花费
            show_count = datas['show_count']  # 展示量
            click_count = datas['click_count']  # 点击量
            fans_increase_count = datas['fans_increase_count']  # 张粉数
            values[date.split(' ')[0]].append((date.split(' ')[0], 975433, '贝德美旗舰店-带货起飞', costs[index],
                                               show_count[index], click_count[index], fans_increase_count[index]))
        for value in values:
            self._sql_server.save_message('贝德美.dbo.bilibili_三连推广效果', values[value])

    def _bilibili_effect_of_three_consecutive_promotion_request(self, start_day, end_day, cookie):
        url = 'https://cm.bilibili.com/ad_account/api/web_api/v1/dashboard/data'
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'cookie': cookie,
            'origin': 'https://e.bilibili.com',
            'pragma': 'no-cache',
            'referer': 'https://e.bilibili.com/',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        params = {
            'account_id': '975433',
            'date_begin': f'{get_time_number(start_day)}000',
            'date_end': f'{get_time_number(end_day)}999',
            'system_type': '7'
        }
        response = requests.get(url=url, headers=headers, params=params).json()
        return response

    # Unidesk_报表_效果投放_日
    def unidesk_report_effect_delivery_day_main(self, cookie, start_day, end_day):
        if not start_day:
            if self._sql_server.get_start_day('Unidesk_报表_效果投放_日', '日期', '') == get_before_day(get_today()):
                print('<Unidesk_报表_效果投放_日>数据获取完毕')
                return 0
        sql = 'delete FROM 贝德美.dbo.Unidesk_报表_效果投放_日 where 转化周期<30'
        self._sql_server.check_message(sql, 2)
        while True:
            if not start_day:
                start_day = self._sql_server.get_start_day('Unidesk_报表_效果投放_日', '日期', '')
                if start_day == get_before_day(get_today()):
                    print('<Unidesk_报表_效果投放_日>数据获取完毕')
                    return 0
                start_day = get_after_day(start_day)
            if not end_day:
                end_day = get_before_day(get_today())
            advertiserIds = [45401, 45409, 45410, 45411, 45412, 78527, 78528, 79036, 79037, 79038]
            for advertiserId in advertiserIds:
                while True:
                    response = self._unidesk_report_effect_delivery_day_request(cookie, start_day, advertiserId)
                    if response['data']:
                        break
                    time.sleep(5)
                    print(advertiserId)
                try:
                    cost = response['data']['summary']['cost'] / 100  # 消耗
                except:
                    cost = None
                advertiserName = response['data']['summary']['advertiserName']  # 投放账户名称
                if not advertiserName:
                    continue
                adPv = response['data']['summary']['adPv']  # 展现量
                ecpm = response['data']['summary']['ecpm'] / 100  # 千次展现成本
                click = response['data']['summary']['click']  # 点击量
                adCtr = response['data']['summary']['adCtr']  # 点击率
                ecpc = response['data']['summary']['ecpc']  # 点击单价
                pageArrive = response['data']['summary']['pageArrive']  # 页面到达量
                pageArriveUv = response['data']['summary']['pageArriveUv']  # 页面到uv
                convert = response['data']['summary']['convert']  # 转化数
                convertCost = response['data']['summary']['convertCost'] / 100  # 转化成本
                takeOrderVolume = response['data']['summary']['takeOrderVolume']  # 拍下订单量
                takeOrderAmount = response['data']['summary']['takeOrderAmount'] / 100  # 拍下订单金额
                transactionVolume = response['data']['summary']['transactionVolume']  # 成交订单量
                transactionAmount = response['data']['summary']['transactionAmount'] / 100  # 成交订金额
                favoriteStores = response['data']['summary']['favoriteStores']  # 收藏店铺量
                favoriteBabyVolume = response['data']['summary']['favoriteBabyVolume']  # 收藏宝贝量
                addCartVolume = response['data']['summary']['addCartVolume']  # 添加购物车量
                returnOnInvestment = response['data']['summary']['returnOnInvestment']  # 投资回报率
                aidPv = response['data']['summary']['aidPv']  # aid展现量
                aidClick = response['data']['summary']['aidClick']  # aid点击量
                aidCtr = response['data']['summary']['aidCtr']  # aid点击率
                likeNums = response['data']['summary']['likeNums']  # 点赞数
                shareNums = response['data']['summary']['shareNums']  # 分享数
                playNums = response['data']['summary']['playNums']  # 播放数
                effectPlayNums = response['data']['summary']['effectPlayNums']  # 有效播放数
                effectPlayRate = response['data']['summary']['effectPlayRate']  # 有效播放率
                playNums50 = response['data']['summary']['playNums50']  # 50%进度播放数
                playNums25 = response['data']['summary']['playNums25']  # 25%进度播放数
                effectPlayCost = response['data']['summary']['effectPlayCost']  # 有效播放成本
                playNums75 = response['data']['summary']['playNums75']  # 75%进度播放数
                finishPlayRate = response['data']['summary']['finishPlayRate']  # 播完率
                playNums99 = response['data']['summary']['playNums99']  # 99%进度播放数
                averagePlayTime = response['data']['summary']['averagePlayTime']  # 平均单次播放时长
                wifiPlayPercent = response['data']['summary']['wifiPlayPercent']  # wifi播放占比
                playOverNums = response['data']['summary']['playOverNums']  # 播完数
                convertRate = response['data']['summary']['convertRate']  # 转化率
                collectionCost = response['data']['summary']['collectionCost'] / 100  # 收藏成本
                visitCost = response['data']['summary']['visitCost'] / 100  # 回访成本
                visitTime = response['data']['summary']['visitTime']  # 深度访问时长
                ysddje = 0.0  # 预售订单金额
                alipayCost = response['data']['summary']['alipayCost'] / 100  # 订单成本
                visitPageVolume = response['data']['summary']['visitPageVolume']  # 深度访问页面数
                buyCost = response['data']['summary']['buyCost'] / 100  # 加购成本
                searchVolume = response['data']['summary']['searchVolume']  # 回搜量
                visitVolume = response['data']['summary']['visitVolume']  # 回访量
                searchCost = response['data']['summary']['searchCost'] / 100  # 回搜成本
                depthStoreVolume = response['data']['summary']['depthStoreVolume']  # 深度进店量
                ysddl = 0  # 预售订单量
                week = int((get_time_number(get_today()) - get_time_number(start_day)) / (60 * 60 * 24))
                if week > 30:
                    week = 30
                value = (
                    week, start_day, advertiserId, advertiserName, cost, adPv, ecpm, click, adCtr, ecpc, pageArrive,
                    pageArriveUv,
                    convert, convertCost, takeOrderVolume, takeOrderAmount, transactionVolume, transactionAmount,
                    favoriteStores, favoriteBabyVolume, addCartVolume, returnOnInvestment, aidPv, aidClick, aidCtr,
                    likeNums, shareNums, playNums, effectPlayNums, effectPlayRate, playNums50, playNums25,
                    effectPlayCost,
                    playNums75, finishPlayRate, playNums99, averagePlayTime, wifiPlayPercent, playOverNums, convertRate,
                    collectionCost, visitCost, visitTime, ysddje, alipayCost, visitPageVolume, buyCost, searchVolume,
                    visitVolume, searchCost, depthStoreVolume, ysddl)
                self._sql_server.save_message('Unidesk_报表_效果投放_日', [value])
                time.sleep(1)
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)
            time.sleep(1)

    def _unidesk_report_effect_delivery_day_request(self, cookie, start_day, advertiserId):
        url = 'https://unidesk.taobao.com/api/direct/report/account/summary'
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': cookie,
            'referer': 'https://unidesk.taobao.com/direct/index',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'x-xsrf-token': cookie.split('XSRF-TOKEN=')[1].split(';')[0]
        }
        params = {
            'r': 'mx_1639',
            'effect': '30',
            'effectType': 'click',
            'ef': 'logDate',
            'directMediaId': '103',
            'startTime': start_day,
            'endTime': start_day,
            'bizType': '37',
            'advertiserId': f'{advertiserId}',
            'timeStr': '1650941504362',
            'dynamicToken': '432200408424484196428388',
            'bizCode': 'uniDeskRtaAdv'
        }
        response = requests.get(url=url, headers=headers, params=params)
        print(response.text)
        return response.json()

    # 二级流量来源_无线端_单品
    def secondary_flow_source_wireless_terminal_single_product_main(self, start_day, cookie, end_day):
        while True:
            if not start_day:
                start_day = self._sql_server.get_start_day('贝德美.dbo.二级流量来源_无线端_单品', '日期', '')
                if start_day == get_before_day(get_today()):
                    print('<贝德美.dbo.二级流量来源_无线端_单品>数据获取完毕')
                    return 0
                start_day = get_after_day(start_day)
            if not end_day:
                end_day = get_before_day(get_today())
            item_list = self._get_item_list(start_day, cookie)
            for item in item_list:
                response = self._secondary_flow_source_wireless_terminal_single_product_request(cookie, start_day, item)
                datas = response['data']
                if datas:
                    for data in datas:
                        pageName = data['pageName']['value']  # 来源
                        if pageName == '0':
                            continue
                        uv = data['uv']['value']  # 访客数
                        pv = data['pv']['value']  # 浏览量
                        payAmt = data['payAmt']['value']  # 支付金额
                        pv_ratio = data['pv']['ratio']  # 浏览量占比
                        jpSelfUv = data['jpSelfUv']['value']  # 店内跳转人数
                        jpUv = data['jpUv']['value']  # 跳出本店人数
                        cltCnt = data['cltCnt']['value']  # 收藏人数
                        cartByrCnt = data['cartByrCnt']['value']  # 加购人数
                        crtByrCnt = data['crtByrCnt']['value']  # 下单买家数
                        crtRate = data['crtRate']['value']  # 下单转化率
                        payItmCnt = data['payItmCnt']['value']  # 支付件数
                        payByrCnt = data['payByrCnt']['value']  # 支付买家数
                        payRate = data['payRate']['value']  # 支付转化率
                        directPayByrCnt = data['directPayByrCnt']['value']  # 直接支付买家数
                        cltItmPayByrCnt = data['cltItmPayByrCnt']['value']  # 收藏商品-支付买家数
                        fansPayByrCnt = data['fansPayByrCnt']['value']  # 粉丝支付买家数
                        ordItmPayByrCnt = data['ordItmPayByrCnt']['value']  # 加购商品-支付买家数
                        tup1 = (
                            start_day, item, pageName, '汇总', uv, pv, '%.2f' % payAmt, '%.4f' % pv_ratio, jpSelfUv, jpUv,
                            cltCnt,
                            cartByrCnt, crtByrCnt, '%.4f' % crtRate, payItmCnt, payByrCnt, '%.4f' % payRate,
                            directPayByrCnt,
                            cltItmPayByrCnt, fansPayByrCnt, ordItmPayByrCnt)
                        self._sql_server.save_message('贝德美.dbo.二级流量来源_无线端_单品', [tup1])
                        if 'children' in data:
                            for y in data['children']:
                                pageName2 = y['pageName']['value']  # 来源
                                uv = y['uv']['value']  # 访客数
                                pv = y['pv']['value']  # 浏-览量
                                payAmt = y['payAmt']['value']  # 支付金额
                                pv_ratio = y['pv']['ratio']  # 浏览量占比
                                jpSelfUv = y['jpSelfUv']['value']  # 店内跳转人数
                                jpUv = y['jpUv']['value']  # 跳出本店人数
                                cltCnt = y['cltCnt']['value']  # 收藏人数
                                cartByrCnt = y['cartByrCnt']['value']  # 加购人数
                                crtByrCnt = y['crtByrCnt']['value']  # 下单买家数
                                crtRate = y['crtRate']['value']  # 下单转化率
                                payItmCnt = y['payItmCnt']['value']  # 支付件数
                                payByrCnt = y['payByrCnt']['value']  # 支付买家数
                                payRate = y['payRate']['value']  # 支付转化率
                                directPayByrCnt = y['directPayByrCnt']['value']  # 直接支付买家数
                                cltItmPayByrCnt = y['cltItmPayByrCnt']['value']  # 收藏商品-支付买家数
                                fansPayByrCnt = y['fansPayByrCnt']['value']  # 粉丝支付买家数
                                ordItmPayByrCnt = y['ordItmPayByrCnt']['value']  # 加购商品-支付买家数
                                tup1 = (
                                    start_day, item, pageName, pageName2, uv, pv, '%.2f' % payAmt, '%.4f' % pv_ratio,
                                    jpSelfUv,
                                    jpUv, cltCnt,
                                    cartByrCnt, crtByrCnt, '%.4f' % crtRate, payItmCnt, payByrCnt, '%.4f' % payRate,
                                    directPayByrCnt,
                                    cltItmPayByrCnt, fansPayByrCnt, ordItmPayByrCnt)
                                self._sql_server.save_message('贝德美.dbo.二级流量来源_无线端_单品', [tup1])
                time.sleep(5)
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)
            time.sleep(5)

    def _get_item_list(self, start_day, cookie):
        url = 'https://sycm.taobao.com/cc/cockpit/marcro/item/top.json'
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': cookie,
            'onetrace-card-id': 'sycm-flow-shop-source-construction.sycm-flow-shop-source-construction-flow-source-self-table.sycm-flow-shop-source-construction-list',
            'pragma': 'no-cache',
            'referer': 'https://sycm.taobao.com/flow/monitor/shopsource/construction?belong=all&dateRange=2022-04-11%7C2022-04-11&dateType=day&device=2&rivalUser1Id=&spm=a21ag.11910098.LeftMenu.d603.327c50a5kzZC3u',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sycm-query': 'dateType=day',
            'sycm-referer': '/flow/monitor/shopsource/construction',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        params = {
            'dateRange': f'{start_day}|{start_day}',
            'dateType': 'day',
            'pageSize': '15',
            'page': '1',
            'order': 'desc',
            'orderBy': 'itmUv',
            'keyword': '',
            'follow': 'false',
            'cateId': '',
            'cateLevel': '',
            'guideCateId': '',
            'device': '0',
            'indexCode': 'itmUv%2CitemCartCnt%2CpayItmCnt',
            '_': '1595837622060',
            'token': '915af1c78'
        }
        response = requests.get(url=url, headers=headers, params=params).json()
        item_list = []
        for data in response['data']['data']:
            item_list.append(data['item']['itemId'])
        item_list = list(
            set(item_list + ['598181988781', '611012660524', '661145734413', '669703761476', '679771374228']))
        return item_list

    def _secondary_flow_source_wireless_terminal_single_product_request(self, cookie, start_day, item):
        url = 'https://sycm.taobao.com/flow/v4/item/source.json'
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': cookie,
            'onetrace-card-id': 'sycm-flow-shop-source-construction.sycm-flow-shop-source-construction-flow-source-self-table.sycm-flow-shop-source-construction-list',
            'pragma': 'no-cache',
            'referer': 'https://sycm.taobao.com/flow/monitor/shopsource/construction?belong=all&dateRange=2022-04-11%7C2022-04-11&dateType=day&device=2&rivalUser1Id=&spm=a21ag.11910098.LeftMenu.d603.327c50a5kzZC3u',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sycm-query': 'dateType=day',
            'sycm-referer': '/flow/monitor/shopsource/construction',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        params = {
            'belong': 'all',
            'dateRange': f'{start_day}|{start_day}',
            'dateType': 'day',
            'order': 'desc',
            'orderBy': 'uv',
            'device': '2',
            'itemId': f'{item}',
            'indexCode': 'uv%2CcrtByrCnt%2CcrtRate',
            '_': '1580726248201',
            'token': '56f52fdc3'
        }
        response = requests.get(url=url, headers=headers, params=params).json()
        return response

    # 三级流量来源_无线端_单品
    def third_stage_flow_source_wireless_terminal_single_product_main(self, start_day, end_day, cookie):
        while True:
            if not start_day:
                start_day = self._sql_server.get_start_day('贝德美.dbo.三级流量来源_无线端_单品', '日期', '')
                if start_day == get_before_day(get_today()):
                    print('<贝德美.dbo.三级流量来源_无线端_单品>数据获取完毕')
                    return 0
                start_day = get_after_day(start_day)
            if not end_day:
                end_day = get_before_day(get_today())
            item_list = self._get_item_list(start_day, cookie)
            item_list = list(
                set(item_list + ['625769583872', '598181988781', '611012660524', '642216586762', '661145734413',
                                 '669703761476', '679771374228']))
            for itemid in item_list:
                pages = \
                self._get_third_stage_flow_source_wireless_terminal_single_product_page(cookie, start_day, itemid)[
                    'data']['recordCount']
                if pages % 10:
                    pages = int(pages / 10) + 1
                elif pages % 10 == 0:
                    pages = int(pages / 10)
                for page in range(pages):
                    response = self._third_stage_flow_source_wireless_terminal_single_product_request(cookie, start_day,
                                                                                                      itemid, page + 1)
                    datas = response['data']['data']
                    for data in datas:
                        pageName = data['pageName']['value'] if '&mdash;' not in data['pageName']['value'] else \
                        data['pageName'][
                            'value'].replace('&mdash;', '')  # 来源
                        uv = data['uv']['value']  # 访客数
                        pv = data['pv']['value']  # 浏览量
                        pv_ratio = data['pv']['ratio']  # 浏览量占比
                        jpSelfUv = data['jpSelfUv']['value']  # 店内跳转人数
                        jpUv = data['jpUv']['value']  # 跳出本店人数
                        cltCnt = data['cltCnt']['value']  # 收藏人数
                        cartByrCnt = data['cartByrCnt']['value']  # 加购人数
                        crtByrCnt = data['crtByrCnt']['value']  # 下单买家数
                        crtRate = data['crtRate']['value']  # 下单转化率
                        payItmCnt = data['payItmCnt']['value']  # 支付件数
                        payByrCnt = data['payByrCnt']['value']  # 支付买家数
                        payRate = data['payRate']['value']  # 支付转化率
                        directPayByrCnt = data['directPayByrCnt']['value']  # 直接支付买家数
                        fansPayByrCnt = data['fansPayByrCnt']['value']  # 粉丝支付买家数
                        cltItmPayByrCnt = data['cltItmPayByrCnt']['value']  # 收藏商品-支付买家数
                        ordItmPayByrCnt = data['ordItmPayByrCnt']['value']  # 加购商品-支付买家数

                        tup1 = (
                            start_day, itemid, '手淘搜索', pageName, uv, pv, '%.4f' % pv_ratio, jpSelfUv, jpUv, cltCnt,
                            cartByrCnt,
                            crtByrCnt, '%.4f' % crtRate, payItmCnt, payByrCnt, '%.4f' % payRate, directPayByrCnt,
                            cltItmPayByrCnt, fansPayByrCnt, ordItmPayByrCnt)
                        self._sql_server.save_message('贝德美.dbo.三级流量来源_无线端_单品', [tup1])
                time.sleep(10)
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)
            time.sleep(5)

    def _get_third_stage_flow_source_wireless_terminal_single_product_page(self, cookie, start_day, itemId):
        url = 'https://sycm.taobao.com/flow/v3/new/item/source/detail.json'
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': cookie,
            'onetrace-card-id': 'sycm-flow-shop-source-construction.sycm-flow-shop-source-construction-flow-source-self-table.sycm-flow-shop-source-construction-list',
            'pragma': 'no-cache',
            'referer': 'https://sycm.taobao.com/flow/monitor/shopsource/construction?belong=all&dateRange=2022-04-11%7C2022-04-11&dateType=day&device=2&rivalUser1Id=&spm=a21ag.11910098.LeftMenu.d603.327c50a5kzZC3u',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sycm-query': 'dateType=day',
            'sycm-referer': '/flow/monitor/shopsource/construction',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        params = {
            'dateRange': f'{start_day}|{start_day}',
            'dateType': 'day',
            'pageSize': '10',
            'page': '1',
            'order': 'desc',
            'orderBy': 'uv',
            'itemId': f'{itemId}',
            'device': '2',
            'pageId': '23.s1150',
            'pPageId': '23',
            'pageLevel': '2',
            'childPageType': 'se_keyword',
            'belong': 'all',
            'indexCode': 'uv%2CcrtByrCnt%2CcrtRate',
            '_': '1580730250009',
            'token': '56f52fdc3'
        }
        response = requests.get(url=url, headers=headers, params=params).json()
        return response

    def _third_stage_flow_source_wireless_terminal_single_product_request(self, cookie, start_day, itemId, page):
        url = 'https://sycm.taobao.com/flow/v3/new/item/source/detail.json'
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': cookie,
            'onetrace-card-id': 'sycm-flow-shop-source-construction.sycm-flow-shop-source-construction-flow-source-self-table.sycm-flow-shop-source-construction-list',
            'pragma': 'no-cache',
            'referer': 'https://sycm.taobao.com/flow/monitor/shopsource/construction?belong=all&dateRange=2022-04-11%7C2022-04-11&dateType=day&device=2&rivalUser1Id=&spm=a21ag.11910098.LeftMenu.d603.327c50a5kzZC3u',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sycm-query': 'dateType=day',
            'sycm-referer': '/flow/monitor/shopsource/construction',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        params = {
            'dateRange': f'{start_day}|{start_day}',
            'dateType': 'day',
            'pageSize': '10',
            'page': f'{page}',
            'order': 'desc',
            'orderBy': 'uv',
            'itemId': f'{itemId}',
            'device': '2',
            'pageId': '23.s1150',
            'pPageId': '23',
            'pageLevel': '2',
            'childPageType': 'se_keyword',
            'belong': 'all',
            'indexCode': 'uv%2CcrtByrCnt%2CcrtRate',
            '_': '1580730250009',
            'token': '56f52fdc3'
        }
        response = requests.get(url=url, headers=headers, params=params).json()
        return response

    # 三级流量来源_无线端_店铺
    def third_stage_flow_source_wireless_terminal_shop_main(self, start_day, end_day, cookie):
        while True:
            if not start_day:
                start_day = self._sql_server.get_start_day('贝德美.dbo.三级流量来源_无线端_店铺', '日期', '')
                if start_day == get_before_day(get_today()):
                    print('<贝德美.dbo.三级流量来源_无线端_店铺>数据获取完毕')
                    return 0
                start_day = get_after_day(start_day)
            if not end_day:
                end_day = get_before_day(get_today())
            response = self._get_third_stage_flow_source_wireless_terminal_shop_page(start_day, cookie)
            pages = response['data']['recordCount']
            if pages % 10:
                pages = int(pages / 10) + 1
            elif pages % 10 == 0:
                pages = int(pages / 10)
            for page in range(pages):
                response = self._third_stage_flow_source_wireless_terminal_shop_request(start_day, cookie, page + 1)
                datas = response['data']['data']
                for data in datas:
                    pageName = data['pageName']['value']  # 来源
                    uv = data['uv']['value']  # 访客数
                    payRate = data['payRate']['value'] if data['payRate']['value'] != None else 0  # 支付转化率
                    payAmt = data['payAmt']['value'] if data['payAmt']['value'] != None else 0  # 支付金额
                    payPct = data['payPct']['value'] if data['payPct']['value'] != None else 0  # 客单价
                    crtVldAmt = data['crtVldAmt']['value'] if data['crtVldAmt']['value'] != None else 0  # 下单金额
                    crtByrCnt = data['crtByrCnt']['value']  # 下单买家数
                    crtRate = data['crtRate']['value'] if data['crtRate']['value'] != None else 0  # 下单转化率
                    payByrCnt = data['payByrCnt']['value']  # 支付买家数
                    uvValue = data['uvValue']['value'] if data['uvValue']['value'] != None else 0  # uv价值
                    shopCltByrCnt = data['shopCltByrCnt']['value']  # 关注店铺买家数
                    cltItmCnt = data['cltItmCnt']['value']  # 收藏商品买家数
                    cartByrCnt = data['cartByrCnt']['value']  # 加购人数
                    newUv = data['newUv']['value']  # 新访客
                    directPayByrCnt = data['directPayByrCnt']['value']  # 直接支付买家数
                    cltItmPayByrCnt = data['cltItmPayByrCnt']['value']  # 收藏商品-支付买家数
                    fansPayByrCnt = data['fansPayByrCnt']['value']  # 粉丝支付买家数
                    ordItmPayByrCnt = data['ordItmPayByrCnt']['value']  # 加购商品-支付买家数

                    value = (
                        start_day, '手淘搜索', pageName, uv, '%.4f' % payRate, '%.2f' % payAmt, '%.2f' % payPct,
                        '%.2f' % crtVldAmt,
                        crtByrCnt, '%.4f' % crtRate, payByrCnt, '%.2f' % uvValue, shopCltByrCnt, cltItmCnt, cartByrCnt,
                        newUv,
                        directPayByrCnt, cltItmPayByrCnt, fansPayByrCnt, ordItmPayByrCnt)
                    self._sql_server.save_message('贝德美.dbo.三级流量来源_无线端_店铺', [value])
                time.sleep(1)
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)
            time.sleep(5)

    def _get_third_stage_flow_source_wireless_terminal_shop_page(self, start_day, cookie):
        url = 'https://sycm.taobao.com/flow/v3/shop/source/detail.json'
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': cookie,
            'onetrace-card-id': 'sycm-flow-shop-source-construction.sycm-flow-shop-source-construction-flow-source-self-table.sycm-flow-shop-source-construction-list',
            'pragma': 'no-cache',
            'referer': 'https://sycm.taobao.com/flow/monitor/shopsource/construction?belong=all&dateRange=2022-04-11%7C2022-04-11&dateType=day&device=2&rivalUser1Id=&spm=a21ag.11910098.LeftMenu.d603.327c50a5kzZC3u',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sycm-query': 'dateType=day',
            'sycm-referer': '/flow/monitor/shopsource/construction',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        params = {
            'dateRange': f'{start_day}|{start_day}',
            'dateType': 'day',
            'pageSize': '10',
            'page': '1',
            'order': 'desc',
            'orderBy': 'uv',
            'device': '2',
            'belong': 'all',
            'pageId': '23.s1150',
            'pPageId': '23',
            'childPageType': 'se_keyword',
            'indexCode': 'uv%2CcrtByrCnt%2CcrtRate',
            '_': '1580881999895',
            'token': 'e1b8ea6cb'
        }
        response = requests.get(url=url, headers=headers, params=params)
        print(response.text)
        return response.json()

    def _third_stage_flow_source_wireless_terminal_shop_request(self, start_day, cookie, page):
        url = 'https://sycm.taobao.com/flow/v3/shop/source/detail.json'
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': cookie,
            'onetrace-card-id': 'sycm-flow-shop-source-construction.sycm-flow-shop-source-construction-flow-source-self-table.sycm-flow-shop-source-construction-list',
            'pragma': 'no-cache',
            'referer': 'https://sycm.taobao.com/flow/monitor/shopsource/construction?belong=all&dateRange=2022-04-11%7C2022-04-11&dateType=day&device=2&rivalUser1Id=&spm=a21ag.11910098.LeftMenu.d603.327c50a5kzZC3u',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sycm-query': 'dateType=day',
            'sycm-referer': '/flow/monitor/shopsource/construction',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        params = {
            'dateRange': f'{start_day}|{start_day}',
            'dateType': 'day',
            'pageSize': '10',
            'page': f'{page}',
            'order': 'desc',
            'orderBy': 'uv',
            'device': '2',
            'belong': 'all',
            'pageId': '23.s1150',
            'pPageId': '23',
            'childPageType': 'se_keyword',
            'indexCode': 'uv%2CcrtByrCnt%2CcrtRate',
            '_': '1580881999895',
            'token': 'e1b8ea6cb'
        }
        response = requests.get(url=url, headers=headers, params=params).json()
        return response

    # 取数_店铺整体_日
    def access_overall_store_day_main(self, start_day, cookie, shop_name, table):
        if not start_day:
            start_day = self._sql_server.get_start_day(table, '日期', '')
            if start_day == get_before_day(get_today()):
                print('<取数_店铺整体_日>数据获取完毕')
                return 0
            start_day = get_after_day(start_day)
        self._shop_judgment(shop_name, cookie)
        response = self._access_overall_store_day_main(cookie, shop_name)
        datas = response['data']['data']
        for data in datas:
            for x in range(len(data)):
                if '%' in data[x]:
                    data[x] = '%.4f' % (float(data[x].replace('%', '')) / 100)
                elif ',' in data[x]:
                    data[x] = data[x].replace(',', '')
            if shop_name == 'bodormebaby旗舰店':
                self._sql_server.save_message('贝德美.BODORME.取数_店铺整体_日', [tuple(data)])
            if shop_name == '贝德美旗舰店':
                self._sql_server.save_message('贝德美.dbo.取数_店铺整体_日', [tuple(data)])
            if start_day == data[0]:
                break

    # 店铺判断
    def _shop_judgment(self, shop_name, cookie):
        url = 'https://sycm.taobao.com/custom/menu/getPersonalView.json?token=2decb18fa'
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': cookie,
            'pragma': 'no-cache',
            'referer': 'https://sycm.taobao.com/portal/home.htm?activeKey=diagnosis&dateRange=2022-04-10%7C2022-04-10&dateType=recent1&spm=a217wi.openworkbeachtb_web',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        response = requests.get(url=url, headers=headers).json()
        print(response['data']['mainUserName'], shop_name)
        if response['data']['mainUserName'] != shop_name:
            raise '店铺不正确'

    def _access_overall_store_day_main(self, cookie, shop_name):
        if shop_name == '贝德美旗舰店':
            url = 'https://sycm.taobao.com/adm/v2/execute/previewById.json?id=1459607&reportType=1&_=1590135769514&token=815e777d7'
        if shop_name == 'bodormebaby旗舰店':
            url = 'https://sycm.taobao.com/adm/v2/execute/previewById.json?id=2391634&reportType=1&_=1649666650220&token=2decb18fa'
        headers = {
            'cookie': cookie,
            'referer': 'https://sycm.taobao.com/adm/v2/my?spm=a21ag.10575379.LeftMenu.d376.6eb5410cYs6LJL',
            'transit-id': 'HVgm4Zah54r8rf4mRLdV3xGJmuPsWc1hw6NRu/4wl7QPUpz55s4XadGRPTLS+BauKeS6lC4/rteOv7ULH+KdCEbfA2T/wmuJ7O888/Pt+oTtJkL06X6krUuKz0VmKE5OA2v51j1aTyY70bs1rJTlqVhK9HCftZMYNe/RsxEBUeU=',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4039.400'
        }
        response = requests.get(url, headers=headers).json()
        return response

    # 贝德美.dbo.二级流量来源_商品效果_日
    def source_of_secondary_flow_commodities_commodity_effect_day_main(self, start_day, end_day, cookie, table,
                                                                       shop_name):
        while True:
            if not start_day:
                start_day = self._sql_server.get_start_day(table, '日期', '')
                if start_day == get_before_day(get_today()):
                    print('<贝德美.dbo.二级流量来源_商品效果_日>数据获取完毕')
                    return 0
                start_day = get_after_day(start_day)
            if not end_day:
                end_day = get_before_day(get_today())
            self._shop_judgment(shop_name, cookie)
            page_need = {'手淘搜索': ['23.s1150', '23', 'se_keyword'], '手淘淘宝直播': ['23.s2594', '23', ''],
                         '淘内免费其他': ['23.11', '23', 'url'], '直通车': ['22.2', '22', 'se_keyword'],
                         '万象台': ['22.17', '22', ''],
                         '淘宝客': ['22.1', '22', ''], '引力魔方': ['22.19', '22', '']}
            for item in page_need:
                page = 1
                while True:
                    response = self._source_of_secondary_flow_commodities_commodity_effect_day_request(start_day,
                                                                                                       cookie,
                                                                                                       page_need[item],
                                                                                                       page)
                    datas = response['data']['data']
                    if not datas:
                        break
                    for data in datas:
                        itemId = data['item']['itemId']  # 商品ID
                        title = data['item']['title']  # 商品名称
                        uv = data['uv']['value']  # 访客数
                        uv_ratio = data['uv']['ratio']  # 商品ID
                        crtByrCnt = data['crtByrCnt']['value']  # 下单买家数
                        crtRate = data['crtRate']['value']  # 下单转化率
                        pv = data['pv']['value']  # 浏览量
                        payAmt = data['payAmt']['value']  # 支付金额
                        jpSelfUv = data['jpSelfUv']['value']  # 店内跳转人数
                        jpUv = data['jpUv']['value']  # 跳出本店人数
                        cltCnt = data['cltCnt']['value']  # 收藏人数
                        cartByrCnt = data['cartByrCnt']['value']  # 加购人数
                        payItmCnt = data['payItmCnt']['value']  # 支付件数
                        payByrCnt = data['payByrCnt']['value']  # 支付买家数
                        payRate = data['payRate']['value']  # 支付转化率
                        directPayByrCnt = data['directPayByrCnt']['value']  # 直接支付买家数
                        cltItmPayByrCnt = data['cltItmPayByrCnt']['value']  # 收藏商品-支付买家数
                        fansPayByrCnt = data['fansPayByrCnt']['value']  # 粉丝支付买家数
                        ordItmPayByrCnt = data['ordItmPayByrCnt']['value']  # 加购商品-支付买家数
                        guideByMiniDetailPayByrCnt = data['guideByMiniDetailPayByrCnt']['value'] if data[
                                                                                                        'guideByMiniDetailPayByrCnt'] != {} else None  # 微详情引导支付买家数
                        guideByMiniDetailPayAmt = data['guideByMiniDetailPayAmt']['value'] if data[
                                                                                                  'guideByMiniDetailPayAmt'] != {} else None  # 微详情引导支付金额
                        guideToMiniDetailUv = data['guideToMiniDetailUv']['value'] if data[
                                                                                          'guideToMiniDetailUv'] != {} else None  # 引导至微详情访客数
                        guideByMiniDetailCartByrCnt = data['guideByMiniDetailCartByrCnt']['value'] if data[
                                                                                                          'guideByMiniDetailCartByrCnt'] != {} else None  # 微详情引导加购人数
                        guideByMiniDetailCltCnt = data['guideByMiniDetailCltCnt']['value'] if data[
                                                                                                  'guideByMiniDetailCltCnt'] != {} else None  # 微详情引导收藏人数
                        guideByMiniDetailPayRate = data['guideByMiniDetailPayRate']['value'] if data[
                                                                                                    'guideByMiniDetailPayRate'] != {} else None  # 微详情引导支付转化率
                        tup1 = (
                            start_day, item, itemId, title, uv, uv_ratio, crtByrCnt, '%.4f' % crtRate, pv, payAmt,
                            jpSelfUv,
                            jpUv, cltCnt, cartByrCnt, payItmCnt, payByrCnt, '%.4f' % payRate, directPayByrCnt,
                            cltItmPayByrCnt,
                            fansPayByrCnt, ordItmPayByrCnt, guideByMiniDetailPayByrCnt, guideByMiniDetailPayAmt,
                            guideToMiniDetailUv, guideByMiniDetailCartByrCnt, guideByMiniDetailCltCnt,
                            guideByMiniDetailPayRate)
                        self._sql_server.save_message(table, [tup1])
                    page += 1
                    time.sleep(1)
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)

    def _source_of_secondary_flow_commodities_commodity_effect_day_request(self, start_day, cookie, item, page):
        url = 'https://sycm.taobao.com/flow/v5/shop/source/top/item.json'
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': cookie,
            'onetrace-card-id': 'sycm-flow-shop-source-effect.sycm-flow-goods-effect-flow-shop-source-effect-list',
            'pragma': 'no-cache',
            'referer': 'https://sycm.taobao.com/flow/monitor/shopsource/effect?belong=all&childPageType=se_keyword&crowdType=all&dateRange=2022-04-10%7C2022-04-10&dateType=day&device=2&pPageId=23&pageId=23.s1150&pageLevel=2&pageName=%E6%89%8B%E6%B7%98%E6%90%9C%E7%B4%A2&spm=a21ag.11910098.sycm-flow-shop-source-construction-list.4.6c1950a5kUcA65',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sycm-query': 'dateType=day',
            'sycm-referer': '/flow/monitor/shopsource/effect',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        params = {
            'dateRange': f'{start_day}|{start_day}',
            'dateType': 'day',
            'pageSize': '10',
            'page': page,
            'order': 'desc',
            'orderBy': 'uv',
            'device': '2',
            'belong': 'all',
            'pageId': f'{item[0]}',
            'pPageId': f'{item[1]}',
            'childPageType': f'{item[2]}',
            'indexCode': 'uv,crtByrCnt,crtRate',
            '_': '1649751279669',
            'token': '2decb18fa'
        }
        response = requests.get(url=url, headers=headers, params=params).json()
        return response

    # 贝德美.dbo.二级流量来源_无线端_店铺
    def secondary_flow_source_wireless_terminal_shop_main(self, start_day, end_day, cookie, table, shop_name):
        while True:
            info = []
            if not start_day:
                start_day = self._sql_server.get_start_day(table, '日期', '')
                if start_day == get_before_day(get_today()):
                    print('<贝德美.dbo.二级流量来源_无线端_店铺>数据获取完毕')
                    return 0
                start_day = get_after_day(start_day)
            if not end_day:
                end_day = get_before_day(get_today())
            self._shop_judgment(shop_name, cookie)
            response = self._secondary_flow_source_wireless_terminal_shop_request(cookie, start_day)
            datas = response['data']
            for data in datas:
                item = data['pageName']['value']  # 来源
                pageName = '汇总'  # 来源明细
                uv = data['uv']['value']  # 访客数
                try:
                    uv_cycleCrc = data['uv']['cycleCrc']  # 访客数变化
                except:
                    uv_cycleCrc = None
                if uv_cycleCrc:
                    uv_cycleCrc = '%.4f' % uv_cycleCrc
                crtVldAmt = data['crtVldAmt']['value']  # 下单金额
                try:
                    crtVldAmt_cycleCrc = data['uv']['cycleCrc']  # 下单金额变化
                except:
                    crtVldAmt_cycleCrc = None
                if crtVldAmt_cycleCrc:
                    crtVldAmt_cycleCrc = '%.4f' % crtVldAmt_cycleCrc
                crtByrCnt = data['crtByrCnt']['value']  # 下单买家数
                try:
                    crtByrCnt_cycleCrc = data['crtByrCnt']['cycleCrc']  # 下单买家数变化
                except:
                    crtByrCnt_cycleCrc = None
                if crtByrCnt_cycleCrc:
                    crtByrCnt_cycleCrc = '%.4f' % crtByrCnt_cycleCrc
                crtRate = data['crtRate']['value']  # 下单转化率
                try:
                    crtRate_cycleCrc = data['crtRate']['cycleCrc']  # 下单转化率变化
                except:
                    crtRate_cycleCrc = None
                if crtRate_cycleCrc:
                    crtRate_cycleCrc = '%.4f' % crtRate_cycleCrc
                payAmt = data['payAmt']['value']  # 支付金额
                try:
                    payAmt_cycleCrc = data['payAmt']['cycleCrc']  # 支付金额变化
                except:
                    payAmt_cycleCrc = None
                if payAmt_cycleCrc:
                    payAmt_cycleCrc = '%.4f' % payAmt_cycleCrc
                payByrCnt = data['payByrCnt']['value']  # 支付买家数
                try:
                    payByrCnt_cycleCrc = data['payByrCnt']['cycleCrc']  # 支付买家数变化
                except:
                    payByrCnt_cycleCrc = None
                if payByrCnt_cycleCrc:
                    payByrCnt_cycleCrc = '%.4f' % payByrCnt_cycleCrc
                payRate = data['payRate']['value']  # 支付转化率
                try:
                    payRate_cycleCrc = data['payRate']['cycleCrc']  # 支付转化率变化
                except:
                    payRate_cycleCrc = None
                if payRate_cycleCrc:
                    payRate_cycleCrc = '%.4f' % payRate_cycleCrc
                payPct = data['payPct']['value']  # 客单价
                try:
                    payPct_cycleCrc = data['payPct']['cycleCrc']  # 客单价变化
                except:
                    payPct_cycleCrc = None
                if payPct_cycleCrc:
                    payPct_cycleCrc = '%.4f' % payPct_cycleCrc
                uvValue = data['uvValue']['value']  # uv价值
                try:
                    uvValue_cycleCrc = data['uvValue']['cycleCrc']  # uv价值变化
                except:
                    uvValue_cycleCrc = None
                if uvValue_cycleCrc:
                    uvValue_cycleCrc = '%.4f' % uvValue_cycleCrc
                shopCltByrCnt = data['shopCltByrCnt']['value']  # 关注店铺买家数
                try:
                    shopCltByrCnt_cycleCrc = data['payRate']['cycleCrc']  # 关注店铺买家数变化
                except:
                    shopCltByrCnt_cycleCrc = None
                if shopCltByrCnt_cycleCrc:
                    shopCltByrCnt_cycleCrc = '%.4f' % shopCltByrCnt_cycleCrc
                cltItmCnt = data['cltItmCnt']['value']  # 收藏商品买家数
                try:
                    cltItmCnt_cycleCrc = data['payRate']['cycleCrc']  # 收藏商品买家数变化
                except:
                    cltItmCnt_cycleCrc = None
                if cltItmCnt_cycleCrc:
                    cltItmCnt_cycleCrc = '%.4f' % cltItmCnt_cycleCrc
                cartByrCnt = data['cartByrCnt']['value']  # 加购人数
                try:
                    cartByrCnt_cycleCrc = data['cartByrCnt']['cycleCrc']  # 加购人数变化
                except:
                    cartByrCnt_cycleCrc = None
                if cartByrCnt_cycleCrc:
                    cartByrCnt_cycleCrc = '%.4f' % cartByrCnt_cycleCrc
                newUv = data['newUv']['value']  # 新访客
                try:
                    newUv_cycleCrc = data['newUv']['cycleCrc']  # 新访客变化
                except:
                    newUv_cycleCrc = None
                if newUv_cycleCrc:
                    newUv_cycleCrc = '%.4f' % newUv_cycleCrc
                directPayByrCnt = data['directPayByrCnt']['value']  # 直接支付买家数
                cltItmPayByrCnt = data['cltItmPayByrCnt']['value']  # 收藏商品-支付买家数
                fansPayByrCnt = data['fansPayByrCnt']['value']  # 粉丝支付买家数
                ordItmPayByrCnt = data['ordItmPayByrCnt']['value']  # 加购商品-支付买家数
                # guideToShortVideoUv = i['guideToShortVideoUv']['value']  # 引导短视频访客数
                # ipvUvRelate = i['ipvUvRelate']['value']  # 引导商品访客数

                tup1 = (
                    start_day, item, pageName, uv, uv_cycleCrc, '%.2f' % crtVldAmt, crtVldAmt_cycleCrc, crtByrCnt,
                    crtByrCnt_cycleCrc, crtRate,
                    crtRate_cycleCrc, '%.2f' % payAmt, payAmt_cycleCrc, payByrCnt, payByrCnt_cycleCrc,
                    '%.4f' % payRate,
                    payRate_cycleCrc, '%.2f' % payPct, payPct_cycleCrc, '%.2f' % uvValue, uvValue_cycleCrc,
                    shopCltByrCnt,
                    shopCltByrCnt_cycleCrc, cltItmCnt, cltItmCnt_cycleCrc, cartByrCnt, cartByrCnt_cycleCrc, newUv,
                    newUv_cycleCrc,
                    directPayByrCnt, cltItmPayByrCnt, fansPayByrCnt, ordItmPayByrCnt)
                info.append(tup1)
                for x in data['children']:
                    try:
                        pageName = x['pageName']['value']  # 来源明细
                        uv = x['uv']['value']  # 访客数
                        uv_cycleCrc = x['uv']['cycleCrc']  # 访客数变化
                        if uv_cycleCrc:
                            uv_cycleCrc = '%.4f' % uv_cycleCrc
                        crtVldAmt = x['crtVldAmt']['value']  # 下单金额
                        crtVldAmt_cycleCrc = x['uv']['cycleCrc']  # 下单金额变化
                        if crtVldAmt_cycleCrc:
                            crtVldAmt_cycleCrc = '%.4f' % crtVldAmt_cycleCrc
                        crtByrCnt = x['crtByrCnt']['value']  # 下单买家数
                        crtByrCnt_cycleCrc = x['crtByrCnt']['cycleCrc']  # 下单买家数变化
                        if crtByrCnt_cycleCrc:
                            crtByrCnt_cycleCrc = '%.4f' % crtByrCnt_cycleCrc
                        crtRate = x['crtRate']['value']  # 下单转化率
                        crtRate_cycleCrc = x['crtRate']['cycleCrc']  # 下单转化率变化
                        if crtRate_cycleCrc:
                            crtRate_cycleCrc = '%.4f' % crtRate_cycleCrc
                        payAmt = x['payAmt']['value']  # 支付金额
                        payAmt_cycleCrc = x['payAmt']['cycleCrc']  # 支付金额变化
                        if payAmt_cycleCrc:
                            payAmt_cycleCrc = '%.4f' % payAmt_cycleCrc
                        payByrCnt = x['payByrCnt']['value']  # 支付买家数
                        payByrCnt_cycleCrc = x['payByrCnt']['cycleCrc']  # 支付买家数变化
                        if payByrCnt_cycleCrc:
                            payByrCnt_cycleCrc = '%.4f' % payByrCnt_cycleCrc
                        payRate = x['payRate']['value']  # 支付转化率
                        payRate_cycleCrc = x['payRate']['cycleCrc']  # 支付转化率变化
                        if payRate_cycleCrc:
                            payRate_cycleCrc = '%.4f' % payRate_cycleCrc
                        payPct = x['payPct']['value']  # 客单价
                        payPct_cycleCrc = x['payPct']['cycleCrc']  # 客单价变化
                        if payPct_cycleCrc:
                            payPct_cycleCrc = '%.4f' % payPct_cycleCrc
                        uvValue = x['uvValue']['value']  # uv价值
                        uvValue_cycleCrc = x['uvValue']['cycleCrc']  # uv价值变化
                        if uvValue_cycleCrc:
                            uvValue_cycleCrc = '%.4f' % uvValue_cycleCrc
                        shopCltByrCnt = x['shopCltByrCnt']['value']  # 关注店铺买家数
                        shopCltByrCnt_cycleCrc = x['payRate']['cycleCrc']  # 关注店铺买家数变化
                        if shopCltByrCnt_cycleCrc:
                            shopCltByrCnt_cycleCrc = '%.4f' % shopCltByrCnt_cycleCrc
                        cltItmCnt = x['cltItmCnt']['value']  # 收藏商品买家数
                        cltItmCnt_cycleCrc = x['payRate']['cycleCrc']  # 收藏商品买家数变化
                        if cltItmCnt_cycleCrc:
                            cltItmCnt_cycleCrc = '%.4f' % cltItmCnt_cycleCrc
                        cartByrCnt = x['cartByrCnt']['value']  # 加购人数
                        cartByrCnt_cycleCrc = x['cartByrCnt']['cycleCrc']  # 加购人数变化
                        if cartByrCnt_cycleCrc:
                            cartByrCnt_cycleCrc = '%.4f' % cartByrCnt_cycleCrc
                        newUv = x['newUv']['value']  # 新访客
                        newUv_cycleCrc = x['newUv']['cycleCrc']  # 新访客变化
                        if newUv_cycleCrc:
                            newUv_cycleCrc = '%.4f' % newUv_cycleCrc
                        directPayByrCnt = x['directPayByrCnt']['value']  # 直接支付买家数
                        cltItmPayByrCnt = x['cltItmPayByrCnt']['value']  # 收藏商品-支付买家数
                        fansPayByrCnt = x['fansPayByrCnt']['value']  # 粉丝支付买家数
                        ordItmPayByrCnt = x['ordItmPayByrCnt']['value']  # 加购商品-支付买家数

                        tup1 = (
                            start_day, item, pageName, uv, uv_cycleCrc, crtVldAmt, crtVldAmt_cycleCrc, crtByrCnt,
                            crtByrCnt_cycleCrc, crtRate, crtRate_cycleCrc, '%.2f' % payAmt, payAmt_cycleCrc,
                            payByrCnt,
                            payByrCnt_cycleCrc, '%.4f' % payRate, payRate_cycleCrc, '%.2f' % payPct,
                            payPct_cycleCrc,
                            '%.2f' % uvValue, uvValue_cycleCrc, shopCltByrCnt, shopCltByrCnt_cycleCrc, cltItmCnt,
                            cltItmCnt_cycleCrc, cartByrCnt, cartByrCnt_cycleCrc, newUv, newUv_cycleCrc,
                            directPayByrCnt,
                            cltItmPayByrCnt, fansPayByrCnt, ordItmPayByrCnt)
                        info.append(tup1)
                    except:
                        break
                time.sleep(5)
            self._sql_server.save_message(table, info)
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)

    def _secondary_flow_source_wireless_terminal_shop_request(self, cookie, start_day):
        url = 'https://sycm.taobao.com/flow/v5/shop/source/tree.json'
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': cookie,
            'onetrace-card-id': 'sycm-flow-shop-source-construction.sycm-flow-shop-source-construction-flow-source-self-table.sycm-flow-shop-source-construction-list',
            'pragma': 'no-cache',
            'referer': 'https://sycm.taobao.com/flow/monitor/shopsource/construction?belong=all&dateRange=2022-04-11%7C2022-04-11&dateType=day&device=2&rivalUser1Id=&spm=a21ag.11910098.LeftMenu.d603.327c50a5kzZC3u',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sycm-query': 'dateType=day',
            'sycm-referer': '/flow/monitor/shopsource/construction',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        params = {
            'dateRange': f'{start_day}|{start_day}',
            'dateType': 'day',
            'pageSize': '10',
            'page': '1',
            'order': 'desc',
            'orderBy': 'uv',
            'device': '2',
            'belong': 'all',
            'indexCode': 'uv,crtByrCnt,crtRate',
            '_': '1649755618152',
            'token': '2decb18fa'
        }
        response = requests.get(url=url, headers=headers, params=params).json()
        return response

    # 贝德美.dbo.品类_宏观监控_标准类目_日
    def category_macro_monitoring_standard_category_main(self, start_day, end_day, cookie, table, shop_name):
        while True:
            if not start_day:
                start_day = self._sql_server.get_start_day(table, '日期', '')
                if start_day == get_before_day(get_today()):
                    print('<贝德美.dbo.品类_宏观监控_标准类目_日>数据获取完毕')
                    return 0
                start_day = get_after_day(start_day)
            if not end_day:
                end_day = get_before_day(get_today())
            self._shop_judgment(shop_name, cookie)
            params = {
                'dateRange': f'{start_day}|{start_day}',
                'dateType': 'day',
                'pageSize': '10',
                'page': '1',
                'order': 'desc',
                'orderBy': 'payAmt',
                'follow': 'false',
                'cateType': 'std',
                'indexCode': 'payAmt,payAmtRatio,paidItemCnt,sucRefundAmt,itmUv',
                '_': '1640056390526',
                'token': '5a8e5403a'
            }
            response = self._category_standard_category_request(cookie, params)
            datas = response['data']
            values = []
            for data in datas:
                cateName = data['cateName']
                value1, cateId1 = self._analysis_request(data, [cateName], start_day)
                if value1 not in values:
                    values.append(value1)
                infos = data['children']
                for info in infos:
                    cateName1 = info['cateName']
                    value2, cateId2 = self._analysis_request(info, [cateName, cateName1], start_day)
                    if value2 not in values:
                        values.append(value2)
                    params = {
                        'dateRange': f'{start_day}|{start_day}',
                        'dateType': 'day',
                        'pageSize': '10',
                        'page': '1',
                        'order': 'desc',
                        'orderBy': 'payAmt',
                        'follow': 'false',
                        'cateType': 'std',
                        'indexCode': 'payAmt,payAmtRatio,sucRefundAmt,payRate,itmUv',
                        'level2CateId': f'{cateId2}',
                        '_': '1640065436862',
                        'token': '5a8e5403a'
                    }
                    try:
                        response1 = self.category_standard_category_request(cookie, params)
                        datas1 = response1['data']
                    except:
                        continue
                    for data1 in datas1:
                        try:
                            cateName2 = data1['cateName']
                            value3, cateId3 = self.analysis_request(data1, [cateName, cateName1, cateName2],
                                                                    start_day)
                            if value3 not in values:
                                values.append(value3)
                        except:
                            pass
                    time.sleep(5)
            try:
                SqlServerConnect().save_message(table, values)
            except:
                pass
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)
            time.sleep(5)

    def _analysis_request(self, data, cateName, start_day):
        crtAmt = data['crtAmt']['value']  # 下单金额
        crtByrCnt = data['crtByrCnt']['value']  # 下单买家数
        crtItmQty = data['crtItmQty']['value']  # 下单件数
        crtRate = data['crtRate']['value']  # 下单转化率
        itemCartByrCnt = data['itemCartByrCnt']['value']  # 商品加购人数
        itemCartCnt = data['itemCartCnt']['value']  # 商品加购件数
        itemCltByrCnt = data['itemCltByrCnt']['value']  # 商品收藏人数
        itmPv = data['itmPv']['value']  # 商品浏览量
        itmUv = data['itmUv']['value']  # 商品访客数
        juPayAmt = data['juPayAmt']['value']  # 聚划算支付金额
        mtdPayAmt = data['mtdPayAmt']['value']  # 月累计支付金额
        newPayByrCnt = data['newPayByrCnt']['value']  # 支付新买家数
        olderPayAmt = data['olderPayAmt']['value']  # 老买家支付金额
        paidItemCnt = data['paidItemCnt']['value']  # 有支付商品数
        payAmt = data['payAmt']['value']  # 支付金额
        payAmtRatio = data['payAmtRatio']['value']  # 支付金额占比
        payByrCnt = data['payByrCnt']['value']  # 支付买家数
        payItmCnt = data['payItmCnt']['value']  # 支付件数
        payOldByrCnt = data['payOldByrCnt']['value']  # 支付老买家数
        payPct = data['payPct']['value']  # 客单价
        payRate = data['payRate']['value']  # 支付转化率
        sucRefundAmt = data['sucRefundAmt']['value']  # 售中售后成功退款金额
        uvAvgValue = data['uvAvgValue']['value']  # 访客平均价值
        try:
            visitCartRate = data['visitCartRate']['value']  # 访问加购转化率
            visitCltRate = data['visitCltRate']['value']  # 访问收藏转化率
        except:
            visitCartRate = 0
            visitCltRate = 0
        visitedItemCnt = data['visitedItemCnt']['value']  # 有访客商品数
        ytdPayAmt = data['ytdPayAmt']['value']  # 年累计支付金额
        if len(cateName) == 1:
            cateId = data['cateId']['value']  # 类目id，用于下一个请求参数
            cateName2 = cateName[0]
            cateName3 = cateName[0]
        if len(cateName) == 2:
            cateId = data['cateId']['value']  # 类目id，用于下一个请求参数
            cateName2 = cateName[1]
            cateName3 = cateName[1]
        if len(cateName) == 3:
            cateId = None
            cateName2 = cateName[1]
            cateName3 = cateName[2]
        value = (
            start_day, cateName[0], cateName2, cateName3, itmUv, itmPv, visitedItemCnt, paidItemCnt, itemCartByrCnt,
            itemCartCnt, itemCltByrCnt, '%.4f' % visitCltRate, '%.4f' % visitCartRate, crtByrCnt, crtItmQty,
            '%.2f' % crtAmt if crtAmt != None else None, '%.4f' % crtRate if crtRate != None else None, payByrCnt,
            payItmCnt, '%.2f' % payAmt if payAmt != None else None,
            '%.4f' % payAmtRatio if payAmtRatio != None else None,
            '%.4f' % payRate if payRate != None else None, '%.2f' % mtdPayAmt if mtdPayAmt != None else None,
            '%.2f' % ytdPayAmt if ytdPayAmt != None else None, '%.2f' % juPayAmt if juPayAmt != None else None,
            newPayByrCnt,
            payOldByrCnt,
            '%.2f' % olderPayAmt if olderPayAmt != None else None, '%.2f' % payPct if payPct != None else None,
            '%.2f' % uvAvgValue if uvAvgValue != None else None,
            '%.2f' % sucRefundAmt if sucRefundAmt != None else None)
        return value, cateId

    def _category_standard_category_request(self, cookie, params):
        url = 'https://sycm.taobao.com/cc/cockpit/marcro/cate.json'
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': cookie,
            'onetrace-card-id': 'sycm-cc-category-all.sycm-cc-category-all-cate-rank-table',
            'referer': 'https://sycm.taobao.com/cc/new_cate_archives?spm=a21ag.23983127.LeftMenu.d2172.223450a5OE3yWU',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        response = requests.get(url=url, headers=headers, params=params)
        return response.json()

    # 贝德美.dbo.品类_商品效果_日
    def category_commodity_effect_day_main(self, start_day, end_day, cookie, table, shop_name):
        while True:
            if not start_day:
                start_day = self._sql_server.get_start_day(table, '日期', '')
                if start_day == get_before_day(get_today()):
                    print('<贝德美.dbo.品类_商品效果_日>数据获取完毕')
                    return 0
                start_day = get_after_day(start_day)
            if not end_day:
                end_day = get_before_day(get_today())
            self._shop_judgment(shop_name, cookie)
            response = self._commodity_effect_day_request(start_day, cookie)
            wb2 = xlrd.open_workbook('./excels/15.xlsx')
            sh2 = wb2.sheet_by_name(wb2.sheets()[0].name)
            payAmts = 0
            values = []
            for i in range(sh2.nrows)[1:]:
                a = sh2.row_values(i)
                if a[0] == start_day:
                    value = []
                    for b in a:
                        if b == '-':
                            b = None
                        if b:
                            b = b.replace(',', '')
                            if '%' in b:
                                b = round(float(b.replace('%', '')) / 100, 4)
                        value.append(b)
                    values.append(tuple(value))
                    payAmts += float(value[-15])
            if table == '贝德美.dbo.品类_商品效果_日':
                sql = f"select 支付金额 from 贝德美.dbo.取数_店铺整体_日 where 日期='{start_day}'"
            else:
                sql = f"select 支付金额 from 贝德美.BODORME.取数_店铺整体_日 where 日期='{start_day}'"
            res = self._sql_server.check_message(sql, 0)[0]
            if abs(int(res) - int(payAmts)) < 5:
                try:
                    self._sql_server.save_message(table, values)
                except:
                    pass
            else:
                raise '更换关键词排序'
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)

    def _commodity_effect_day_request(self, start_day, cookie):
        url = 'https://sycm.taobao.com/cc/item/view/excel/top.json'
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': cookie,
            'pragma': 'no-cache',
            'referer': 'https://sycm.taobao.com/cc/item_rank',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        params = {
            'spm': 'a21ag.23983127.item-rank.1.6a2750a5MwSoD0',
            'dateRange': f'{start_day}|{start_day}',
            'dateType': 'day',
            'pageSize': '10',
            'page': '1',
            'order': 'desc',
            'orderBy': 'payAmt',
            'dtUpdateTime': 'false',
            'dtMaxAge': '0',
            'device': '0',
            'compareType': 'cycle',
            'keyword': '',
            'follow': 'false',
            'cateId': '',
            'cateLevel': '',
            'indexCode': 'payAmt,payItmCnt,sucRefundAmt,itemCartCnt,itmUv'
        }
        response = requests.get(url=url, headers=headers, params=params).content
        with open('./excels/15.xlsx', 'wb') as w:
            w.write(response)
        w.close()
        return response

    # 二级流量来源_无线端_店铺_月  贝德美旗舰店账号
    def secondary_flow_source_wireless_store_main(self, start_month, end_month, cookie, shop_name):
        self._shop_judgment(shop_name, cookie)
        while True:
            if not start_month:
                start_month = self._sql_server.get_start_day('贝德美.dbo.二级流量来源_无线端_店铺_月', '月份', '')
                start_month = start_month[:-2] + '-' + start_month[-2:]
                if start_month == get_before_month(get_month()):
                    print('<二级流量来源_无线端_店铺_月>数据已经更新至最新')
                    return 0
            if not end_month:
                end_month = get_before_month(get_month())
            self._secondary_flow_source_wireless_store_request(start_month, cookie)
            wb = xlrd.open_workbook(r'sycm.xls')
            shs = wb.sheet_by_name(wb.sheet_names()[0])
            values = []
            start = 0
            for sh in range(shs.nrows):
                if shs.row_values(sh)[0] == '流量来源':
                    start = 1
                    continue
                if start:
                    value = [start_month.replace('-', '')]
                    for item in shs.row_values(sh):
                        item = item.replace(',', '')
                        if item:
                            if '%' in item:
                                item = round(float(item.replace('%', '')) / 100)
                            if item == '-':
                                item = None
                        value.append(item)
                    values.append(tuple(value))
            if values:
                SqlServerConnect().save_message('贝德美.dbo.二级流量来源_无线端_店铺_月', values)
            if start_month == end_month:
                break
            start_month = get_after_month(start_month)

    def _secondary_flow_source_wireless_store_request(self, start_month, cookie):
        url = f'https://sycm.taobao.com/flow/gray/excel.do?spm=a21ag.11910098.sycm-flow-shop-source-construction-flow-source-self-table.2.488f410cRR3sMd&_path_=v4/excel/shop/source&device=2&dateType=month&dateRange={start_month + "-01"}|{get_before_day(get_after_month(start_month) + "-01")}&belong=all'
        headers = {
            'Host': 'sycm.taobao.com',
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://sycm.taobao.com/flow/monitor/shopsource/construction?belong=all&dateRange=2021-12-01%7C2021-12-31&dateType=month&device=2&rivalUser1Id=&spm=a21ag.8198212.LeftMenu.d603.5830410cUPYYRb',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': cookie
        }
        response = requests.get(url=url, headers=headers).content
        with open('sycm.xls', 'wb') as w:
            w.write(response)
        w.close()

    # 品类商品效果_月
    def commodity_effect_month_main(self, start_month, end_month, cookie, table, shop_name):
        if not start_month:
            start_month = self._sql_server.get_start_day(table, '月份', '')
            if start_month == get_before_month(get_month()).replace('-', ''):
                print('<品类商品效果_月>数据获取完毕')
                return 0
            start_month = get_after_month(start_month)
        if not end_month:
            end_month = get_before_month(get_month())
        self._shop_judgment(shop_name, cookie)
        while True:
            response = self._commodity_effect_month_request(start_month, cookie)
            wb2 = xlrd.open_workbook('./excels/18.xlsx')
            sh2 = wb2.sheet_by_name(wb2.sheets()[0].name)
            payAmts = 0
            values = []
            for i in range(sh2.nrows)[1:]:
                a = sh2.row_values(i)
                if a[0] == get_before_day(get_after_month(start_month) + '-01'):
                    value = []
                    for b in a:
                        if b == '-':
                            b = None
                        if b:
                            b = b.replace(',', '')
                            if '%' in b:
                                b = round(float(b.replace('%', '')) / 100, 4)
                        value.append(b)
                    value[0] = start_month.replace('-', '')
                    value[8] = value[8].split('.')[0]
                    values.append(tuple(value))
                    payAmts += float(value[-15])
            if table == '贝德美.dbo.品类_商品效果_月':
                sql = f"select 支付金额 from 贝德美.dbo.取数_店铺整体_月 where 月份='{start_month.replace('-', '')}'"
            else:
                sql = f"select 支付金额 from 贝德美.BODORME.取数_店铺整体_月 where 月份='{start_month.replace('-', '')}'"
            res = self._sql_server.check_message(sql, 0)[0]
            if abs(int(res) - int(payAmts)) < 5:
                try:
                    self._sql_server.save_message(table, values)
                except:
                    pass
            else:
                raise '更换关键词排序'
            if start_month == end_month:
                break
            start_month = get_after_month(start_month)

    def _commodity_effect_month_request(self, start_month, cookie):
        url = 'https://sycm.taobao.com/cc/item/view/excel/top.json'
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': cookie,
            'pragma': 'no-cache',
            'referer': 'https://sycm.taobao.com/cc/item_rank',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        params = {
            'spm': 'a21ag.23983127.item-rank.1.6a2750a5MwSoD0',
            'dateRange': f'{start_month + "-01"}|{get_before_day(get_after_month(start_month) + "-01")}',
            'dateType': 'month',
            'pageSize': '10',
            'page': '1',
            'order': 'desc',
            'orderBy': 'payAmt',
            'dtUpdateTime': 'false',
            'dtMaxAge': '0',
            'device': '0',
            'compareType': 'cycle',
            'keyword': '',
            'follow': 'false',
            'cateId': '',
            'cateLevel': '',
            'indexCode': 'payAmt,payItmCnt,sucRefundAmt,itemCartCnt,itmUv'
        }
        response = requests.get(url=url, headers=headers, params=params).content
        with open('./excels/18.xlsx', 'wb') as w:
            w.write(response)
        w.close()
        return response

    # 优惠券效果_日
    def coupon_effect_day_main(self, start_day, end_day, cookie):
        while 1:
            if not start_day:
                start_day = self._sql_server.get_start_day('[贝德美].[dbo].[优惠券效果_日]', '日期', '')
                if start_day == get_before_day(get_today()):
                    print('<优惠券效果_日>今日数据获取完毕')
                    return 0
                start_day = get_after_day(start_day)
            if not end_day:
                end_day = get_before_day(get_today())
            sql = f"""SELECT [优惠券ID] FROM [贝德美].[dbo].[t_coupon_base_info] where InsertDate > '2022-01-01' and 投放方 = '抖加' and 使用起始日期 <= '{start_day}' and 使用结束日期 >= '{start_day}'"""
            actIds = self._sql_server.check_message(sql, 1)
            for actId in actIds:
                self._coupon_effect_day_request(start_day, actId[0], cookie)
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)

    def _coupon_effect_day_request(self, start_day, actId, cookie):
        url = 'https://sycm.taobao.com/xsite/sale/getSaleToolActTrend.json'
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': cookie,
            'onetrace-card-id': 'promotionSalesDetail-fenri-shopbonus-4849560032',
            'pragma': 'no-cache',
            'referer': 'https://sycm.taobao.com/xsite/promotion/sales_coupon_detail?toolId=shopbonus&actId=4849560032',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sycm-referer': '/xsite/promotion/sales_coupon_detail',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        params = {
            'dateType': 'day',
            'dateRange': f'{start_day}|{start_day}',
            'indexCode': '',
            'toolId': 'itemcoupon',
            'actId': actId,
            '_': '1644306377387',
            'token': '394e917c4'
        }
        response = requests.get(url=url, headers=headers, params=params).json()
        datas = response['content']['data']
        for key in datas:
            if key == 'payAmt':
                payAmt = datas[key][-1]  # 支付金额
            if key == 'getCouponsCnt':
                getCouponsCnt = datas[key][-1]  # 领取张数
            if key == 'payByrCnt':
                payByrCnt = datas[key][-1]  # 使用张数
                payuser = payByrCnt  # 支付买家数
            if key == 'payItmCnt':
                payItmCnt = datas[key][-1]  # 支付件数
        value = (start_day, actId, getCouponsCnt, payByrCnt, payAmt, payuser, payItmCnt)
        try:
            self._sql_server.save_message('[贝德美].[dbo].[优惠券效果_日]', [value])
        except:
            pass

    # 热浪联盟_推广数据总览_日
    def heat_wave_alliance_overview_of_promotion_data_day_main(self, start_day, end_day, cookie):
        if not start_day:
            start_day = self._sql_server.get_start_day('贝德美.dbo.热浪联盟_推广数据总览_日', '日期', '')
            if start_day == get_before_day(get_today()):
                return 0
            start_day = get_after_day(start_day)
        if not end_day:
            end_day = get_before_day(get_today())
        response = self._heat_wave_alliance_overview_of_promotion_data_day_request(cookie, end_day)
        dates = response['data']['dataTable']
        values = []
        for date in dates:
            value = [start_day]
            for item in dates[start_day.replace('-', '')]:
                if item['val'] == '-':
                    item['val'] = None
                value.append(item['val'])
            values.append(tuple(value))
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)
        self._sql_server.save_message('贝德美.dbo.热浪联盟_推广数据总览_日', values)

    def _heat_wave_alliance_overview_of_promotion_data_day_request(self, cookie, end_day):
        url = f'https://hot.taobao.com/commission/panel/shop/daily/detail.do?_csrf={cookie.split("XSRF-TOKEN=")[1].split(";")[0]}'
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-length': '38',
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': cookie,
            'origin': 'https://hot.taobao.com',
            'referer': 'https://hot.taobao.com/hw/union/goods-alliance/databoard/overview',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'x-xsrf-token': cookie.split("XSRF-TOKEN=")[1].split(";")[0]
        }
        data = {
            'queryDate': f"{end_day.replace('-', '')}",
            'period': '0',
            'planType': '0',
        }
        response = requests.post(url=url, headers=headers, data=data)
        return response.json()

    # 内容_全屏页视频_商品分析_达人带货视频
    def content_full_screen_video_commodity_analysis_videos_of_experts_carrying_goods_main(self, start_day, end_day,
                                                                                           cookie):
        while 1:
            if not start_day:
                start_day = self._sql_server.get_start_day('贝德美.dbo.内容_全屏页视频_商品分析_达人带货视频', '日期', '')
                if start_day == get_before_day(get_today()):
                    return 0
                start_day = get_after_day(start_day)
            if not end_day:
                end_day = get_before_day(get_today())
            response = self._content_full_screen_video_commodity_analysis_videos_of_experts_carrying_goods_request(
                start_day, cookie)
            with open('./excels/3.xlsx', 'wb') as w:
                w.write(response.content)
            w.close()
            wb = xlrd.open_workbook('./excels/3.xlsx')
            sh = wb.sheet_by_name(wb.sheets()[0].name)
            values = []
            for i in range(sh.nrows):
                a = sh.row_values(i)
                if a[0] not in ['数据说明：以下数据为您所选时间周期的相关指标，如需查看其他时间周期的数据，请重新选择后下载',
                                '收藏网址：d.alibaba.com，让数据帮您生意参谋！点此进入>>',
                                '', '商品ID']:
                    a.insert(0, start_day)
                    value = []
                    for i in a:
                        value.append(i.replace(',', ''))
                    values.append(tuple(value))
            self._sql_server.save_message('贝德美.dbo.内容_全屏页视频_商品分析_达人带货视频', values)
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)
            time.sleep(5)

    def _content_full_screen_video_commodity_analysis_videos_of_experts_carrying_goods_request(self, start_day, cookie):
        url = f'https://sycm.taobao.com/s_content/video/single/item/list/v2/export.json?spm=a21ag.21206911.sycm-cp-duanshipin-commodity-table.1.49fd50a5eBBNi0&dateRange={start_day}%7C{start_day}&dateType=day&order=desc&orderBy=clickCnt&keyword=&accountRole=daren&indexCode=clickCnt%2CitemFansClickPv%2CcltTimes%2CcartItmCnt%2CinterestPayAmt'
        headers = {
            'Host': 'sycm.taobao.com',
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://sycm.taobao.com/xsite/contentanalysis/duanshipin/fscreen_analysis?activeKey=commodity&dateRange=2022-02-09%7C2022-02-09&dateType=day',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': cookie
        }
        response = requests.get(url=url, headers=headers)
        return response

    # 热浪联盟商品明细 热浪联盟_主播明细
    def heat_wave_alliance_commodity_details_day_main(self, start_day, end_day, cookie):
        while True:
            if not start_day:
                start_day = self._sql_server.get_start_day('贝德美.dbo.热浪联盟_商品明细_日', '日期', '')
                if start_day == get_before_day(get_today()):
                    return 0
                start_day = get_after_day(start_day)
            if not end_day:
                end_day = get_today()
            response = self._heat_wave_alliance_commodity_details_day_request(cookie, start_day)
            self.heat_wave_alliance_anchor_details_day_main(start_day, cookie)
            dataLabelList = response['data']['dataFirstColumn']
            dataTable = response['data']['dataTable']
            if not dataTable:
                break
            for data in dataLabelList:
                name = dataLabelList[data]['name']
                name_id = dataLabelList[data]['id']
                value = [start_day, name, name_id]
                for save_msg in dataTable[data]:
                    val = save_msg['val']
                    if save_msg['val'] == '-':
                        val = None
                    value.append(val)
                try:
                    self._sql_server.save_message('贝德美.dbo.热浪联盟_商品明细_日', [tuple(value)])
                except:
                    pass
            time.sleep(10)
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)

    def _heat_wave_alliance_commodity_details_day_request(self, cookie, start_day):
        url = f'https://hot.taobao.com/commission/panel/shop/item/detail.do?_csrf={cookie.split("XSRF-TOKEN=")[1].split(";")[0]}'
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': cookie,
            'referer': 'https://hot.taobao.com/hw/union/goods-alliance/databoard/overview',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
            'x-xsrf-token': cookie.split('XSRF-TOKEN=')[1].split(';')[0]
        }
        data = {
            'period': '3',
            'planType': '0',
            'queryDate': start_day.replace('-', '')
        }
        response = requests.post(url=url, headers=headers, params=data).json()
        return response

    # 热浪联盟_主播明细主函数
    def heat_wave_alliance_anchor_details_day_main(self, start_day, cookie):
        zb_response = self._heat_wave_alliance_anchor_details_day_request(cookie, start_day)
        zb_dataTable = zb_response['data']['dataTable']
        zb_dataFirstColumn = zb_response['data']['dataFirstColumn']
        if not zb_dataTable:
            return 0
        for data in zb_dataFirstColumn:
            name = zb_dataFirstColumn[data]['name']
            name_id = zb_dataFirstColumn[data]['id']
            value = [start_day, name, name_id]
            for save_msg in zb_dataTable[data]:
                val = save_msg['val']
                if save_msg['val'] == '-':
                    val = None
                value.append(val)
            try:
                self._sql_server.save_message('贝德美.dbo.热浪联盟_主播明细_日', [tuple(value)])
            except:
                pass

    def _heat_wave_alliance_anchor_details_day_request(self, cookie, start_day):
        url = f'https://hot.taobao.com/commission/panel/shop/anchor/detail.do?_csrf={cookie.split("XSRF-TOKEN=")[1].split(";")[0]}'
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': cookie,
            'referer': 'https://hot.taobao.com/hw/union/goods-alliance/databoard/overview',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
            'x-xsrf-token': cookie.split('XSRF-TOKEN=')[1].split(';')[0]
        }
        data = {
            'period': '3',
            'planType': '0',
            'queryDate': start_day.replace('-', '')
        }
        response = requests.post(url, headers=headers, data=data).json()
        return response

    # 引力魔方_报表_点击_主体汇总
    def gravitational_magic_cube_report_click_entity_summary_main(self, start_day, end_day, cookie):
        # start_day = self._sql_server.get_start_day('贝德美.dbo.引力魔方_报表_点击_主体汇总', '日期', '')
        # if start_day == get_before_day(get_today()):
        #     return 0
        sql = f"""delete from 贝德美.dbo.引力魔方_报表_点击_主体汇总 where 转化周期 < 15"""
        self._sql_server.check_message(sql, 2)
        if not start_day:
            start_day = self._sql_server.get_start_day('贝德美.dbo.引力魔方_报表_点击_主体汇总', '日期', '')
            if start_day == get_before_day(get_today()):
                return 0
            start_day = get_after_day(get_after_day(start_day))
        if not end_day:
            end_day = get_today()
        self.gravitational_magic_cube_report_click_entity_summary_request(start_day, end_day, cookie)
        book = xlrd.open_workbook('./excels/7.xlsx')
        sh2 = book.sheet_by_name(book.sheets()[0].name)
        for i in range(sh2.nrows)[1:]:
            a = sh2.row_values(i)
            week = int((get_time_number(get_today()) - get_time_number(a[0])) / (60 * 60 * 24))
            if week > 15:
                week = 15
            a.insert(0, week)
            save_info = []
            for i in a:
                if not i:
                    i = None
                if i == '0.00000':
                    i = 0
                save_info.append(i)
            self._sql_server.save_message('贝德美.dbo.引力魔方_报表_点击_主体汇总', [tuple(save_info)])

    def gravitational_magic_cube_report_click_entity_summary_request(self, start_day, end_day, cookie):
        infos, csrfID = self._getcsrftoken(cookie)
        headers = {
            'Host': 'tuijian.taobao.com',
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://tuijian.taobao.com/indexbp-display.html',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': cookie
        }
        # url = f'https://tuijian.taobao.com/api2/report/export.json?alias=def&bizCode=displayDefault&componentTemplateId=&creativeId=&privateMiniId=&startTime={start_day}&componentCode=reportFiledTemplate&curComponentTemplateId=undefined&effect=15&endTime={end_day}&effectType=click&baseDomainOptionList=%5B%22needCampaign%22%2C%22needPromotion%22%5D&advancedDomainOptionList=%5B%22needAdzone%22%5D&campaignIdList=%5B%5D&materialIdList=%5B%5D&campaignGroupIdList=%5B%5D&creativeIdList=%5B%5D&subPromotionTypeList=%5B%5D&targetTypeList=%5B%5D&creativeFormIdList=%5B%5D&adzoneIdList=%5B%5D&rptDomainOption=%7B%22needCampaign%22%3Atrue%2C%22needPromotion%22%3Atrue%2C%22needAdzone%22%3Atrue%7D&offset=&pageSize=40&orderField=&orderBy=&timeStr={infos[1]}&csrfID={csrfID}&dynamicToken={infos[0]}&excelName=21&exportSummary='
        url = f'https://tuijian.taobao.com/api2/report/export.json?startTime={get_before_day(start_day)}&endTime={end_day}&bizCode=displayDefault&customs=%5B%22charge%22%2C%22impression%22%2C%22click%22%2C%22ctr%22%2C%22cpc%22%2C%22inshopItemColNum%22%2C%22cartNum%22%2C%22alipayInshopNum%22%5D&curTemplateId=xtpromotion&random=0.5880527312372557&rptDomainOption=%7B%22needPromotion%22%3Atrue%7D&realtime=false&offset=0&pageSize=40&orderField=&orderBy=&effect=15&effectType=click&timeStr={infos[1]}&csrfID={csrfID}&dynamicToken={infos[0]}&exportSummary=false'
        response = requests.get(url=url, headers=headers).content
        with open('./excels/7.xlsx', 'wb') as w:
            w.write(response)
        w.close()

    def _getcsrftoken(self, cookie):
        url = 'https://tuijian.taobao.com/api2/member/getInfo.json'
        headers = {
            'accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': cookie,
            'pragma': 'no-cache',
            'referer': 'https://tuijian.taobao.com/indexbp-display.html',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }

        with open(r'F:\lqlf\日常程序\plug_in_unit\alimama.js', 'r') as f:
            b = f.read()
        infos = execjs.compile(b).call('get_n')

        params = {
            'r': 'mx_14',
            'bizCode': 'display',
            'invitationCode': '',
            'timeStr': str(infos[1]),
            'dynamicToken': str(infos[0]),
            'csrfID': '',
            '_': '1646720673455'
        }
        response = requests.get(url=url, headers=headers, params=params).json()
        csrfID = response['data']['csrfID']
        seedToken = response['data']['seedToken']
        pin = response['data']['pin']

        with open(r'F:\lqlf\日常程序\plug_in_unit\alimama.js', 'r') as f:
            b = f.read()
        infos = execjs.compile(b).call('get_n', seedToken, pin)
        return infos, csrfID

    def _getcsrftoken2(self, cookie):
        url = 'https://alimama2.taobao.com/loginUser/info.json'
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': cookie,
            'pragma': 'no-cache',
            'referer': 'https://tuijian.taobao.com/',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'script',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }

        with open(r'F:\lqlf\日常程序\plug_in_unit\alimama.js', 'r') as f:
            b = f.read()
        infos = execjs.compile(b).call('get_n')

        params = {
            'callback': 'jQuery3210505034813495401_1646738316862',
            'r': 'mx_194',
            'bizCode': 'display',
            'timeStr': infos[1],
            'dynamicToken': infos[0],
            'csrfID': '',
            '_': '1646737145111'
        }
        response = requests.get(url=url, headers=headers, params=params).text
        response = response.split('_1646738316862(')[1][:-1]
        response = demjson.decode(response)
        csrfID = response['data']['csrfID']
        # seedToken = str(response['data']['seedToken'])
        # pin = response['data']['pin']

        # with open(r'F:\lqlf\日常程序\plug_in_unit\alimama.js', 'r') as f:
        #     b = f.read()
        # infos = execjs.compile(b).call('get_n', seedToken, pin)
        return csrfID

    def _getcsrftoken3(self, cookie):
        url = 'https://adbrain.taobao.com/api/member/getInfo.json'
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': cookie,
            'pragma': 'no-cache',
            'referer': 'https://adbrain.taobao.com/indexbp.html',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        with open(r'F:\lqlf\日常程序\plug_in_unit\alimama.js', 'r') as f:
            b = f.read()
        infos = execjs.compile(b).call('get_n')
        params = {
            'r': 'mx_14',
            'timeStr': infos[1],
            'dynamicToken': infos[0],
            'bizCode': 'adStrategy'
        }
        response = requests.get(url=url, headers=headers, params=params).json()
        csrfID = response['data']['csrfID']
        seedToken = str(response['data']['seedToken'])
        pin = response['data']['pin']

        with open(r'F:\lqlf\日常程序\plug_in_unit\alimama.js', 'r') as f:
            b = f.read()
        infos = execjs.compile(b).call('get_n', seedToken, pin)
        return infos, csrfID

    def _getcsrftoken4(self, cookie):
        url = 'https://adbrain.taobao.com/api/member/getInfo.json?r=mx_10&timeStr=1658974755928&dynamicToken=432216208404452420212208&bizCode=adStrategy'
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9',
            'bx-v': '2.2.0',
            'cache-control': 'no-cache',
            'cookie': cookie,
            'pragma': 'no-cache',
            'referer': 'https://adbrain.taobao.com/',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }

        response = requests.get(url=url, headers=headers).json()
        # response = response.split('_1646738316862(')[1][:-1]
        # response = demjson.decode(response)
        csrfID = response['data']['csrfID']
        return csrfID

    # 引力魔方_扣款数据
    def gravitational_magic_cube_deduction_data_main(self, start_day, end_day, cookie, table):
        while True:
            if not start_day:
                start_day = self._sql_server.get_start_day(table, '日期', '')
                if start_day == get_before_day(get_today()):
                    print('<引力魔方_扣款数据>数据已更新至最新')
                    return 0
                start_day = get_after_day(get_after_day(start_day))
            if not end_day:
                end_day = get_today()
            page = 0
            while True:
                response = self._gravitational_magic_cube_deduction_data_request(start_day, page, cookie)
                datas = response['data']['list']
                if not datas:
                    break
                for data in datas:
                    uniTransTime = data['uniTransTime']
                    amount = int(data['amount']) / 100
                    value = (get_before_day(uniTransTime.split(' ')[0]), '支出', '扣款', amount, uniTransTime)
                    self._sql_server.save_message(table, [value])
                page += 1
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)

    def _gravitational_magic_cube_deduction_data_request(self, start_day, page, cookie):
        csrfID = self._getcsrftoken2(cookie)
        url = 'https://alimama2.taobao.com/settleAccount/account/listAccountJournal.json'
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': cookie,
            'origin': 'https://tuijian.taobao.com',
            'referer': 'https://tuijian.taobao.com/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
        }
        re_time = int(time.time() * 1000)
        with open(r'F:\lqlf\日常程序\plug_in_unit\dynamicToken.js', 'r', errors='ignore') as r:
            b = r.read()
        dynamicToken = execjs.compile(b).call('t', '', '', re_time)
        params = {
            'r': 'mx_1402',
            'bizCode': 'display',
            'offset': f'{40 * page}',
            'beginTime': start_day,
            'endTime': start_day,
            'limit': '40',
            'finType': 'CREDIT',
            'tradeType': 'DEDUCT',
            'timeStr': re_time,
            'dynamicToken': dynamicToken,
            'csrfID': csrfID
        }
        response = requests.get(url=url, headers=headers, params=params)
        return response.json()

    # 万象台_报表_创意_拉新快
    def vientiane_report_creativity_laxin_express_main(self, cookie):
        start_day = self._sql_server.get_start_day('贝德美.dbo.万象台_报表_创意_拉新快', '日期', '')
        if start_day == get_before_day(get_today()):
            print('<贝德美.dbo.万象台_报表_创意_拉新快>数据已更新至最新')
            return 0
        sql = 'delete from 贝德美.dbo.万象台_报表_创意_拉新快 where 转化周期 < 15'
        self._sql_server.check_message(sql, 2)
        start_day = get_before_day(get_today())
        self._vientiane_report_creativity_laxin_express_request(start_day, cookie)
        wb2 = xlrd.open_workbook('./excels/8.xlsx')
        sh2 = wb2.sheet_by_name(wb2.sheets()[0].name)
        for i in range(sh2.nrows)[1:]:
            a = sh2.row_values(i)
            week = int((get_time_number(get_today()) - get_time_number(a[0])) / (60 * 60 * 24))
            if week > 15:
                week = 15
            a.insert(0, week)
            value = []
            for c in a:
                if not c:
                    c = None
                value.append(c)
            value.remove('15天')
            print(value)
            try:
                self._sql_server.save_message('贝德美.dbo.万象台_报表_创意_拉新快', [tuple(value)])
            except:
                pass

    def _vientiane_report_creativity_laxin_express_request(self, start_day, cookie):
        infos, csrfID = self._getcsrftoken3(cookie)
        url = f'https://adbrain.taobao.com/api/export/report/exportOverProductReportList.json?rptDataContentType=creative&bizCode=adStrategyDkx&unifyType=zhai&effectType=click&groupByDate=day&effects=15&startTime={get_day_before_today(start_day, 14)}&endTime={start_day}&timeStr={infos[1]}&dynamicToken={infos[0]}&csrfID={csrfID}'
        headers = {
            'Host': 'adbrain.taobao.com',
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://adbrain.taobao.com/indexbp.html',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': cookie
        }
        response = requests.get(url=url, headers=headers).content
        print(response)
        with open('./excels/8.xlsx', 'wb') as w:
            w.write(response)
        w.close()

    # 万象台_账户扣款明细
    def vientiane_account_deduction_details_main(self, cookie, table):
        start_day = self._sql_server.get_start_day(table, '日期', '')
        if start_day == get_before_day(get_today()):
            print('<万象台_账户扣款明细>数据已经抓取完毕')
            return 0
        start_day = get_after_day(get_today())
        try:
            if not start_day:
                start_day = self._sql_server.get_start_day(table, '日期', '')
                if start_day == get_before_day(get_today()):
                    print('<万象台_账户扣款明细>数据已经抓取完毕')
                    return 0
                start_day = get_after_day(get_after_day(start_day))
            page = 0
            while True:
                result = self._vientiane_account_deduction_details_request(cookie, page, start_day, table)
                page += 1
                if not result:
                    break
        except:
            error_message(0)

    def _vientiane_account_deduction_details_request(self, cookie, page, start_day, table):
        csrfID = self._getcsrftoken2(cookie)
        url = 'https://alimama2.taobao.com/settleAccount/account/listAccountJournal.json'
        # url = 'https://alimama2.taobao.com/account/listAccountJournal.json'
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': cookie,
            'origin': 'https://adbrain.taobao.com',
            'referer': 'https://adbrain.taobao.com/',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        re_time = int(time.time() * 1000)
        with open(r'F:\lqlf\日常程序\plug_in_unit\dynamicToken.js', 'r', errors='ignore') as r:
            b = r.read()
        dynamicToken = execjs.compile(b).call('t', '', '', re_time)
        params = {
            'r': 'mx_1807',
            'bizCode': 'dkx',
            'offset': f'{page * 40}',
            'beginTime': f'{get_day_before_today(start_day, 29)}',
            'endTime': f'{start_day}',
            'limit': '40',
            'tradeType': 'DEDUCT',
            'timeStr': re_time,
            'dynamicToken': dynamicToken,
            'csrfID': csrfID
        }
        response = requests.get(url=url, headers=headers, params=params)
        response = response.json()
        if not response['data']['list']:
            return 0
        datas = response['data']['list']
        for data in datas:
            if data['finType'] == 'DEBIT':
                bizType = '收入'
            else:
                bizType = '支出'
            if data['tradeType'] == 'DEDUCT':
                tradeType = '扣款'
            amount = round(data['amount'] / 100, 2)
            uniTransTime = data['uniTransTime']
            value = (get_before_day(uniTransTime), bizType, tradeType, amount, uniTransTime)
            try:
                self._sql_server.save_message(table, [value])
            except:
                error_message(1)
        return 1

    # 直播_合作直播间_日
    def live_broadcast_cooperative_broadcast_room_day(self, start_day, end_day, cookie):
        while True:
            if not start_day:
                start_day = self._sql_server.get_start_day('贝德美.dbo.直播_合作直播间_日', '日期', '')
                if start_day == get_before_day(get_today()):
                    return 0
                start_day = get_after_day(start_day)
            if not end_day:
                end_day = get_before_day(get_today())
            values = []
            page = 0
            while True:
                response = self._live_broadcast_cooperative_broadcast_room_request(start_day, cookie, page)
                model = response['data']['model']
                if not model:
                    break
                for data in model:
                    itemTitle = data['itemTitle']  # 标题
                    itemId = data['itemId']  # 商品id
                    accountName = data['accountName']  # 账号名称
                    accountId = data['accountId']  # 账号id
                    contentTitle = data['contentTitle']  # 直播标题
                    contentId = data['contentId']  # 场次id
                    liveStartTime = data['liveStartTime']  # 开播时间
                    ipvUv = data['ipvUv']  # 商品点击人数
                    ipv = data['ipv']  # 商品点击次数
                    cartUv = data['cartUv']  # 商品加够人数
                    cartItemQty = data['cartItemQty']  # 商品加够件数
                    payBuyerCnt = data['payBuyerCnt']  # 种草成交人数
                    payItemQty = data['payItemQty']  # 种草成交件数
                    payOrderCnt = data['payOrderCnt']  # 种草成交笔数
                    payAmt = data['payAmt']  # 种草成交金额
                    value = [start_day, itemTitle, itemId, accountName, accountId, contentTitle, contentId,
                             liveStartTime, ipvUv,
                             ipv, cartUv, cartItemQty, payBuyerCnt, payItemQty, payOrderCnt, payAmt]
                    new_value = []
                    for val in value:
                        if val == '-':
                            val = None
                        new_value.append(val)
                    print(value)
                    try:
                        self._sql_server.save_message('贝德美.dbo.直播_合作直播间_日', [tuple(new_value)])
                    except:
                        pass
                    values.append(tuple(new_value))
                page += 1
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)
            time.sleep(5)

    def _live_broadcast_cooperative_broadcast_room_request(self, start_day, cookie, page):
        url = 'https://sycm.taobao.com/s_live/liveGeneralQuery.json'
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'bx-ua': '140#Bv1rtUtlzzZrgzo2KZrQw3SramE7WG3UWlX/L16m30vKqj8F2jhqYB3JCTm44fMkCJ5Nx6+mOn9e+rTFP3hqzznYGyXtd5XzzjIcba7ulFzx2DD3VthqzZx8QfLz+oH/ziOIWrb3rquu7MQ62CyyQSawjbyoFFsxxD2iVP//lbzx2BHhNssDW0UCaSvZrI7Zbiom9cHylBXCOfE8ZU26zBCqABLrqayurnmp0eRdQUDUM688oWeLuUueowo7I7g49JhE7lwrMqR1Dvc6H7e2L5HCQFXsrZvsXu6b8D9KFI/gADEkWT3nPI1Cclg7REsuoUa1JpWfkFe2Em2QK3UPb49+3DB/3joXkwYvikRGw+NEPpLS3eXfTj10JR5Xp2iKDrxsSMJbqiJBAO5LgVniDiw9VXKZX/tnKNrOzDJVenneRKU6LljPJjIKyrAr/4ydT7Fmvw/Y/ij4RWP2HCgzTRA5S/RgRhRYqYscOslkaCTZ2Erm8OpBUJlYzkZwcP0qxkwpXfSFKR2ArvVgR/fC6zGeMtaTSX1Um95rVU8dfVo0v+zU4nWibOPn+0CB/hRvKoCfAc/S1sugwfz9ImPemhYJo39nkn5qVRdRCiyvAdHNIrp0xm/CNfhclsZ7u9VpVKb4xynyOYTJJGis5AhTUk3xbedr2JkmXAVXbSQz4qzRAjXvonBAVPUEzD77Xz69xBuvUvIqx4rSNWZzHyNM/MfwmCxbWylL2+NKTWeM7POiDMByDwcG1N4CtiF2BOMyb9xxOn0qkfF7SvdgCReLz9Lf/7Svfnk+bMKXx2LOvEPIG07SqvudnEg2whwNC1DTAZ73Ap9PeVt1wq+kcPH504eGbSxJMYZhJr1HlauIcxbQaC7sDlnrYr/UiUGNZpALNl6DCsI4TvwwLX4BRhCQFjhS9U9KwrY9ZjaS3EJFPaD+jDeiiOgHNrw/LtxBJLm9ijixpGpGLi7a+5WNJkOXqz4YGoTuoCwjbSNWLw1f5mrS6PBmIFzMtnD9x2BCx2DGHJzsCjsf5u9U3v+PLJyK5SthQLHufBRpeutmqW7xZi4rmsqfweMtjMERkDfAfKeiv0fGWaHMDcUAnwoBb3ERkrZp1JMfa7EiErgFVvrRrBbLlp0HUPwOsxjpLi/+oGmeyf+S3CoHmkvpUYlzcmsbw2mrIv3G2j8Z21Sf4qNnhvNsBG7DsZlw9FwKfOhpv4HcQfjJe325CiLOs9WMgtyNJWWTSxcjRlqPwALu4sSv8UP+mpA7zMoIF5ZRdVdqoa3adRKOk6v7OAmGgljaVhRFwWGAmS6UK1qRVh9sb6hjbumZZevO2zeT8CkOJPkCfiPOWngqLg6u1+xuqyEudSo+8DX/7Z7d2t0ITafKGUbmZb4Oncg/oLdvYUfl08YRBgPF2uHia75UAvlGimZeYLmSSaXS1K7/cQqVOKrgTuuIo3lV3zL3kd0BpfvvOxB7zZ8HRJ+DL1vnesvWXsWc4xOzQ3Ih+bU3HHTyOiKpfB0k75a35F==',
            'bx-umidtoken': 'T2gA4lJIyQvkESmL0s5UVsFUK5eZVa1MpoHLtNSIzHb0X42_NA_ZutQ1SEMoGDk1Hxk=',
            'cookie': cookie,
            'referer': 'https://sycm.taobao.com/s_live/live_data.htm',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        }
        params = {
            'dataApi': 'dataQRForm',
            'paramJsonStr': '{"dataQRFormId":"live_ia_co_item","beginDate":"%s","endDate":"%s}","itemId":null,"itemTitle":null,"contentId":null,"coAccountId":null,"orderType":"1","orderColumn":"live_start_time","start":"%s","hit":"10","queryUserRole":"ALL","time":1630598400000}' % (
                start_day.replace('-', ''), start_day.replace('-', ''), page * 10)
        }
        response = requests.get(url=url, headers=headers, params=params).json()
        return response

    # 监控店铺_竞店列表_月
    def monitor_stores_list_of_competing_stores_main(self, start_day, end_day, cookie):
        while True:
            if not start_day:
                start_day = self._sql_server.get_start_day('贝德美.dbo.监控店铺_竞店列表_月', '月份', '')
                if start_day == get_before_month(get_month()).replace('-', ''):
                    print('数据抓取完毕')
                    return 0
                start_day = get_after_month(start_day)
            if not end_day:
                end_day = get_before_month(get_month())
            cateIds = [50014812, 50022517]
            values = []
            for cateId in cateIds:
                response = self._monitor_stores_list_of_competing_stores_request(start_day, cookie, cateId)
                response = response.json()
                print(response)
                datas = decrypt(response['data'])
                for i in datas:
                    title = i['shop']['title']  # 店铺
                    userId = i['shop']['userId']  # 店铺ID
                    shop_uvIndex = i['shop_uvIndex']['value']  # 流量指数
                    shop_seIpvUvHits = i['shop_seIpvUvHits']['value']  # 搜索人气
                    shop_cltHits = i['shop_cltHits']['value']  # 收藏人气
                    shop_cartHits = i['shop_cartHits']['value']  # 加购人气
                    shop_payRateIndex = i['shop_payRateIndex']['value']  # 支付转化指数
                    shop_tradeIndex = i['shop_tradeIndex']['value']  # 交易指数
                    shop_payByrCntIndex = i['shop_payByrCntIndex']['value']  # 客群指数
                    shop_preTradeIndex = 0  # 预售定金指数
                    shop_preSellItmCnt = 0  # 预售定金商品件数
                    shop_fstOnsItmCnt = 0  # 上新商品数
                    TradeIndex = get_change(shop_tradeIndex)  # 交易金额
                    FlowIndex = get_change(shop_uvIndex)  # 访客人数
                    SearchPoplty = get_change(shop_seIpvUvHits)  # 搜索人数
                    cltHits = get_change(shop_cltHits)  # 收藏人数
                    AddCartPoplty = get_change(shop_cartHits)  # 加购人数
                    CVR = get_pay(shop_payRateIndex)  # 支付转化率
                    PayBuyer = get_change(shop_payByrCntIndex)  # 支付人数
                    preTradeIndex = 0  # F_Rest_TradeIndex_New(shop_preTradeIndex)
                    tup1 = (
                        start_day.replace('-', ''), 'ALL', title, userId, 0, TradeIndex, FlowIndex, SearchPoplty,
                        cltHits, AddCartPoplty,
                        CVR, PayBuyer, '%.0f' % shop_uvIndex, '%.0f' % shop_seIpvUvHits, '%.0f' % shop_cltHits,
                        '%.0f' % shop_cartHits,
                        '%.0f' % shop_payRateIndex, '%.0f' % shop_tradeIndex, '%.0f' % shop_payByrCntIndex)
                    print(tup1)
                    if tup1 not in values:
                        values.append(tup1)
                    try:
                        cate_cateRankId = i['cate_cateRankId']['value']  # 行业排名
                    except:
                        cate_cateRankId = 0
                    cate_uvIndex = i['cate_uvIndex']['value']  # 流量指数
                    try:
                        cate_seIpvUvHits = i['cate_seIpvUvHits']['value']  # 搜索人气
                    except:
                        cate_seIpvUvHits = 0
                    cate_cltHits = i['cate_cltHits']['value']  # 收藏人气
                    cate_cartHits = i['cate_cartHits']['value']  # 加购人气
                    cate_payRateIndex = i['cate_payRateIndex']['value']  # 支付转化指数
                    cate_tradeIndex = i['cate_tradeIndex']['value']  # 交易指数
                    cate_payByrCntIndex = i['cate_payByrCntIndex']['value']  # 客群指数
                    TradeIndex = get_change(cate_tradeIndex)  # 交易金额
                    FlowIndex = get_change(cate_uvIndex)  # 访客人数
                    SearchPoplty = get_change(cate_seIpvUvHits)  # 搜索人数
                    cltHits = get_change(cate_cltHits)  # 收藏人数
                    AddCartPoplty = get_change(cate_cartHits)  # 加购人数
                    CVR = get_pay(cate_payRateIndex)  # 支付转化率
                    PayBuyer = get_change(cate_payByrCntIndex)  # 支付人数
                    tup1 = (
                        start_day.replace('-', ''), cateId, title, userId, cate_cateRankId, TradeIndex, FlowIndex,
                        SearchPoplty, cltHits,
                        AddCartPoplty, CVR,
                        PayBuyer, '%.0f' % cate_uvIndex, '%.0f' % cate_seIpvUvHits, '%.0f' % cate_cltHits,
                        '%.0f' % cate_cartHits, '%.0f' % cate_payRateIndex, '%.0f' % cate_tradeIndex,
                        '%.0f' % cate_payByrCntIndex, '', '', '', '')
                    print(tup1)
                    values.append(tup1)
            self._sql_server.save_message('贝德美.dbo.监控店铺_竞店列表_月', values)
            if start_day.replace('-', '') == end_day.replace('-', ''):
                break
            start_day = get_after_month(start_day)
            time.sleep(20)

    def _monitor_stores_list_of_competing_stores_request(self, start_day, cookie, cateId):
        url = 'https://sycm.taobao.com/mc/ci/shop/monitor/listShop.json'
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'bx-ua': '219!88HbA8uIPXX8ADaVmm+SlaHJDrXwq02Vyv/+we3f4qnHZ7PK8uVVXM6MonKFf0U0xDY8jo7/FkQ3swvsZDQKoso4CkvpVm/FhDCfXaA5st9SFib5hFmwN1qkRedlkmt0Zqb1voIX5bO7YHsd+8xjkm2LUzmKneEoUo39NW5h2JKYhzxGjub/wdoXN/O7327Vs/WvijOEWeJ2mo5NsENdgsqA0Pyejkl13I6Em4iGG5gmcvIzH1/+T1z5yD+j5QR5Xk442BGln2obO+iyapbLs/5w6rWpHgs2YhQSBkixrhY+3IoVelOVfmlQX7CMWD3vNRS79H1YTmLThQoUHrCaJf3WDfW0jd/OtRsTFJMPWg/2SqCuixnCSeAWsiBRK0WOSYuA7CKo021bWSSNPT1XorKW0pVP1vqsmvxR74igVPTr+ug21ERCT3RuzCmxVNTVTxL+uSvgfF+a+gFiK3IPjzpBDqh3AmPSAYkMDyvK0A3OqQs1uqkvLWBKTklg2ucDCixNKPaJxMVlRGBsgnKm4kjoXQl4X1zX2s47HO0ID7A2Cp77A9Og1rW2OWW3e0x3BVFAmOLMNtbv1yoKb6Wt3WaNFfs2TXXQkig21ZgSrm6VQzh3gY1Du4qo1NQzW4PVBxkAVZYBpUfnTEZZsxevv1lvBIGIWJhICXdz4YL3tMNcLCxbt3dwUY8fG06Jvwq8qPvTduU7E0vTz2gZZTjT4KbIj4mvlyIWFsfyN0DzLBhzMgdOBSbAVCuCEksFe+Pzy6G3paiRj6etUPIPLe+Ynnt22YYu4ZSGWw3gih6pOKPvl6FdhO1sqfcacz4R4LJXxZ8Obusw8DedLp34gZ2NBh9sZMSeCUrCvDlIy0OFC0q2/lYW8lmOxJsGh17oCVHAZtp/5OKMOBMUhN+AS9Eb+21J8zDHRwjFJWeXes79PYODucx5aKue+rlifg+8T20xRf29d5Q/6T0ins/pS6UGDMr/QcDhjfKNrsp8+ikH0s/9f2prWpNKCLYaU/J2c/6PyEIFVUFR4gDWjl/hoh6WDKc+9PY4IZUMJ9pW10GZGieD12JY7x3t3A8q61OukqfDCAbFo7xVP+JUrar9XiYzFUhAAmGT21//fPaM+BJ2eDODNPQTmz8OhkGZSXi/3/GiMoUrSHFdy6sO+0b94GVqPeH4QO4Dvx8PCDSNXFDcYCBHwo+FFp0EPvgi+U4mFUz6SW22S03+qm94qJ+hE5HHh9lDDZ8shm97Im49arq9J+JYHLNBGfQFAR85xLPGHL9QDI5S+IB05y2K5AZAm1BVIh94UDXnxZY+y4tjzwxru8k4V5yEVNmhx9Kzbwcuwg04tGih5nxT5Wjl5bfDDev=',
            'bx-umidtoken': 'T2gAweTCCH6q_1ZIWFAaktYr11n_E6FhGY89XE8lCjYoUtf2NwOKGQFG_r5aUkzTCZo=',
            'cache-control': 'no-cache',
            'cookie': cookie,
            'onetrace-card-id': 'sycm-mc-ci-shop-monitor',
            'pragma': 'no-cache',
            'referer': 'https://sycm.taobao.com/mc/ci/shop/monitor?cateFlag=1&cateId=50014812&dateRange=2021-12-01%7C2021-12-31&dateType=month&sellerType=-1&spm=a21ag.8718589.TopMenu.d234.279c50a57a2YDy',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sycm-query': 'dateType=month',
            'sycm-referer': '/mc/ci/shop/monitor',
            'transit-id': 'Lgxy6uyTxmkzPPEjgqCKrSCjbIl9vR+PUJyb5L5WoBIPWLhH/2tJgcDFjl40vDYEkiQBcBT6u/60Wt5d7FTPEwB7jNMeML4M+5TSeXytx8whTwsqNmRCbyF7xViwK/uXezHQIExdRP3+ilDBJ7psNdGbBJ2uXZyTDfgo2WkZFaY=',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        params = {
            'dateType': 'month',
            'dateRange': f'{start_day}-01|{get_before_day(get_after_month(start_day) + "-01")}',
            'orderType': 'shop',
            'order': 'desc',
            'orderBy': 'uvIndex',
            'device': '0',
            'cateId': cateId,
            'sellerType': '-1',
            'indexCode': 'uvIndex,tradeIndex,cateRankId',
            'type': 'all',
            '_': '1645586994496',
            'token': '994ffa3dd'
        }
        response = requests.get(url=url, headers=headers, params=params)
        return response

    # 监控店铺_二级流量_月
    def secondary_flow_month_main(self, start_day, end_day, cookie):
        while True:
            if not start_day:
                start_day = self._sql_server.get_start_day('贝德美.dbo.监控店铺_竞店列表_月', '月份', '')
                if start_day == get_before_month(get_month()).replace('-', ''):
                    print('数据抓取完毕')
                    return 0
                start_day = get_after_month(start_day)
            if not end_day:
                end_day = get_before_month(get_month())
            for shop in self.shops:
                response = self._secondary_flow_month_request(self.shops[shop], cookie, start_day)
                datas = response['data']
                msg = decrypt(datas)
                for data in msg:
                    rivalShop1UvIndex = data['rivalShop1UvIndex']['value']  # 流量指数
                    pageName = data['pageName']['value']  # 流量来源
                    rivalShop1PayByrCntIndex = data['rivalShop1PayByrCntIndex']['value']  # 客群指数
                    rivalShop1PayRateIndex = data['rivalShop1PayRateIndex']['value']  # 支付转化指数
                    rivalShop1TradeIndex = data['rivalShop1TradeIndex']['value']  # 交易指数
                    FlowIndex = get_change(rivalShop1UvIndex)  # 访客数
                    PayBuyer = get_change(rivalShop1PayByrCntIndex)  # 买家数
                    CVR = get_pay(rivalShop1PayRateIndex)  # 支付转化率
                    TradeIndex = get_change(rivalShop1TradeIndex)  # 交易金额
                    value = (
                        start_day, shop, self.shops[shop], pageName, FlowIndex, PayBuyer, CVR, TradeIndex,
                        rivalShop1UvIndex,
                        rivalShop1PayByrCntIndex,
                        rivalShop1PayRateIndex, rivalShop1TradeIndex)
                    self._sql_server.save_message('贝德美.dbo.监控店铺_二级流量_无线_月', [value])
                    for n_data in data['children']:
                        n_rivalShop1UvIndex = n_data['rivalShop1UvIndex']['value']  # 流量指数
                        n_pageName = n_data['pageName']['value']  # 流量来源
                        n_rivalShop1PayByrCntIndex = n_data['rivalShop1PayByrCntIndex']['value']  # 客群指数
                        n_rivalShop1PayRateIndex = n_data['rivalShop1PayRateIndex']['value']  # 支付转化指数
                        n_rivalShop1TradeIndex = n_data['rivalShop1TradeIndex']['value']  # 交易指数
                        n_FlowIndex = get_change(n_rivalShop1UvIndex)  # 访客数
                        n_PayBuyer = get_change(n_rivalShop1PayByrCntIndex)  # 买家数
                        n_CVR = get_pay(n_rivalShop1PayRateIndex)  # 支付转化率
                        n_TradeIndex = get_change(n_rivalShop1TradeIndex)  # 交易金额
                        n_value = (
                            start_day, shop, self.shops[shop], n_pageName, n_FlowIndex, n_PayBuyer, n_CVR, n_TradeIndex,
                            n_rivalShop1UvIndex, n_rivalShop1PayByrCntIndex,
                            n_rivalShop1PayRateIndex, n_rivalShop1TradeIndex
                        )
                        print(n_value)
                        self._sql_server.save_message('贝德美.dbo.监控店铺_二级流量_无线_月', [n_value])
                time.sleep(5)
            if start_day.replace('-', '') == end_day.replace('-', ''):
                break
            start_day = get_after_month(start_day)
            time.sleep(20)

    def _secondary_flow_month_request(self, shop_id, cookie, start_month):
        url = 'https://sycm.taobao.com/mc/rivalShop/analysis/getFlowSource.json'
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'bx-ua': '221!uMCu++JiFSOZYj4iGU0JCWJ28RTJASlKMK/AOYPdpj+opvZSayTHHc0T1jBx6z9yPcNXUylVcbFfMwQ6dms6wxisPaw5lGh2hwqBZvLEvPjYUNUAf20x1l0S+Tc0G7tx+eZEoZBkprfpxeR2XRIErZzxNDrbA5Ij8h4foO6wa2KqBgEUKypJgW/d5kGDd/h0+Oc5u4/sQkhN2xAYWaWN/sqd6geRby6OatTIpdXEeu5MnBIJ+BpxnZAyttn+SpYu8cBdlrw2dLLjqvkPCb4Dz3b3bBNy9rn2xAzf3poJxB/D63iWNcjCMa7wU+TqWk71bu7bMwFP/Ew8P/9pueOvbhGQhueqAH9FXP5C71AKbYyuqZSsd2oBTeefAhh+qhzLmSuwOehCVZAL+NiD8c105fn1N0PoPz2+FDvAclgfC8pVNEU++znrc5PWhPIyB8hKY2x01jEX7R9t/oM0svPvJbCESxwlMaHMxciMtlzBZZhzp0952TLly3/s/u3ZgmNW8zMiSeZ745mYhLnZsRu7apvapqeQJZCOBNj1zua5+tdzqIeortm9A6SucfDDPZCwKbsvKOFQJl8vdTJjy9IOL1QU6GuxTQaFuPnN34DfWlfi8BPTk6UnuF72/dT028Kz5sSlxdhh+SqOnxX8EaXN167Vkmm+vizMbEdO+Y+pQt8DJGFlUDLgBbEy88iflZohi/CG+cBXWell0yQ2dPlTaFZb8A0viSrd62Ujm/B8NYlxK17kmhxepBJIlPhgZSWskyDHdK78hTFNRjQ5D+p5Uztv5bFq2bpOlVA8ffP8gJG4lWQCtwmi/L3rARNeiyTL0L6GGSEN/IdMa+yQIBCbhcOHllKNuqonidcyCjuJF+iJ9rFbG7gnNNlj0WBu7rYIMrvVAEF1Fi8PrcTqxW9ssRB/3YYoFvT1KE7I66LejxQYkvNNtD0ypAGsaumwuPLS6AKg9717iLhQupUggE8rbskH2xz2/mCe4LOWmWxsbv6Ppbz2t89WKzjY9SV6pIwnJoph8WIIRj4yTp0p/CHLheLacRLnOOXIjxp98WT8Pjz9+rhv+Il1cKAXMUmaMmhsMJID0dS4C5lo0KBYZVEdyLOa3j0elDNy87fLRSTLfIM21EjnEMMUdx+HTDg4uuq7Bu1SiRymdmS9WMfimONdpAVrx5rxbZ9tQr9H2BO2AtBy/fQV48jggzoQuMKnlS8HSn/AAxUarprIV9BDuf5ZACrjXuckO4pDGmZhzEchUXh8lBEbKtQbyt5Ef4DlOvXzkbAkT2zLwJksRFdJCdQhBh3/dj96OXi3rYSe+PqLrcH/GxyvZ7CbBsaYOkbqdta5Fa7yBHyQjY00wdA2',
            'bx-umidtoken': 'T2gA9hbwdUG5DNWyZVGvKUIMZPsbcxe1QrnC-dWEd2X0L_5ez8RChqQBxTb81W8qfRw=',
            'cache-control': 'no-cache',
            'cookie': cookie,
            'onetrace-card-id': 'sycm-mc-ci-shop-analysis.sycm-mc-ci-shop-analysis-source',
            'pragma': 'no-cache',
            'referer': 'https://sycm.taobao.com/mc/ci/shop/analysis?cateFlag=1&cateId=50014812&dateRange=2022-02-01%7C2022-02-28&dateType=month&rivalUser1Id=2616970884&rivalUser2Id=&spm=a21ag.11815275.completeShop.5.489550a52y5b4Q',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sycm-query': 'dateType=month',
            'sycm-referer': '/mc/ci/shop/analysis',
            'transit-id': 'aMf2Zp/o/stiDjawP3jheeXl1NCPfiLREU+GfFL8dCxSQaj83LC9mllZitutwDI1fDJnG2hRlAJFKKOd1Jdd9Vz/yoKF7ZnDCOd20mouOxcnhtYPyuA8NuzoYItjApo+LpC7IJoFAgRBj7Rc1P5aQY8mChP2KLqYbErnDLoTsdY=',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        params = {
            'cateId': '50014812',
            'selfUserId': '4224382495',
            'rivalUser1Id': shop_id,
            'device': '2',
            'dateType': 'month',
            'dateRange': f'{start_month[:-2] + "-" + start_month[-2:] + "-01"}|{get_before_day(get_after_month(start_month) + "-01")}',
            'indexCode': 'uvIndex',
            'orderBy': 'uvIndex',
            'order': 'desc',
            '_': '1646124177924',
            'token': '907dcbf34'
        }
        response = requests.get(url=url, headers=headers, params=params).json()
        return response

    # 市场大盘_全网_类目_月
    def market_network_category_month_start_main(self, childid, end_month, start_month, dts_cookie, cookie):
        all_childid_ids = self.all_categories_of_the_market(cookie)
        print(all_childid_ids)
        if childid == 50014812 or childid == 50022517:
            print(f'一级类目：{childid}')
            self.monthly_market_request(childid, dts_cookie, start_month, end_month, cookie)
        else:
            for i in all_childid_ids:
                print(i[0], i[1], childid)
                print(i)
                if i[0] == childid:
                    print(f'二级类目：{childid} ------> {i[2]} {i[1]}')
                    self.monthly_market_request(i[1], dts_cookie, start_month, end_month, cookie)
                    time.sleep(10)
                if i[1] == childid:
                    print(f'叶子类目：{childid} ------> {i[2]} {i[1]} {i[-1]}')
                    self.monthly_market_request(i[1], dts_cookie, start_month, end_month, cookie)
                    time.sleep(20)

    # 市场大盘所有类目
    def all_categories_of_the_market(self, cookie):
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

    # 市场大盘月度
    def monthly_market_request(self, cateid, dts_cookie, start_month, end_month, cookie):
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
        infos = ['seIpvUvHits', 'sePvIndex', 'uvHits', 'pvHot', 'cltHits', 'cltHot', 'cartHits', 'cartHot',
                 'payByrCntIndex', 'tradeIndex']
        value = []
        for info in infos:
            value.append(self.change_info(cateid, [info, int(datas[info]['value'])], dts_cookie))
        values = [start_month.replace('-', ''), cateid] + value + [seIpvUvHits, sePvIndex, uvHits, pvHot, cltHits,
                                                                   cltHot, cartHits, cartHot, payByrCntIndex,
                                                                   tradeIndex]
        self._sql_server.save_message('贝德美.dbo.市场大盘_全网_类目_月', [tuple(values)])

    # 店透视
    def change_info(self, cateid, value, dts_cookie):
        # values = []
        # for i in value:
        #     values.append(str(int(i)))
        url = 'https://diantoushi.com/switch/v2/change'
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-length': '63',
            'content-type': 'application/json',
            'cookie': dts_cookie,
            'origin': 'https://www.diantoushi.com',
            'pragma': 'no-cache',
            'referer': 'https://www.diantoushi.com/index.html',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        data = {"categoryId": "", "changeType": "2",
                "indexTrans": '[{"' + value[0] + '":"' + str(value[1]) + '","num":1}]'}
        # data = {"categoryId": cateid, "changeType": "1", "indexTrans": '[{"' + value[0] + '":"' + str(value[1]) + '","num":1}]'}
        response = requests.post(url=url, headers=headers, json=data).json()
        return response['data'][0][value[0] + 'Change']

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

    #  贝德美.dbo.市场排行_商品_高流量_天猫_类目_月
    def market_ranking_commodity_high_flow_tmall_category_month_main(self, start_day, cateid, cookie):
        response = self._market_ranking_commodity_high_flow_tmall_category_month_request(cateid, start_day, cookie)
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

            value = (
            start_day.replace('-', ''), cateid, item_title, shop_title, item_itemId, num, self.get_change(uvIndex),
            self.get_change(seIpvUvHits), self.get_change(tradeIndex), uvIndex, seIpvUvHits, tradeIndex)
            self._sql_server.save_message('贝德美.dbo.市场排行_商品_高流量_天猫_类目_月', [value])
            num += 1

    def _market_ranking_commodity_high_flow_tmall_category_month_request(self, cateId, start_day, cookie):
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
            'dateRange': f'{start_day}-01|{get_before_day(get_after_month(start_day) + "-01")}',
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

    # 市场排行_商品_高交易_天猫_类目_月
    def market_ranking_commodity_high_transaction_tmall_category_month_main(self, start_day, cateId, cookie):
        response = self._market_ranking_commodity_high_transaction_tmall_category_month_request(cateId, start_day,
                                                                                                cookie)
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
                start_day.replace('-', ''), cateId, item_title, shop_title, item_itemId, num,
                self.get_change(tradeIndex), self._get_pay(payRateIndex), tradeIndex, payRateIndex)
            self._sql_server.save_message('贝德美.dbo.市场排行_商品_高交易_天猫_类目_月', [value])
            num += 1

    def _market_ranking_commodity_high_transaction_tmall_category_month_request(self, cateId, start_day, cookie):
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
            'dateRange': f'{start_day}-01|{get_before_day(get_after_month(start_day) + "-01")}',
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

    def _get_pay(self, x):
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

    # 获取直通车token
    def get_subway_token(self, cookie):
        url = 'https://subway.simba.taobao.com/bpenv/getLoginUserInfo.htm'
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9',
            'bx-v': '2.2.0',
            'content-length': '0',
            'cookie': cookie,
            'origin': 'https://subway.simba.taobao.com',
            'referer': 'https://subway.simba.taobao.com/index.jsp',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        response = requests.post(url=url, headers=headers)
        print(response.text)
        response = response.json()['result']['token']
        return response

    # 贝德美.dbo.直通车_账户报表
    def through_train_account_statement_main(self, start_day, end_day, cookie, table, token):
        sql = f"""delete from {table} where 转化周期 < 30"""
        self._sql_server.check_message(sql, 2)
        if not start_day:
            start_day = self._sql_server.get_start_day(table, '日期', '')
            print(start_day)
            if start_day == get_before_day(get_today()):
                return 0
            start_day = get_after_day(start_day)
        if not end_day:
            end_day = get_today()
        page = 1
        while True:
            response = self._through_train_account_statement_request(page, start_day, end_day, cookie, token)
            if not response:
                break
            for data in response:
                print(data)
                thedate = data['thedate']  # 日期
                try:
                    impression = data['impression']  # 展现量
                except:
                    impression = None
                try:
                    click = data['click']  # 点击量
                except:
                    click = None
                try:
                    costInYuan = data['costInYuan']  # 花费
                except:
                    costInYuan = None
                try:
                    cli = round(float(click) / float(impression), 4)  # 点击率
                except:
                    cli = None
                try:
                    cpcInYuan = data['cpcInYuan']  # 平均点击花费
                except:
                    cpcInYuan = None
                try:
                    cpmInYuan = data['cpmInYuan']  # 千次展现花费
                except:
                    cpmInYuan = None
                try:
                    favTotal = data['favTotal']  # 总收藏数
                except:
                    favTotal = None
                try:
                    favItemTotal = data['favItemTotal']  # 收藏宝贝数
                except:
                    favItemTotal = None
                try:
                    favShopTotal = data['favShopTotal']  # 收藏店铺数
                except:
                    favShopTotal = None
                try:
                    cartTotal = data['cartTotal']  # 总购物车数
                except:
                    cartTotal = None
                try:
                    directCartTotal = data['directCartTotal']  # 直接购物车数
                except:
                    directCartTotal = None
                try:
                    indirectCartTotal = data['indirectCartTotal']  # 简接购物车数
                except:
                    indirectCartTotal = None
                try:
                    cartTotalCost = round(float(data['cartTotalCost']) / 100, 2)  # 加购成本
                except:
                    cartTotalCost = None
                try:
                    favItemTotalCostInYuan = data['favItemTotalCostInYuan']  # 宝贝收藏成本
                except:
                    favItemTotalCostInYuan = None
                try:
                    favItemTotalCoverage = round(float(data['favItemTotalCoverage']) / 100, 4)  # 宝贝收藏率
                except:
                    favItemTotalCoverage = None
                try:
                    cartTotalCoverage = round(float(data['cartTotalCoverage']) / 100, 4)  # 加购率
                except:
                    cartTotalCoverage = None
                try:
                    eprePayAmtInYuan = data['eprePayAmtInYuan']  # 总预售成交金额
                except:
                    eprePayAmtInYuan = None
                try:
                    indirEprePayCnt = data['indirEprePayCnt']  # 总预售成交笔数
                except:
                    indirEprePayCnt = None
                try:
                    zhijieyus = 0  # 直接预售成交金额
                except:
                    zhijieyus = None
                zhijiebs = 0  # 直接预售成交笔数
                try:
                    indirEprePayAmtInYuan = data['indirEprePayAmtInYuan']  # 间接预售成交金额
                except:
                    indirEprePayAmtInYuan = None
                try:
                    eprePayCnt = data['eprePayCnt']  # 间接预售成交笔数
                except:
                    eprePayCnt = None
                try:
                    transactionTotalInYuan = data['transactionTotalInYuan']  # 总成交金额
                except:
                    transactionTotalInYuan = None
                try:
                    directTransactionInYuan = data['directTransactionInYuan']  # 直接成交金额
                except:
                    directTransactionInYuan = None
                try:
                    indirectTransactionInYuan = data['indirectTransactionInYuan']  # 间接成交金额
                except:
                    indirectTransactionInYuan = None
                try:
                    transactionShippingTotal = data['transactionShippingTotal']  # 总成交笔数
                except:
                    transactionShippingTotal = None
                try:
                    directTransactionShipping = data['directTransactionShipping']  # 直接成交笔数
                except:
                    directTransactionShipping = None
                try:
                    indirectTransactionShipping = data['indirectTransactionShipping']  # 间接成交笔数
                except:
                    indirectTransactionShipping = None
                try:
                    trc = float(transactionTotalInYuan) / float(costInYuan)  # 投入产出比
                except:
                    trc = None
                try:
                    coverage = round(float(data['coverage']) / 100, 4)  # 点击转化率
                except:
                    coverage = None
                try:
                    zjdjzhl = round(float(directTransactionShipping) / float(click), 4)  # 直接点击转化率
                except:
                    zjdjzhl = None
                try:
                    clickShoppingNum = data['clickShoppingNum']  # 购物金充值笔数
                except:
                    clickShoppingNum = None
                try:
                    clickShoppingAmtInYuan = float(data['clickShoppingAmtInYuan']) / 100  # 购物金充值金额
                except:
                    clickShoppingAmtInYuan = None
                try:
                    searchImpression = data['searchImpression']  # 自然流量曝光
                except:
                    searchImpression = None
                try:
                    searchTransactionInYuan = data['searchTransactionInYuan']  # 自然流量转化金额
                except:
                    searchTransactionInYuan = None
                tqdjje = None  # 特权订金金额
                wkje = None  # 尾款金额
                ykjje = None  # 一口价金额
                try:
                    newAlipayUv = data['newAlipayUv']  # 新成交用户数
                except:
                    newAlipayUv = None
                try:
                    newAlipayUvRate = float(data['newAlipayUvRate']) / 100  # 新成交用户占比
                except:
                    newAlipayUvRate = None
                try:
                    favAndCartTotal = data['favAndCartTotal']  # 总收藏加购数
                except:
                    favAndCartTotal = None
                try:
                    cof = round(float(costInYuan) / float(favAndCartTotal), 4)  # 总收藏加购成本
                except:
                    cof = None
                try:
                    favItemAndCartTotal = data['favItemAndCartTotal']  # 宝贝收藏加购数
                except:
                    favItemAndCartTotal = None
                try:
                    cofa = round(float(costInYuan) / float(favItemAndCartTotal), 4)  # 宝贝收藏加购成本
                except:
                    cofa = None

                change_day = int((get_time_number(get_today()) - get_time_number(thedate)) / 60 / 60 / 24)
                change_week = 30 if change_day >= 30 else change_day
                value = (
                    change_week, thedate, impression, click, costInYuan, cli, cpcInYuan, cpmInYuan, favTotal,
                    favItemTotal, favShopTotal, cartTotal, directCartTotal, indirectCartTotal, cartTotalCost,
                    favItemTotalCostInYuan, favItemTotalCoverage, cartTotalCoverage,
                    eprePayAmtInYuan, indirEprePayCnt, zhijieyus, zhijiebs, indirEprePayAmtInYuan,
                    eprePayCnt, transactionTotalInYuan, directTransactionInYuan, indirectTransactionInYuan,
                    transactionShippingTotal, directTransactionShipping, indirectTransactionShipping, trc,
                    coverage, zjdjzhl, clickShoppingNum, clickShoppingAmtInYuan,
                    searchImpression, searchTransactionInYuan, tqdjje, wkje, ykjje,
                    newAlipayUv, newAlipayUvRate, favAndCartTotal, cof, favItemAndCartTotal, cofa)
                self._sql_server.save_message(table, [value])
            page += 1

    def _through_train_account_statement_request(self, page, start_day, end_day, cookie, token):
        url = 'https://subway.simba.taobao.com/openapi/param2/1/gateway.subway/rpt/rptCustomerList$'
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9',
            'bx-v': '2.2.0',
            'cache-control': 'no-cache',
            'content-length': '522',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': cookie,
            'origin': 'https://subway.simba.taobao.com',
            'pragma': 'no-cache',
            'referer': 'https://subway.simba.taobao.com/index.jsp',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        data = {
            'queryParam': '{"page":"' + str(
                page) + '","pageSize":"100","startDate":"' + start_day + '","endDate":"' + end_day + '","effectEqual":"30","pvType":["1","4","2","5","6"],"sortField":"cost","sortType":"desc"}',
            'sla': 'json',
            'isAjaxRequest': 'true',
            'token': token,
            '_referer': f'/report/bpreport/index?page=1&start={start_day}&end={end_day}&effect=30&pageSize=100&orderField=cost&orderBy=desc',
            'sessionId': 'tnjkrgcndd'
        }
        response = requests.post(url=url, headers=headers, data=data)
        print(response.text)
        response = response.json()
        return response['result']['data']

    # 贝德美.dbo.直通车_单元报表
    def through_train_cell_report_main(self, start_day, end_day, cookie, token):
        sql = f"""delete from 贝德美.dbo.直通车_单元报表 where 转化周期 < 30"""
        self._sql_server.check_message(sql, 2)
        if not start_day:
            start_day = self._sql_server.get_start_day('贝德美.dbo.直通车_单元报表', '日期', '')
            print(start_day)
            if start_day == get_before_day(get_today()):
                return 0
            start_day = get_after_day(start_day)
        if not end_day:
            end_day = get_today()
        self._through_train_cell_report_request(start_day, end_day, cookie, token)
        res = un_zip('单元.zip')
        for file_path in res:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                values = {}
                for row in reader:
                    save_value = []
                    for i in row:
                        if not i:
                            i = None
                        save_value.append(i)
                    if save_value[0] == '\ufeff日期':
                        continue
                    change_day = int((get_time_number(get_today()) - get_time_number(save_value[0])) / 60 / 60 / 24)
                    try:
                        save_value[10] = round(float(save_value[10]) / 100, 4)
                    except:
                        pass
                    save_value[0] = str(save_value[0])
                    if save_value[0] not in values:
                        values[save_value[0]] = []
                    try:
                        save_value[21] = round(float(save_value[21]) / 100, 4)
                    except:
                        pass
                    try:
                        save_value[22] = round(float(save_value[22]) / 100, 4)
                    except:
                        pass
                    try:
                        save_value[36] = round(float(save_value[36]) / 100, 4)
                    except:
                        pass
                    change_week = 30 if change_day >= 30 else change_day
                    save_value.insert(0, change_week)
                    values[save_value[1]].append(tuple(save_value))
                for value in values:
                    ur_cost = 0
                    for data in values[value]:
                        ur_cost += float(data[10])
                    ur_costs = self._check_unit_report_msg(value)[0]
                    print(ur_costs, ur_cost, value)
                    if abs(float(ur_costs) - ur_cost) < 1:
                        self._sql_server.save_message('贝德美.dbo.直通车_单元报表', values[value])
                    else:
                        raise '花费不一致'
            f.close()
            os.remove(file_path)

    def _through_train_cell_report_request(self, start_day, end_day, cookie, token):
        url = 'https://subway.simba.taobao.com/reportdownload/addMultiTask.htm'
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9',
            'bx-v': '2.2.0',
            'cache-control': 'no-cache',
            'content-length': '299',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': cookie,
            'origin': 'https://subway.simba.taobao.com',
            'pragma': 'no-cache',
            'referer': 'https://subway.simba.taobao.com/index.jsp',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        data = {
            'fileName': f'{start_day}',
            'dimension': '[103]',
            'startDate': start_day,
            'endDate': end_day,
            'transactionCycle': '30',
            'aggregationMode': '2',
            'sla': 'json',
            'isAjaxRequest': 'true',
            'token': token,
            '_referer': '/report/bpreport/adgroup/index?page=1&effect=30&start=2022-07-20&end=2022-07-20',
            'sessionId': 'ct4fr1rkoa8'
        }
        response = requests.post(url=url, headers=headers, data=data).text
        print(response)
        time.sleep(10)
        page = 1
        while True:
            url1 = 'https://subway.simba.taobao.com/reportdownload/getdownloadTasks.htm'
            headers = {
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'accept-language': 'zh-CN,zh;q=0.9',
                'bx-v': '2.2.0',
                'cache-control': 'no-cache',
                'content-length': '160',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'cookie': cookie,
                'origin': 'https://subway.simba.taobao.com',
                'pragma': 'no-cache',
                'referer': 'https://subway.simba.taobao.com/index.jsp',
                'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': 'Windows',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest'
            }
            data = {
                'pageSize': '20',
                'pageNumber': f'{page}',
                'sla': 'json',
                'isAjaxRequest': 'true',
                'token': token,
                '_referer': '/report/bpreport/download-list?rows=20&page=38',
                'sessionId': 'ct4fr1rkoa8'
            }
            response = requests.post(url=url1, headers=headers, data=data).json()
            datas = response['result']['items']
            print(datas)
            data = datas[-1]
            taskId = data['id']
            custId = data['custId']
            fileName = data['fileName']
            print(fileName, str(start_day) + '_单元')
            if fileName != str(start_day) + '_单元':
                print(response['result']['totalItem'], response['result']['pageSize'])
                p = int(response['result']['totalItem']) / int(response['result']['pageSize'])
                if p > int(int(response['result']['totalItem']) / int(response['result']['pageSize'])):
                    p = int(int(response['result']['totalItem']) / int(response['result']['pageSize'])) + 1
                else:
                    p = int(int(response['result']['totalItem']) / int(response['result']['pageSize']))
                page = p
                continue
            down_url = f'https://download-subway.simba.taobao.com/download.do?spm=a2e2i.23211836.ce272de26.d5325113b.67c368f8vEF3oc&custId={custId}&token=f6f29d12&taskId={taskId}'
            headers = {
                'Host': 'download-subway.simba.taobao.com',
                'Connection': 'keep-alive',
                'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': 'Windows',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Sec-Fetch-Site': 'same-site',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Dest': 'document',
                'Referer': 'https://subway.simba.taobao.com/',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cookie': cookie
            }
            cont = requests.get(url=down_url, headers=headers).content
            with open('单元.zip', 'wb') as w:
                w.write(cont)
            w.close()
            break

    # 贝德美.dbo.直通车_关键词报表
    def through_train_keyword_report_main(self, start_day, cookie, end_day, token):
        sql = f"""delete from 贝德美.dbo.直通车_关键词报表 where 转化周期 < 30"""
        self._sql_server.check_message(sql, 2)
        if not start_day:
            start_day = self._sql_server.get_start_day('贝德美.dbo.直通车_关键词报表', '日期', '')
            print(start_day)
            if start_day == get_before_day(get_today()):
                return 0
            start_day = get_after_day(start_day)
        if not end_day:
            end_day = get_today()
        self._through_train_keyword_report_request(start_day, cookie, end_day, token)
        res = un_zip('关键词.zip')
        for file_path in res:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                values = {}
                for row in reader:
                    save_value = []
                    for i in row:
                        if not i:
                            i = None
                        save_value.append(i)
                    if save_value[0] == '\ufeff日期':
                        continue
                    change_day = int((get_time_number(get_today()) - get_time_number(save_value[0])) / 60 / 60 / 24)
                    try:
                        save_value[11] = round(float(save_value[11]) / 100, 4)
                    except:
                        pass
                    save_value[0] = str(save_value[0])
                    if save_value[0] not in values:
                        values[save_value[0]] = []
                    try:
                        save_value[22] = round(float(save_value[22]) / 100, 4)
                    except:
                        pass
                    try:
                        save_value[23] = round(float(save_value[23]) / 100, 4)
                    except:
                        pass
                    try:
                        save_value[37] = round(float(save_value[37]) / 100, 4)
                    except:
                        pass
                    try:
                        save_value[38] = round(float(save_value[38]) / 100, 4)
                    except:
                        pass
                    change_week = 30 if change_day >= 30 else change_day
                    save_value.insert(0, change_week)
                    try:
                        good_id = self._check_good_id(save_value[5], start_day)[0]
                    except:
                        good_id = None
                    save_value.insert(7, good_id)
                    # print(save_value)
                    values[save_value[1]].append(tuple(save_value))
                for value in values:
                    ur_cost = 0
                    for data in values[value]:
                        # print(data)
                        ur_cost += float(data[12])
                    ur_costs = self._check_unit_report_msg(value)[0]
                    # print(ur_costs, ur_cost, value)
                    if abs(float(ur_costs) - ur_cost) < 1:
                        self._sql_server.save_message('贝德美.dbo.直通车_关键词报表', values[value])
                    else:
                        raise '花费不一致'
            f.close()
            os.remove(file_path)

    def _through_train_keyword_report_request(self, start_day, cookie, end_day, token):
        url = 'https://subway.simba.taobao.com/reportdownload/addMultiTask.htm'
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9',
            'bx-v': '2.2.0',
            'cache-control': 'no-cache',
            'content-length': '299',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': cookie,
            'origin': 'https://subway.simba.taobao.com',
            'pragma': 'no-cache',
            'referer': 'https://subway.simba.taobao.com/index.jsp',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        data = {
            'fileName': f'{start_day}',
            'dimension': '[104]',
            'startDate': start_day,
            'endDate': end_day,
            'transactionCycle': '30',
            'aggregationMode': '2',
            'sla': 'json',
            'isAjaxRequest': 'true',
            'token': token,
            '_referer': '/report/bpreport/keyword/index?page=1&effect=30&start=2022-06-22&end=2022-07-21',
            'sessionId': 'ct4fr1rkoa8'
        }
        response = requests.post(url=url, headers=headers, data=data).text
        print(response)
        time.sleep(10)
        page = 1
        while True:
            url1 = 'https://subway.simba.taobao.com/reportdownload/getdownloadTasks.htm'
            headers = {
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'accept-language': 'zh-CN,zh;q=0.9',
                'bx-v': '2.2.0',
                'cache-control': 'no-cache',
                'content-length': '160',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'cookie': cookie,
                'origin': 'https://subway.simba.taobao.com',
                'pragma': 'no-cache',
                'referer': 'https://subway.simba.taobao.com/index.jsp',
                'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': 'Windows',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest'
            }
            data = {
                'pageSize': '20',
                'pageNumber': f'{page}',
                'sla': 'json',
                'isAjaxRequest': 'true',
                'token': token,
                '_referer': '/report/bpreport/download-list?rows=20&page=38',
                'sessionId': 'ct4fr1rkoa8'
            }
            response = requests.post(url=url1, headers=headers, data=data).json()
            datas = response['result']['items']
            print(datas)
            data = datas[-1]
            taskId = data['id']
            custId = data['custId']
            fileName = data['fileName']
            print(fileName, str(start_day) + '_关键词')
            if fileName != str(start_day) + '_关键词':
                print(response['result']['totalItem'], response['result']['pageSize'])
                p = int(response['result']['totalItem']) / int(response['result']['pageSize'])
                if p > int(int(response['result']['totalItem']) / int(response['result']['pageSize'])):
                    p = int(int(response['result']['totalItem']) / int(response['result']['pageSize'])) + 1
                else:
                    p = int(int(response['result']['totalItem']) / int(response['result']['pageSize']))
                page = p
                continue
            down_url = f'https://download-subway.simba.taobao.com/download.do?spm=a2e2i.23211836.ce272de26.d5325113b.67c368f8vEF3oc&custId={custId}&token=f6f29d12&taskId={taskId}'
            headers = {
                'Host': 'download-subway.simba.taobao.com',
                'Connection': 'keep-alive',
                'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': 'Windows',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Sec-Fetch-Site': 'same-site',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Dest': 'document',
                'Referer': 'https://subway.simba.taobao.com/',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cookie': cookie
            }
            cont = requests.get(url=down_url, headers=headers).content
            with open('关键词.zip', 'wb') as w:
                w.write(cont)
            w.close()
            break

    # 检查商品id
    def _check_good_id(self, dy_id, start_day):
        sql = f"SELECT top 1 商品id FROM [dbo].[直通车_单元报表] where 单元ID='{dy_id}'"
        return self._sql_server.check_message(sql, 0)

    # 检查单元
    def _check_unit_report_msg(self, start_day):
        sql = f"select 花费 from 贝德美.dbo.直通车_账户报表 where 日期='{start_day}'"
        return self._sql_server.check_message(sql, 0)

    # 直通车账号检查
    def check_user(self, cookie, shop_name):
        url = 'https://subway.simba.taobao.com/bpenv/getLoginUserInfo.htm'
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9',
            'bx-v': '2.2.3',
            'cache-control': 'no-cache',
            'content-length': '0',
            'cookie': cookie,
            'origin': 'https://subway.simba.taobao.com',
            'pragma': 'no-cache',
            'referer': 'https://subway.simba.taobao.com/index.jsp',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        response = requests.get(url=url, headers=headers).json()
        print(response['result']['nickName'], shop_name)
        if response['result']['nickName'] != shop_name:
            raise '账户错误'

    # 获取市场大盘的所有类目
    def _get_ids(self, cookie):
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
        return response

    # 循环获取市场大盘id
    def market_ranking_brand_high_transaction_tmall_category_month_start(self, cateid, start_day, cookie, end_day):
        all_childid_ids = self._get_ids(cookie)
        if isinstance(cateid, list):
            for ca_id in cateid:
                print(ca_id)
                if ca_id == 50014812 or ca_id == 50022517:
                    print(f'一级类目：{ca_id}')
                    self._market_ranking_brand_high_transaction_tmall_category_month_main(start_day, end_day, ca_id,
                                                                                          cookie)
                else:
                    for i in all_childid_ids:
                        print(i[0], i[1], ca_id)
                        print(i)
                        if i[0] == ca_id:
                            print(f'二级类目：{ca_id} ------> {i[2]} {i[1]}')
                            self._market_ranking_brand_high_transaction_tmall_category_month_main(start_day, end_day,
                                                                                                  i[1],
                                                                                                  cookie)
                        if i[1] == ca_id:
                            print(f'叶子类目：{ca_id} ------> {i[2]} {i[1]} {i[-1]}')
                            self._market_ranking_brand_high_transaction_tmall_category_month_main(start_day, end_day,
                                                                                                  i[1],
                                                                                                  cookie)
        else:
            if cateid == 50014812 or cateid == 50022517:
                print(f'一级类目：{cateid}')
                self._market_ranking_brand_high_transaction_tmall_category_month_main(start_day, end_day, cateid, cookie)
            else:
                # a = 0
                for i in all_childid_ids:
                    # sql = 'select * from 贝德美.dbo.市场大盘_全网_类目_月 where'
                    print(i[0], i[1], cateid)
                    print(i)
                    if i[0] == cateid:
                        print(f'二级类目：{cateid} ------> {i[2]} {i[1]}')
                        self._market_ranking_brand_high_transaction_tmall_category_month_main(start_day, end_day, i[0],
                                                                                              cookie)
                    if i[1] == cateid:
                        print(f'叶子类目：{cateid} ------> {i[2]} {i[1]} {i[-1]}')
                        self._market_ranking_brand_high_transaction_tmall_category_month_main(start_day, end_day, i[1],
                                                                                              cookie)

    # 市场排行_品牌_高交易_天猫_类目_月
    def _market_ranking_brand_high_transaction_tmall_category_month_main(self, start_day, end_day, cateId, cookie):
        if not start_day:
            start_day = self._sql_server.get_start_day('贝德美.dbo.市场排行_品牌_高交易_天猫_类目_月', '月份', '')
            if start_day == end_day:
                print('<贝德美.dbo.市场排行_品牌_高交易_天猫_类目_月>本月数据已更新')
                return 0
        if not end_day:
            end_day = get_before_month(get_month())
        while True:
            print(start_day, end_day)
            sql = f"select top 1 * from 贝德美.dbo.市场排行_品牌_高交易_天猫_类目_月 where 月份='{start_day.replace('-', '')}' and 类目ID='{cateId}'"
            res = self._sql_server.check_message(sql, 0)
            if not res:
                response = self._market_ranking_brand_high_transaction_tmall_category_month_request(cookie, cateId,
                                                                                                    start_day)
                data = response['data']
                datas = decrypt(data)
                for data in datas:
                    brandName = data['brandModel']['brandName']  # 店铺名称
                    brandId = data['brandModel']['brandId']  # 店铺id
                    cateRankId = data['cateRankId']['value']  # 交易排名
                    tradeIndex = data['tradeIndex']['value']  # 交易指数
                    tradeGrowthRange = data['tradeGrowthRange']['value']  # 交易增长幅度
                    payRateIndex = round(float(data['payRateIndex']['value']), 0)  # 支付转化指数
                    tradeIndex1 = self.change_info(cateId, ['tradeIndex', tradeIndex], dts_cookie)  # 交易金额
                    payRateIndex1 = round(float(
                        self.change_info(cateId, ['payRateIndex', data['payRateIndex']['value']],
                                         dts_cookie).replace('%', '')) / 100, 4)  # 支付转化率
                    value = (start_day.replace('-', ''), cateId, brandName, brandId, cateRankId, tradeIndex1,
                             tradeGrowthRange, payRateIndex1, tradeIndex, payRateIndex)
                    self._sql_server.save_message('贝德美.dbo.市场排行_品牌_高交易_天猫_类目_月', [value])
            if start_day == end_day:
                break
            start_day = get_after_month(start_day)
            time.sleep(3)

    def _market_ranking_brand_high_transaction_tmall_category_month_request(self, cookie, cateId, start_day):
        url = 'https://sycm.taobao.com/mc/mq/mkt/rank/brand/hotsale.json'
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'bx-ua': '223!g2ICro+RurXgGCgyyg67xMFGrOX+xO6SoGmrPzgd4sAthxinwkCUmgp1O6GSWPGi36WXH5Q23Cf/AsTegMBl4VFuUoM8EGDs73aivw7S3Psn1zTJx/uoR7iWJ1h/exX4cgRTW1TkrWW4chcO7+lycQQ4z8G/e6o4MfRpWSh3r2/cPKKHgUN4sbhPz62/fgR4cgRCWd9Fz1aKcAcOe1l4rQQczsi/ejW4cgypWGh/rQR4+DW48llCP5u+qlG08h+WzdSI5vU/SYXV8AQR5HckPH3/3XgnN9nFgrCzWWn7dmfypi4oUo/IjJuyvXsdZjy6lsbnFtGJhh1jNBk+V6M7PJV9foTJf4fScMpHAfrxXqoaIZau7kyrbANeWAMTtYFfG/r+DNrI6Q/YP6f/50GbQ1tmWsSvu8qE9xyUmyvBdqS0gV66T53CfwKWfK6cXJDIRHMUo4OPFWkCI/qAJi+WyP1Z6VbJn0yGWzS8snJTY3lI+ixLhI84KaEIj5VlaB0vvbvn1aGmRohow2JfTlFaRRVJnPcZYsulVaynyktdiG4jDkUJPsYiHWs3DO+iMUw+MAKd3ZyBTGh7wH7vBbKXpkFVEwKzaFMOHN8+/spBkqIHNSzn9Vthizqb+a8BwMiNB2EyCxENVGoBqTr9Z5ZVVAjkMLsBm0p42FLtnV20MBszRdjE4cuCZlSwN0qdJV1RqZYbYHVCGUOaavWeIYSXX4qG36iZXdPfYI/rgZ2clokqlshjb3xy//FbX5ghL4nquc/ed/ncsQtngyDtbqf54paIfBqFGRP/68XQTW30vt58UGb5mtHNW9LcTU2ZcqMmnY1aLFKr8ZPPsot17jTbhkuOazJsLJ32wSorBkHFS3ax0A0GwePKG3IZIP8wfNJhDgNiaCXQEaikACtlIVOjCUPL/zDfaaIlpZM0Qmum9j1QdrsIzX/gZ/51YZoqSRBMcjr8mMnTBNJ+zd06BUHGdkBF73KWuule8LOSENED1ZMMHt/NMAdPX9HWwy8l3VWleGKAYjJ9v6D1a3dgqDJVgRguq93GPOcNirq0RQmcmut6Mg9kgWcs1XQ5qIeHIy3m0Nl4UXk1GlybiYYOTo3XdMhJaZPSuFgb26382cvasFRtqIIzuv78Fgx1tO2z1pUmdHdn/j0wd7uZuj==',
            'bx-umidtoken': 'GAABFF3FBC2470A7C2B11C8F5DB2750A196AD4813D256421D0B',
            'bx-v': '2.2.3',
            'cache-control': 'no-cache',
            'cookie': cookie,
            'onetrace-card-id': 'sycm-mc-mq-market-rank.sycm-mc-mq-brand-brand-sale$-122854005-0-1',
            'pragma': 'no-cache',
            'referer': 'https://sycm.taobao.com/mc/mq/market_rank?activeKey=brand&cateFlag=2&cateId=122854005&dateRange=2022-09-26%7C2022-09-26&dateType=day&parentCateId=50014812&sellerType=1&spm=a21ag.11815228.LeftMenu.d591.671a50a5qYQAfj',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sycm-query': 'dateType=day&activeKey=brand',
            'sycm-referer': '/mc/mq/market_rank',
            'transit-id': 'Onp1PZzrfgN2CL5xSVE5qbIJKCXBdai2DimqrRSz0h+Ig13XFfD/+RLc/83ys6+PWhsyZik4UthNLkCB0XZC9iE0HzzCiGsgHwwetedOqf/8pGN0li7oYeTjXP98icLWUf/NLItr0qdgi2DEs+1/8M2OmJpP6VzRgrvn/380nT8=',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        params = {
            'dateRange': f'{start_day}-01|{get_before_day(get_after_month(start_day) + "-01")}',
            'dateType': 'month',
            'pageSize': '10',
            'page': '1',
            'order': 'desc',
            'orderBy': 'tradeIndex',
            'cateId': f'{cateId}',
            'device': '0',
            'sellerType': '1',
            'indexCode': 'tradeIndex,tradeGrowthRange,payRateIndex',
            '_': '1664262752258',
            'token': '0af67f152'
        }
        response = requests.get(url=url, headers=headers, params=params).json()
        return response

    # 市场排行_品牌_高流量_天猫_类目_月
    def market_ranking_brand_high_flow_tmall_category_month_main(self, start_day, cookie, cateId):
        # response = self._market_ranking_brand_high_flow_tmall_category_month_request(start_day, cookie, cateId)
        # datas = response['data']
        datas = decrypt(
            '660ED0FCE51BBF22276982667DD1F5CBD6B7C4DC8C9BE59CB3C046E14F6F7BEB566239174EE1751548A03D7C350BF2A7F7947FA405C32583380E101A8A7B9D8F93F91DB48E741FD763F9FC9E4AAA422C5507AF83F5388176CF8E19A9288F9E1457E142C22D121A3D30E5C13B88DFAC64F184460B3512F55D706F2D4A7A49AA6ED6219EEEF5C5C4F83AD6215D420D9CEEF04CAB12EAE0D782C13BDAEED601F4A5BBABE439062F94720491B8FB16A25D35D4C9FEBBAC4817F8F75FA396BA761E2F44D69EF35261FB541FFEE469F0BF838825780D2BF7227D52FD530190FF6AE35D1ED335C50495E101C7B01D564E659A1B1C325AB1C1E2DC21FBD13EA72E05640525F6257DCC4E816AAFB59A9A00FD6215561B96F79298A0B5A46406A445F6A506EB6E02F0E5FA5268D8F3D48AA1D62103ABED15F5AB91025833172595CD9341EA8E0E0415CC2AC3D5D96E68DA5D884091FAE034D2AF1D706C90EEB9B02D830763942056780C86C286D6FA650B9F80CCD5BFC99D182D8BCC49811232A23E91389662E3D9E7247AE635425355EFF46022489917CE6E07011E40EFD5647ADE02A684B9582769FDBAF72B352B643C43FA4E1FB493B1F58E217751E576D5D3A6F2BC539A9815DED9CEEA65DD0D87FCB44E2DEEA646D0F9F0D29366B6917A0ACC169183ADD38ECAA86F3E5C26F12AB6DC695A2A5CEE52E85F844154E2ACAE50875C71E27AD0EE14784F5143956135932203FF09941208AE3B84D5718272D9DDCB9344F2017B7BAC12C3905F3BB3BE945DB32A82EEAADA2EA8F5BEAD9AFAD89E96686B985089169C6676DB5EF91D03F159A7F773428A150926DD4FF5EE0793D90C7EBF6D24CC13DBCE4CA2C3137F259570E6CEC26A06A97D274D80270A0E6F31F89B023BFFE37A71C7480C26D0C039A620EA49AAA1B6F3695570F2CC50378F9D63DE9FB2A599567639600A7F4E947772B9EEE83D8FAE456B7BD0C5CD86A6D1AE8C58B4CD3D7FE071A08CEB28E353B8D577099425041BC836347D9BC0C8E88C1CD54C258849EA652ECD15EE59A90BC97E0555585487BC3F971D2141E9CEC39146C4AA2D4F4667BAA14EFC14F94580A6B6A58C5FC7BAF39EB1225D7A1DBEAD2076EEDD860DB8580CBC69398ED7E800C2FC14670A1B1904DF214E92EF0B758457C8286A79121F916A84CE09C66FE2D8C0632FEA379F69878381D2FEDE8F72B057A2B2A5E608D5E3FB605B4B87FCF243F8A75726320C826F1915F23D83F8E365377DA7F6EF6482C65DAEDFBD9564350626E0F0658E4192875342D92CA373CF358858BCBAB8E239F8E6D8E14DF49FA65670E58B3D58E9EF6CCE3D3A9AE11FAA5D61652BC6D71385536E4115D673E8EE6FB7A51AC7CC5CB3160FD026C46BE7CB4250BC7B5F9E15997A0DD4EB5E1E2B7A3FEB24DF3E5A9702D8B0C2012A726652C7AA183D53995D33D965120E9E95114B91554CFF98AEA438088999D9B74FE396B540A44EB4E6966D11EB8C7FDB445B6E9C6004453BFBB10A908056E1612E7D667015204485CF2951C54A17ED84B551130E1307676FC0E19DC6E2BDD11F51635C5A99538797B8C6C31F030DD2F13FDEE98688D3247AEE300982A694AB448C6BD63A9707F01C8AB2BCC6F8C91E82F41EF7E658DA10AEC8933EB3AF78922A9D41EA114DCCDE98B27F50615FFA9A5EAE2640DC60E950DD7667D42158E918224FF520F9E4AE31B14E1DDA6BC1F3237ADC4DDEFE2EF28D44F577C92A53F56A1001412DFE0DAB35562D8BB23A55AEFD9EEEF0FD7C84729F1E42B6BA6584E8E4DE17D11587AA2E1EA2BF0EA9CAB12AC3E0DCBD82D144FBA8D02F2623B4531367E9973B90C07C7245A6016DC0FA0F8E3F7FC4F26C7450D7B95D03025F7CF207D507FA3B64E26F581CB9D0DAD222C9A2973A01A8ED26D755790C566C514433562E16FE66F2DB9AEB1AC9CC47EAAFCB66B2325D649546CA60554C613DBB68C5CB0E0E65467EDED848D4AD9B674CB11C2311F8B6A1DAAF95F91610218E87FE4ED19166F8121A78AA7EE7EE1B07F30B0FC123EDC3634B96F3F337C86AB78BADA4BAF1B851B06FC322392585C939B4D49CEA4AFEFD8737AAC1ECBB28BFCB47071FE4D3C7EF27B2D33E8174900AFA05E28587A0289D32F1056D955DED78D24679B0BCA5CA99905B47F2E3A3A125D432739812E61B2E38598AF0BB7DEEFBF3CFA689AF5DFA1E682A45FFA642F99A9FAFC1EF9FF59628F5E78158E51B74FD00CA232947D7D180F34E58C2F20B57A2A1D9DAE48DE4CEF3C185613F6BA9CF1373FDE07EBD3DFA489A5FBCC62EB4C82A1E496C0BECB45D4CCB6C5E5B7448C2AE456E5C9B4A3E10EA12D43A207067BD1B1A4A45DBCCC338EDC912905A57D1F7441B3E0A31B366374856C4045DEA945C1B49B1D38C90717091095223B573B616EFBE11CB4284B0CFE67496D2AAFB6AFF087F71821063542E73BB0F4D5B4FBBEB6F68B7BF3549E9A6DFFD746F06DAF183CC5E36005FF92CB66B528BEE8D532FD35E921A433C3B252A4EB19FE4A1A0AA485A3FA03D1E3D2E574A5BBB497833BFC178279AE719AECF67A868EA5C2A68C6492D05EDAD4905C2613C522649EEA1E8350CFBBB4B5BDA196707B0793F8C2C77A390C1AA8AAF19B83870CF5FB817212E5FAA904E1D5A975229D60948E1D190CD56EB84AFA0DD94E644BB96E2D3290D34872E5D75A6EC1B23945F8430D468A45C63DE58EEC8BDE4088AB9104A9AFED963BDB80BEC70CCD65FDB505CEA835D7A870C9671E9B745CF266823703CD046C38CDE2B0A78EF222FAFB77BBA5057B2B521B16CD3C707D7E8B85C9240D6577BF98A88FF78F0ACF1602F7861C470E262C22FC05FBD616665613A5C5D23C3CB325F0BA214E70CD300BF1E4EB8D3FA044F00E45956873BF9108A587E6CC538CDBAD63E0CAEC50D568CCDC7FE8F7D2B56372E4FD53677988253DDEAA4879BDCF046D5E0B14E3A64DB8AD1C32D6C41C82920915F6B97CECA2B30EF742D80591402D3FB0825227292093C721DDE8CF7E9068DBD48AFC667F292FBCAC5269892E806A5E6E405AD148CA0AD544A5F4E5B7737C6BCCEE40B50DEC0C01B7472F180DFADC9A096748472190D7AE31AC0030A53DB934288017F783E7B8500E287A78A413A37332CB0B9A3D4B4D6D171A29A96C6605E4BBE550B7DD3D8B4A97885A4BAEAF39B68E058E855B83D57B0F2DFB8F8B50975B4F8EAC7CADDEB075E83100CF390A73C222C5AE5048176E99589D2083F47F2D3A2D6D83B2E30A12A75817679748670986E3C2737C1DDEDD209FA2BD0EDBF8C7DE90FEF52F401D8EB56BCB6D2435F19FE56D785306283F74D38A31FBA714AFA584D4A8BE730F4E857731E765B4CD365C9C804A4B3937CA0ADBC7933F492AC227A66385DAF4ACEA25360AD280E031D4F042B4D8ED342CE149CFE957F68F6C8ED571124636A4D47F00333266D4E14EF59EC32F103D699374A0E80C7113EFE7B7B0F997D32D3930CD2EBFCB7A73D0ECF6DAEF83EC0A0EE1D4C2C7318ADA206BD0FF8529A657D701F40F28842EC492C76CBF801F7A78DF66BED67C7F8CE78D59431CB305D70657F3956E7FA6A663143F019F094C56E79828E2BAE7415951217B89F348F0DF936378CEA123BFCF685F9FCC6480717916119B6B54B21C3AA6C047F57DECEDD2AF99388844AF2689B851767C70F0692F147BDC05EEEC215D01868071F9753BE4F8D01CE3B1238400EC3E83EFB70858B2F6F54D46412FA6225A4CA99979412368DE58B4B322534220023DBE326881EB2849DA2DCA6CD412ABBB50D09BC6B1FB6DD7A239AAAA9CF58D53E9D2F0BF4625FB9B311CD7C0C62C74F5B88E749A88A8D77613B4BB760E6E5FB1CC19BE778E234656BD8781424455BB451A135613366F9E7B3C1DCFED7EFF298642725CC28FF7BEE7793CF8CEBB3A8CEA4640357865A6FD4105B8A3569A5DCC82D8C4AB9413F3B3925200858B9492FA18831267647509FFC3C9FB64248C65DDB32943723C2068D5CCBE3EE252663D74EC98928BB01C5E3CCA695880AFD12DFC51FFE9AF5A494795FCAD1177A7D06649ABE44D7C5F3412257C145B95B880C5627963FC3A9FDCAC96FFC4971463CCC9AC7BAB9769515961EC6EBB06071EAF0CF6318443C62C567B2BABD54B6397ABEA1536DE2567C99CD7F3BFA0797037FCEE4AC9798BC137F02959E13C54330840CC3CD849FAC48DBBEA0406A371A4E2BF19AE289BD175467FDD9DCAB9D77B8CF69F2458D410C5BCE0768BE459062E3C22AB1E5394F60A743A44A59043D6D720702B34651EC69D0F4B780568ECB2489F1C4102A9CBAB9C38D5DD272F754D421C3ACF2102EF617B5E2BEF13CFB2C4388D06891D676BC7A9ED6BE5B5EF282D4B338D6650AFF7FEAFB65905A1DE569A20741A1EC3D63B95339C8BE306F3AF7016EA9A6AF2B0B85029A5446F9EB00612B6CDD6FEFE1CBE5E5CBDC0BAE967C80ADCE7B6F919419D961461AE6C68D3221908F735E3070D187FFEA047FB84ABFF2C6CBB90726071759B1887B5C559423AB16504DE9AC7B5696FE799C7CCFAAB02082A6D8CECD0BFD041109EE2238F3DE330C53F9B6B0C5737EDEBA269F879599234223DD98D3CE399E376B9FC485E921E3A16D349EDF95C58F780D22C67C329A0B8B844090242A8F66D3CDB41265321689BD6B3631467816DACC7BBF7635464D820FAC2A351BAF5A4B3DB8E620402B508F1D9DC7728B1A713B2F870A1821F640947EFF3EF56B4D6DFEFB31E15A1C098E767C50A061A83E13D11096DED4047A52AD2459F537F3C37AFB153B996041F1739AE9CB6BCE4B978C5896C6C3512EBD23634005B61D7523111BAF0708674FEE9E7DE64477B2DCA9839ED9899012FE61116E30F2E93336DE31A34C65C4B4143D7F0D4D8DDC5C89EF40A9E6BFA3FD89EEED3AA8BFF755E66C20E5F1AA10567F24C6FB24B8865080669D72ABE7F1D44D59102C97DB1ABF8BD32A98F10749911EB0DC50CD7F42057C3E6E660032B2525CA01E8D44B033EEC32C7EF1E63402E237F51CEE6C82D611E30C2FFC1658EC96C7EF3B9E83093648C7E45B868BF6148274514AFBCF86A63AF672F9580FC960FDC21A380C73418E9A82F75B2FFC1E470A735483669AC626C8B5095C8022B9CADC4E80B92959EC2A8ABEE45E21EF3F3EA4E12DA3A3BDDE4FDF57D9EC45D479AA0DEEEBD55F2A9599DF772BF440A75F8A7302CC62422915B297DA16BB663137618DB8694721C29E1B68CF46B8E0D2DB23EC45B8F15055C2C29F24538EBF032AD4C8BAE3B01B77D4495926EE5B78E68BF4A67B73EB4F923EA309DA5D7A1A549AAD771A20B1A4FADC14ED4AFD086CFE87105B214B65CF1102297F1A81113E361E263E9ED8B98D12B0D755367B9905B249E0CDB387DA33D05A00A034CED5EDA38968E9235952AE6E4C55060373F126AAD315F9B6FE6068AB57AA394A6B2D5FD7DE0E2793D1C3D39BC7FD3B2B3FEA87AB97BCDD2EE7EB69D889C9C72228108A00604C6157AFD799A7386BB82FCF5D70251EE7AD56E6EB1E9E47A3FAFADB99CE2C004F1AD5EE1C4E3F5613733F5C871B6B762A8FA3332B68B98BFE444028C292596F00C68B8299D6C50A5C3080B3C4C6BB0878C7152F7A6C3B2A66F2C3E0C39248FD9006DAA54C077936E3A97365CF4A5758081017C00E6B1179AF75F6DC7D96FABF4E7E11956824AD9F4D4C4FB929BED6A344E8CA12387706F5B36654AED486FF3B0E2FF070B63B426D70409F687C6714354F3FA19349A36AFF7E88EBF97CF67623F7F16F0FAC5760753FBA880E3EA1A7BA183A355F60382E377458F4B6305441BABD1DBB84077BDB8E0BD30E6ADDF91F4052B164821D1BD8804750630098352AB630450B2C1E23A24E8B073FFE1614F69B933EAFEBC31045E331FDBD6AF8F2FF3EF4B547714CD59A60B31552F9A964D870C01A87B6C00FF9F7CF43E395A8486CA601DCFDBAFCB0260A80A1F8C808B50D929CF70CA234DBC78A8A9A0F33B4099C894B853C205CE71E3DDDB31755448B47BF51697695EE40AC6E6D560679E44E978F441BB82A5C3051D1A4E4C7C5E86482541E812EE56A31EB3A9F85671CAA5EA4561D96F016A136D1A68E05E0DD6DB294036EEE30E3072FDBB44A56E730CD16D2ADA3AFD4346EE971E866F9B9F4D6478F28A1E590C212DE0232B9BACEEC035397912254DD4B714262F8793E978878DB34011C17FF3E23FA0420EF2D8386DC5CB41E96AC5F2FE7E2E8E6B27D3D0B876E067E532ED9D4BA31355116BF9F1D04E5DE3771DD3A1BBB06E535B083ED58274F21E85E14856A2F56559122CC0FBDE4820D62ACAFB94EAA6DCC593841654B553BDFFC80FE256EEA8320957435D080876521F0383C8C6FE42C27439F07359272799F9910451BB2D996F774C572FB947AD9E1131FFD3D9CFD4B64F55B398C1950CAFD5B1F07FD6E68F22F45E110D0CFCEB48E37621EDA1EE13845E92931A8DE22E9C248776C3318202B74F44E3AA1FCE5CEFD8C9C8588BC03806721AF8354395A7093B985851E6D82A2AD4924DBCBEFE3695281BF3EBEA41C46679DBA64BB50D561FF64D696ADC9D1DEA7E48E9709E9C3888A57648817C8BA611AF17ECBE61FDFD34F03792B849A237158742FC052DD918679C7E4731370157714E4F7B7343D7C7DE875538D17D98C2CDCFB17CE5B5E809C4257BBD41770E60C288B3868AF1C105144B8027A350A7121EEDD90C9BCEF69681E35144953708489E40BE9715CB2AAE6B4A10CEC9CA04DB707CBBB3C394B34358EFB7DC0D3A66D35A0CFA72D5600AEF6CB6C916B679DCCCFABB85DE26E58BF2A749346079A5BF43C3E32DE52C948BB26544A3F5939958A76090668A1DDEDF2058C424CDA635AF9ED39E151D5FE79495DB977AAE59E249BDBD5BB3143FCDA4D1F958520FAD056C905BD800DBFD6A8DBFCE569F3A3EB1FB608794BF14F89A469102A04F09E551582A453E9FEB14F99A449C61F2B4B4A8F4BD727FCBCD5347ADE6C9189088BE1DDB7D379C92F1ED4EB8CCE9BB524D6826BED68C5437C10595D998DD85A7FC139B6C09AC0F1403C35676941586A900500BD181370C06F3A7AC529032AF0DE0DC53B2BD08DB9056F1837E3705D4ABABBCB83C792C58D441AB160F8AAE5E15BAA63D5D258109326E2970A9C810972E529ADA6922D20B63A8E1904A14E9456C6C37D904D0B4C23803554BDDB237A897F45FFB7E9A5B232005CE0DA12D4E793CD8AF1E4F50A403F5AC39CEE7BD6C2185701F517CF9CF1ADA2BA2CB64A7CC7C550AC4129742E65981DED36C71F0FE94BCD1D1F959C768E31525EAB6AB5C099A1658669A469B8D70CADD41EC876B39F59B296CC4819EC94051F783642684C4434BF668A52B8DE19874B79C7D2544B4F9979F384D188073EDE319627BFB6D1D171C608139CBBC20BE92F5BB94B3C1C8FFAD60A2717DC2E5A45B9AD079BBFAEB3790BEF78E4FC3C7836DE70EC09F52E8E12B1BA06B7C22A86ABF4CFD6B427081E4540BDE6387D07ED2B1A27559A42A72FF894D1E08B1D0CB98DD5D18575AFAD6B21C48363325E4A89D16766142E7A2A43D93995CABC4EF04129C6806D822EC23F5AC788A76AC1B7474809D34324632B05E69EB7162FA3F9D25D4289AFE14600710B7B79E3448A2DA14EB6538E22E13AE395A794546E7AEF726D38C710721CED4E3C63EC905E4A6917BF671FCA82BA974C48F2F22899C89E0197A47D1FB104E75A15D641C66AC584C7D40EF3188CF5EDDD08B35FE8D7D3822314DE260BE7CD4556B930F9CA98072A84E61E9166291CCD35115EB203F818C67D607034954BCF9579ECDA94C5499B76AEB160FCBA2C3119585D9A612FD732CA0E0B741631E5AAF0662A7EDDDF0E526C77C7C3E9151B19E3D10D7460688C2DE307DE7089DA5E9D5C34719C1C7BAEBB2D165261D67B5FC1D4C97D05915C90D2A6F32F84E19B8E0D11961138473D7DA0DD0C53F54594399E3CF89E89563A3380CDA5EFAC423EBA911586FBA469A3FF0770F8278F676C36441916E8AB4B6CFC704845C6284F9BACBA232C33322C486A8593CA42824B51C933790D7276B0B0BFA4F9851D1D0C346F2C3E1077E651C1B25ADDB406BCF4FDE0F2103F7C447CC81FA53AD5D53A400D21E2AF86C1C21A49EFF09502EDC812DBA92FEC4EE1B1D2AF74A4830670DF729F88F746C7FEAD2D8EBC05486133CFF58A54E6EB129A0E6EF27D2892E1825E918874F17B5FE64403C96D6B85581CEEED761185AD1185CB375190D1555CA4A562BA73447915934C604C5C52C3164A3CBBE7479E95D0C3FB558458B2CB7F248EEAEC5CA1078C70942AD62564791A55D8DBF60B820A139D61B65757DB0E1A4AC16ED86EBDDFB8EADC1216C76C804D94E6EBCCE907B62EC233A236015104B986C8BFBEDACD70A4BD9AB50514C5A644ED1F4E4238E2A30CC766A64A75A9863BADDCD8F815571170A2EF2A6F3DAC182BAFDC677BA1096402AFC2193D04283AE80BD2631A087BC2B3F76A722BEE1A6469AB904D16905EC9EEE3820FE95D63BDEDE265EBB05A66E5F2A740DA875418052680C205785593D668833B69B57CDC71E3173E528B5FD64C7AE999CDBF94EC46436B09F3BF00E6686A3E55B55125C5870705845B40FF06016400D3EF829DA02ECA328A7C4557957275FFF08BDEB71AD3E29816D4E4ADE470A7290115CA8732FFBD47C3C89D882A37A812951DB4CD659CE1123D1EA7003F4A240724F98D5EC4AE70CFABB0C37BA77EDBF29C845CC938B9F74E0380922C87173679A41B6307E88174F8AB77EFA384A145C71EB84F93E000FD4E4F6240268B861DE1B7F05470E1FD4DF154BCA2759F197CC6B5FED859C2E71582F01ED43B6ED80FD3655A5A4C2F6B0C4432B71987EE5C63B2EDAE0F15A5F1451A51053C253AD9E86D3FA30D2B21CFEE7FF95E78A1216E272C136D0DE97BF10E357C57D891AA18240237A42BACF229FA6F3ECF8159DBE8A84170ACD16E2A5731EABD112E72025D07F234107374CC787785C51CA85BC54EF347C5A5ED1000F370FA3CEAC76F841FFAAD1E137ADF29C5136B3ED02467050406DB9150170E9DC992BCCDD67CBCED817E8FEB24E1B491CF0C66F33B21ED51FE083D52BE0EF99AE1778708E345867F4D796EDFAF4C6EA7253214EBF0474D0B387A6A9143EECFF8E3FF95E6C4FA703C5A9B72634432DDEA84E4257F11A65F76CE378FBAADC3BD2345C7DD627D883ACDE7ED513A841E93B3DC33BC2AA9CEFBFBEF268FFA17630D0B485BAD82022BECE1C9976CE13DAC01DA9E70FF93BA9BEB7E8A02A8B30501258624AF429320F697A748C681F21DF3BDFCE15B48BCE2E19819F2E6E2CFCF74AED9D3C2703A47A9002623C1E8A4BC76BEFB63ACDDBA366EE5D949F489D9CA62CA58B34AED1F2B789A8C44A82C54CD5E0AF65FC8BD327BE205711C8A1BA5D9EEBA3F617FEC6C4A5BC337FB254F030252CCC1D5E41712D4CF0B78FB401335667B9D48ED674CDF2B0A2F467785ED28229C86AFCA892B9F4F211D9EA79E97A5CBB28345B06DCF82D884E8E0B4C55C9F23B0CCC8B02697357BB0114F7ED6A5AE8C2DB78D07FFBC5E3B5A3AC72F5CBCEEC549E9067D4F4F4ADCFD7EDB2B674CB7E440C135688BD67F6A786C2883C30D702F8C63FF79C5FC50B13644135758D1BF57D5D584F6EA16E7DB05FC419E102B28BE7EC8E2B63BA8843F15A668E362DA8CA260900FFA2D7A811AD2BD46EFD175ED3DE08B8BE028E93577646F79013E7C41829E2117E4030F6F007D33AD7A6A7C8F21E0DF6E68B7FDCAE670F33D283EF604110436C08D56A93230191F44D3616AB1F4AB40EB1B38F7F298C01F02ABBB437BFC0E4446ACC56EE8E2026D60C640856F64318F77080F6BFB5EA75E51357BDAA8BF772211E29A3B67FD6B8EC81FF7D4A260409DF2E5AEE532E60ABCB7C9B78E97E96D1757BCFBCE3F32F180D41DFF3CA3214B36236E92A2DB398630B5C22D5BA5FA9FC4E028E5359A577891F4D7FF46BB67B4BD687ABE27EF489F8E003B9BD00E63F932BE505954CC71484912A04294C0076BED7396EE1859F9A450B15C330FE5153D24DBDD9DEB57D743E2AE8A758A1FB1B00FDC3A923E10F5681098D6FB948A0CD31DB422A3FA7877E42319A385E8E647F44E7BFEFB595500722537F3A988E3431A58F724CE24E254284356E4610A3A8F4CF2246302FFD253986468953B9BA777F8318E2159036E131DA7CFC193324B52054981452727F6249EE035002851BC77872757DA71F8D2664BE89CE4E445330CAECF1C513E98E139ECDE7E8CBD4D5BFF877923459C86331B710A91668FD5F900A9A1D90E4C1D72126647A6AB10BA10386192FF10224F3990BCD016B8861E540CF4032550441019755D395C50C97F8112B9AD607403B6C252F04E7D68C380D48E19EA8C6DEA852131A6EF0FB792EB663460B7CE4E12A23B6EF3245D9D4136BACE6193A2BDBA5F0CCC8794FEC10109EE65680FCCF1C7EAD0EB1BEE3129D934347E88D57B3E9FC8EA6A5E2E263DB8C93C5E35CAB2BC8C35B35CBFBC3F0610E7B04A14B94938D1462CD2A61304A09362393D0302726E8078FA4F3C7DB594171C22E2814A424A3B8AEF1CF0CF3ADF62F2971715A147F6622E55949EC7C2A047A200CD38381FE7AED070C6301535B645D14D37CD072B99A7A99E0D5BEE81FDAE36DC77340B2FF61EBD7E883F5DDD26767AFECD32C0378C49370F5F0991791B4E1365652BAFA087DF72ADFCCAD5063A2305BFF98F88917536424ABD2688156AFCB611332CDF320C7F58E2B4DEA434E260A25B361168D1707A3929E09A4151078BE461E2E6B92332179906D4EE64F850BCBFD83205DF36A3E46E4FA193D2070E6AB2ED743277A289457BF0A6E3C2618A37D05B54F3DCA2DD72B88E9450BEED2FA7861553B8985F38291BECC0DBB4DC4A0355B3772DE4EDCCF04F2B9FFE4F7CE505B876D97C21969380F80BDBC87DFA3C65CA4264179CAE09A7AB54C09970B005E664F183F4AA57E58B5A9A1A416EA84421D8EFE7C622AC34245E8DDCAC622AC000C53F745E9B6CA5B66CED6A7C4B2CA9A59586C44C9C5E04BD930EB6FAB729D371FCC05C692249D04753CD61BFFEA09DA136623851EE78908FEE4271569D5D2C9DF723B0A915BD3A75CCC6C81AFFB636973EDE17C33AA3253D1242981CBBD0B5AA4B089EAD4C0165F6A2934DEBD9AD41A56D08564C89015468B6177879ECAD4AF36972E26F5A858241368AC5B52BFF17053295E38926074C08B8AEF8D99AD996DBFCA6CF6454BAB602F140206ECE83F791C6A1FB8A798B38630D3A3205FFCD0F6146B2D2AECF01CF6FF04D1F423C45B665B82B55F594F71851DA4AE5DC2B2F6EBF76BEAB72AD2A1F72D25F75B2D5D4E5CCF2D9F52564599D3803117A374FF18F4AB9517E52111228BB2EE5E478974D397CEC86619714D9A23F6FE629B61A0A1507BB883E766994D03CF20CD0A3EF44E4F0D54B4EC56303EABD08FADBA8896AA8980CE0D18510AC031978607B2CC685962E3F1A524EA926ABA0895344600F29FA8A5B03B727E448B2D5A5CDBD9B9E9F93A9AD70321038DC1C744AEA556924001E2DDCF272A80A6AB47E7F24B4E25E885B17A7D3EFE7EF89A93A0CC405A9FE75FF84AB51A342CBB4DC7A8F9E3D0EAA2B4967D100C0D65C841B4D9DD281F0682CADDDD695F5E4466C22803B17B187D4695CD91E2B1C17D086D74024070C27BE92370E799D3C02114917C146553DD975E2155F27F6C9AAAF8CBA6B6CA763F8EF18A6667D371E9CFBC64A3C46151ED93699B5E953CA7151D22368D4D6764D538EC13D570801A5DEE15104400060F177E43E657D4CEE94A968A818187AD4BB5E389292FB5295C683113DD3582E2BCE5E5F9F26DB849F8E533827A43D983AFDE6263EC575E5747446664DC7E7ECEF6D193646133263AB339B08E08856CCE9E590E0B339B68FB880D43AFA77E7AD68E627B05F6ABE988769437FB6AF299EFD3D318E0E471CFF253E60D8680B489A8FDEAB6312E264BC07BFBFA0DEAF609A654EB8A5651D51DE92416AC3C33038591F95310ED9D940E9D4E362EC31AED4363419BCF57CAFCD5F0522216FADF757A006252DFB984221E482C6140A02F1DE7E752391374E12F6C465E93043C372CF9E5B285877C56DD82660D337A0D1D418E55E779CB812B299769DCA1F8F3ACB292CEBF24F563B937F21200ED9A1796AA4E85F8C603EC966BFE398B71411094915216D7495ED05961645E4E3B5904330A5E2F6578FE40A8D3791E398FBE32CAAF3A8085A5233596EFFB0CD4EEA94705F72AD48C2776924EFED9CD3F86D3B7501AE1315FFE906829E3B57452E04F39F1B6F3F829A5CB01BF40C5CDBA845075CC1C85DADDBB9DB8B5F2BF789092F7E10F25028FB8E1C5B4CA50747C7C717D3AEF92F14BF5FC47C1196AC9BFEAAF2936CCF7E772408B51F3500FAFA82AF52F5682C9F72079BF48AE42F5B60E5D8CFF3526A0BBAA0A75874E9449FE381BF5B1DC02EAE63DB2824020C30C7093187208635EA2A5282E01496562A245680C19750B915FA6A268166BA92A89BE62B4DC9D6E8A3106406F79ABEAA57C776257D0E75294A9DFBFC9C8CE3B9314210844CB2A9FFEC8F171C1D8B31348E7328A402B769FFFCDD07248BAB65ED9A3ACF5B6D17E9CD29A64C0B38584CCF21ED9A77B5C3DA8860F968C2A98AD9E6B8C9FC086BE2E96B3BDF6A64035E06358CAF2F460A39AC3686B034926CBE9BBB4C9411F04DF75EB1F8C79497071D12A410E404B49BE52281EF8F523853CAC996D93CB5FBFE91EBF470A994DFB66C4AB6061ACB1DDA98E4CC9B1AC37C137769299EBE9B0F9B2F980C62C7FDB3F164DDFE559244396F855E10879D1B6BA96E19A57665E10BE014BB36EE7B8004AABA875DA6BEE4140C311004F9100B8BEB76A6F4EE0B03C89484EFB5A45CCA714282F2978ACFCB3A3AB2AF3786984FDCEE689DBC4CE510E0BB03236FCB68ABAA59890B62583058B9BAD3FCF346484F55BF9BF7000FEEC63C97972A1503563771C40782BA987BB51D8E250730ABC04CEAC8D99113D457538B0240CA1B4918F981DFE68475C5A295E7EB44A43EE6D9B4EA3493E4CFD4E269EC8133106CAD7EDB40A25BB61C4AE14480E3F78491FBA688A1BB304DD190F01BCABC697393D3B29475527AEEF82B6CB46B3CC1E8581E818BF2CF25356870BAEB6467771C50202466B14D66069C22DFC30750F20A4F16F144BF7D72019FBD90B2754CDF39D3461E355A1A878EFC41C75C90850CAA7B3C815E436C7C6AB4D28FFE9C11F3900D2211EA070A0B14EDDE3A8EFBD12B1B55B060001AFF649DBFDE9779B120B42E6B67B3F3E810BE2944E0F58525802662EFA8E623FD36B53FE3E2024D3934400602C5ECFB26A23B0E240DCCA1C24CD7882B70F87F5FE65DC5592A2661ADAAC05AC0B7367D5851FEC28CAD93D4DA318D56BE3C5F5F142D75668D9CF7F33043C0E5E6E7FFDE27AE67500D955A06E6F1B871367D7143D9F5814DE949048968DB14D95C9A21BA0017E677C8ED1BCADD2D399339F5EEE246AB712D192F2B37DD3F2DB9644BE9E11BD275C7700074DB26DF7D3D395F627B668C65265C6A7223286A7C7982734EF85440B75FC2980DFDA413798BCE7F7AC93FDEB323F8979F60E30CDB44D5DF24AD0BE8C365157EFD919E20FA15ADAC392FDDF4443EA09E5D29C456ACF0EBEC75DB5519A0A4215FEA9463BC5E2CC21C4F16400AB9356705CBFB712B1DC21EE4E223718F90F71886CED4904914B9F23F2EBF934FEF8C36B45A7FCED90C75C6D499B27CB353BEC203F90F667AD43BE33C7D4A75A9F4983C2D40801169179E3EA027F3EAF0728E722DF11F998D537121AF0FC9795F01F375049A8EEBE7F1317D0DE245A07D2C6896593950D8127ACC9351B4E26292D9702CCB6260271801FEA01D693172790B8967F1B2B4725C5D89D1D98BC346E54573547967C66717830830E02CE762CE0750C7E3AB6DAB2876FE2ACF6DF488CFBC8603B064CF8303C67EB58E5DF1DBB28C80C326CCDE78A6F5CA433CE4D1F7A3F7268D019C6D184C71FC9D56837CA5A2CFA11AE565D5F83986247A2199A5D8EF03CA3D8D760873DEB37A78EDDF7503B5BA1E735F3ACF9469B9D140A3173D3D6DDAEEC1B941BF3B8CB27FE1F874B2C7241735D19D92563E99E0CAAB0BA46031249F9469904B9B28B46A60F39E49B323F86674878DA610E578203C22B49B6AD776C081127E7A5C1A94F2CF1DABD8E5AE26BD2B51B11B92A17FE4910C779942D51D18DA6D49F7276B6B5840A626AB37451573EED581D138820C5FF0C80BE184C1117CFE237C745B4EAFB6EBB36F88A78C714FBC0D8A3EB4DB3DE0588A2F1769D52710015F1C6D6A27B1EEC749F24494FD392965B4C0D089B6CD9089DB99018129A15F66693E1B273F12BC9C4D4FE54EFDCBEEC3FDAD2E8D78A93A0C443CFC4035ADE5E6A422EF34C4F0442A74196AA4A7043AEABE6A55F3AB2B769B6F5B50CB45C9B69A6C548D224FDCD49078F5ED1BEE0F1144CDE472F8D1D677DBCEBCF5D19815A1B5F4EA24FB78DA5B94564B012F927FB28AF4AB3F614AC999BDD335640E6880AF89E046411F4C6D31F75E914A283CE9CEC2C6D0DA31C4D1D3F8277CFCBEAAD682691D3275B95253D779289A4CF716C6708E580632AB99C98C825B10DB135E80732C0C933D76460D115BC97DD04384FCB57F7F7C603A31CD008D08060AC67DB8116C5E77C1D81CCCE25C1F6B98E85B0CE436246F12D844E6181B68F2C8600CE590648898B36E2B4E6BBE20903305038E0F7589E5DA9DE1BDCB28C390062019B3769B7D6A8E73CEB61B3635B351B3A9B58A2D4438E87F4F5DAEC07589A6903FB0323169356C56E71C408255EAB9A485C2BD593787C157966F1485D1E21C643F0C21B86FA26103D35BF9962477634F399C4A4624A597E17635F453BF6ECC2DF4CAC60664ABB9B707BAADBE332551205D92DD854D2858559B5BE63354F2C373E05BF7FD8A1B700CC0AE8EFACB4DDB623499963CE3C5136F244641467B0FC1EA90F13873A95A43E549271716B14A4739D2C64E3778D222C3621FC5EA90C673CC15FB4D42892810A9598DD91633B7BAA59FAEA2D9A18D0824F351A88EB7831ED174884B91052C60A23F9316A683C4D24A244A9AA1C6FA9274EEF6ED77E6DD8E5D8ACBEA199B5D77A4B93E6761BF441FA3DD805876EC7028565B18858D4B9926ABE44431E028606134892D029EE36DF16676D954B6DB88C9A967DFCB29C48A4752DBDE40DE9284016520AE263917B8EB6483C2DDCB07B9D691CDAAA3812B18129A52F5AFB14878D38E84AE55F32E99FEF3623231F681A31361117CFA1D027B5007F097924EC1F31D6377F90368491D1F9B1B4A23C5E34C99E1117E49418ADB13654217C6C89E73E11056D168C270E7C41C7362DEA590FF98B70A40F9F347A89F7F39CBF31DAA88746D011438098CAB0AA6AC21675C311053B866127E380F0E727A9CB586F7370D9587AE93684776E60314B5D47D4C89199416D44A10C0CEC97FFF299DB54BDE72E1CD8DFC1A2E26572CA34F88F6B0F3B82FB3B2D420ECB6CBF58EB5BC21F8EEABFDC4601DD35921E089F48D63B3AAD0E1B25860C47B9F4917E1604EB5367D87AE55E631F99A9996C4DAC9DB30FEAC526B6AFC0C34F67C38D93B8C25BFA6B95BA29BF3544F888B946D6EADD53CB02EA2E7E7BF9C5CE7126958693D3C03D4AD6CC776860A22EF0EB06072B8DBA085444EB21858017508D5E0F480F68977789B5F3527BA559772DCDC02603F6DA868C9C529C369DA93F5B69F423A8C55BFD15552CD2E5B27CA1EEF9463C5CBA878D0BBD74BED1B46A91EE91191E6C62FBDCD16433B1F49374B49FCCB50FA5C44210421AC5BDEFFA5068B4536FCD4AAAB696A372E8A91E900F9DBAB5D6C20D2AD1090D330D22C5435036F751EDBA37C7937E3A5EE1AEC365E59C56059F8254728F19C3264756324B613DA4465ED0105DCEAF0F646F03EB512D7C0EA05AFCDD67609F889A2A0D82EEDE3321D42780AA61605F7525BD6F3BB5374C4EF68B96B5C04DE890B34BDDA83D93AA1229F10F5C77F52BEA69F73B2E2C25800AA694CED565FB961944F58DC50A8ACD24FC441DC9730CF1E96FE20FAEEAFA9ADF89FF4FC85D998529D8B1D24594297D08D8C44DC5339914764801E6CEE6EC97D24CBDAE09303503FDCF294C8FDAEE7A202B9A837E5DAE71FC706581CFC46CD99828473AF8E2AA9DC749D2F76307EA6B01C94FB86C1588F6DB3AEE0925B073B1959AFCA28FF7DA392BB34C414DD425F7579F53C5699E3791595E28F9C5CB9DC6DE7DE4D777571D4D0CDC26E6D6C5FB6DD6C037689EEECE6BE6766F107366D91DB1FC2EF3CE52B3F817F5C8E7FD1DD34E11B89BFDD57E57FC0050BBF18650203C54DC2591E855041ECC9FEAC690DE57A1AF39AE8D853A789D11EFD6E85039D191A31C5788BE3AD41853A00BC82EC7B1A77B917EBCFAC1DEFE5FBECF57F477D95124A2216669F273DABB53C2BAFAC12BBCB38226F1FE781C6F112AB8415994515D3E8CCCF29202E83F1DEF27233F2ABE72B840EB82228E2B19080868587F89E8ACB551C55DC9BECE8D9481006C35CE5DA400270AB39EC038C37893290709B96DCDAE741362774100037971E03AB15921BC8452FFBF3B3D1036AC21BF3AC9118D763CF588C')
        for data in datas:
            brandName = data['brandModel']['brandName']  # 品牌
            brandId = data['brandModel']['brandId']  # 品牌id
            cateRankId = data['cateRankId']['value']  # 排行
            tradeIndex = data['tradeIndex']['value']  # 交易指数
            uvIndex = data['uvIndex']['value']  # 流量指数
            seIpvUvHits = data['seIpvUvHits']['value']  # 搜索人气
            tradeIndex1 = self.change_info(cateId, ['tradeIndex', tradeIndex], dts_cookie)  # 交易金额
            uvIndex1 = self.change_info(cateId, ['uvIndex', uvIndex], dts_cookie)  # 访客人数
            seIpvUvHits1 = self.change_info(cateId, ['seIpvUvHits', seIpvUvHits], dts_cookie)  # 搜索人数
            value = (
            start_day, cateId, brandName, brandId, cateRankId, uvIndex1, seIpvUvHits1, tradeIndex1, uvIndex, seIpvUvHits,
            tradeIndex)
            print(value)

    def _market_ranking_brand_high_flow_tmall_category_month_request(self, start_day, cookie, cateId):
        url = 'https://sycm.taobao.com/mc/mq/mkt/rank/brand/hotsearch.json'
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'bx-ua': '223!g2Bdfzfd6QIgGCgyyg67xMFGrOX+xO6SoGmrPzc4J0hOhxinwCesUqlJZVZJxQA8EvZ/xIN5ybqg34H2vgK5pXD4wn38F2r/E842u2JG5HUSxF0+TSBcKxrINDJlGA1pkgns3cOQ+1lGcQQ4z3c/eW3JcQXCW+t/rgRycKJw+1l4TQ0jNJa/K6SmAHj29jAhr85ZdKMEeuC4cQQ4zJNkUEsy+gQCWGT/rWRygKaOe1IJcQQciJi/+6R4ce9ZcmAzVxBMtIZPFsX+9A4W1wJVrvz4Li0nI2YUm1+OOnLAmzC4esMl6OUYQg18mcwG8N6LLVEE3STKlVUtUKKoeu7F7g9eSCBwss+fQY8/MQOhzYJ98dOq2It0Y3iwFz7nKE4bJelam+lf9X65MUO0RP0XRDYbcj0kKWh8YsHpAp74mRDU4s+OAf5vJRwy/FgtMpb2oGElX5l/DCnolt4Q319+KSuWlivCpaPKU7rxNrvMViqbCXJAcN6XvNWL+5/ybbn9+jZwx+Sy+wnpHcCOy1U31a3nKU/tkX6nD65wKDBcM9HzGZuQS8jJB/DucVG5rjDVvfZignfJm4QPsCqH3fvhUQwgLMY3LFG+gDu7Q1asCHJajOO/M5kHhBkb7EtHnLxV61i8midNQSjoWkfqdHucmPPurDq5b6qyaFrSR8D0LCgJPLn9g/SKtIMetsMHdltgLItOh8VOjFD5CpmvmELQWwNEUXcHWSqsBB1yi8/EiVBaM1YBYsiDmDll7CQFFsFpnjjY0v29EjYzNdgRSdxz4d5I4juA92gfdAVvYyN1a1pRGvLRzoHwPdJbNX82tljefWMrYCy/Le6YKb4QUEEWw+1WrUcbGrjmDtfMq+ZtqBdF+CkogIE+YL8j4cC2pmOaayxJ3wJV574z0qyjuwq4ECQxtJx2p0sdfNNfgHdAGGu2+N7HfScitl8QLWdAi93MowMbD0nDNZGkxbSZz9KiwKuwCccKE0leiUsVJxinM4svZh7XnlYdr4teGE8OPTvSg9gBNs8frtDU6x6AF0zVGZU5+kkAChckLwJg5vjW22g/99OydtjM7SgK/T8N6EZ1wbf7cGPx9BDmbOo/KKtphVP3yYfu2Vbu3gGPvd6ygZ21fp3ziMt78b9rwKa+CBXoFahiYFuV4q95Yg==',
            'bx-umidtoken': 'G55C27A8591A27B4A7D75BCCEBB929F92606DED891B04991A37',
            'bx-v': '2.2.3',
            'cache-control': 'no-cache',
            'cookie': 't=da03a3a2ff72f7a25e393fbd232e1134; cookie2=121ead4360c93f87765c152c6653fe17; _tb_token_=389583a0e66ae; _samesite_flag_=true; XSRF-TOKEN=acd73bc1-09ac-4719-9f17-828c35aea530; xlly_s=1; sgcookie=E100ixY2KjHyX5Sx%2FdGzmDd2b%2BwAc55gYFNESe2Yxn4EM6tDY4p3NlQwEUyuu5HLhvjQBnNrww9vk%2FsYoRU4wH05MwQG9To%2Fcw5NSggaI7E3MLA%3D; unb=2212628883848; sn=dyyyz99%3A%E7%BB%83%E5%BA%86%E9%BE%99%E9%A3%9E; uc1=cookie14=UoeyChEKvV3mfw%3D%3D&cookie21=VFC%2FuZ9aj3yE; csg=76e0c49c; cancelledSubSites=empty; skt=06b4cde54b4bf632; _cc_=WqG3DMC9EA%3D%3D; _euacm_ac_l_uid_=2212628883848; 2212628883848_euacm_ac_c_uid_=4224382495; 2212628883848_euacm_ac_rs_uid_=4224382495; _portal_version_=new; cc_gray=1; v=0; cna=jWCxGw8o4HwCAXPG25PMGsWZ; _euacm_ac_rs_sid_=231244751; _m_h5_tk=52fedde33b581105fe2a1f0ad77a0439_1664345848517; _m_h5_tk_enc=2c930d1b9fe8fa8d34d61802d30a4bdd; JSESSIONID=575B06DE46966A82DD7BD1EC2CCEB7CA; tfstk=clnVBAZO-nKVQ-H99uqZ4dg0vMXRaaMmIgyQoBBbxPAehg4bTsVc68VbH8y1U14c.; l=fBE4J76mTrlClT8FBO5Zhurza77OfQRfhsPzaNbMiIeca6OJiFgJZNCEoE7lrdtjgT5qceKrshOewREv8oa38xt0zOZLQf3ZYwv68eM3N7AN.; isg=BK6uutkKQap12bVXemrI4RYM_wRwr3Kp8pGLPth19bF5u0gVQT5duFP9cydXY2rB',
            'onetrace-card-id': 'sycm-mc-mq-market-rank.sycm-mc-mq-brand-brand-search$-122854005-0--1',
            'pragma': 'no-cache',
            'referer': 'https://sycm.taobao.com/mc/mq/market_rank?activeKey=brand&cateFlag=2&cateId=122854005&dateRange=2022-08-01%7C2022-08-31&dateType=month&parentCateId=50014812&sellerType=-1&spm=a21ag.11815228.LeftMenu.d591.671a50a5ROAAAO',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sycm-query': 'dateType=month&activeKey=brand',
            'sycm-referer': '/mc/mq/market_rank',
            'transit-id': 'GEj1fIyMjCJvheKmn5UZNn2ZQAYoMNphB72T8zljoRAEGytM7Mm3sw4RiQKeGPXakGHZeD3NpykE9Fe1phV32jexBaDx673qNCRy1SETF81IZIJAurg4zLMOPamFxua9jeiIMahdh4tHZWbyeVIPX7yjtzwiFERWMDMPqqefoXM=',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        params = {
            'dateRange': '2022-08-01|2022-08-31',
            'dateType': 'month',
            'pageSize': '10',
            'page': '1',
            'order': 'desc',
            'orderBy': 'uvIndex',
            'cateId': '122854005',
            'device': '0',
            'sellerType': '-1',
            'indexCode': 'uvIndex,seIpvUvHits,tradeIndex',
            '_': '1664336186104',
            'token': '0af67f152'
        }
        response = requests.get(url=url, headers=headers, params=params).json()
        print(response)
        return response

    #  贝德美.dbo.淘宝客_定向计划报表
    def taobao_guest_directed_plan_report_main(self, cookie, start_day, end_day):
        if not start_day:
            start_day = self._sql_server.get_start_day('贝德美.dbo.淘宝客_定向计划报表', '日期', '')
            print(start_day)
            if start_day == get_before_day(get_today()):
                return 0
            start_day = get_after_day(start_day)
        if not end_day:
            end_day = get_today()
        while True:
            info = []
            response = self._taobao_guest_directed_plan_report_request(cookie, start_day)
            fk_all = response['data']['result'][0]['alipayAmt']
            fk = 0
            p = 1
            while 1:
                res = self._taobao_guest_directed_plan_report_request1(cookie, start_day, p)
                for i in res['data']['result']:
                    campaignId = i['campaignId']  # 计划Id
                    campaignTitle = i['campaignTitle']  # 计划名称
                    enterShopPvTk = i['enterShopPvTk']  # 点击数
                    cvr = i['cvr']  # 点击转换率
                    alipayNum = i['alipayNum']  # 付款笔数
                    alipayAmt = i['alipayAmt']  # 付款金额
                    preCommissionFee = i['preCommissionFee']  # 付款佣金支出
                    preCommissionRate = i['preCommissionRate']  # 付款佣金率
                    tkSuccCnt = i['tkSuccCnt']  # 确认收货笔数
                    tkSuccAmt = i['tkSuccAmt']  # 确认收货金额
                    cpsSettleNum = i['cpsSettleNum']  # 结算笔数
                    cpsSettleAmt = i['cpsSettleAmt']  # 结算金额
                    cmCommissionFee = i['cmCommissionFee']  # 结算佣金支出
                    cmCommissionRate = i['cmCommissionRate']  # 平均佣金比率
                    fk += alipayAmt
                    tup1 = (
                    start_day, campaignId, campaignTitle, enterShopPvTk, cvr, alipayNum, alipayAmt, preCommissionFee,
                    preCommissionRate, tkSuccCnt, tkSuccAmt, cpsSettleNum, cpsSettleAmt, cmCommissionFee,
                    cmCommissionRate)
                    print(tup1)
                    # if tup1 not in info:
                    info.append(tup1)
                if res['data']['hasNext']:
                    p += 1
                else:
                    break
            if (fk - fk_all) > 1 or (fk - fk_all) < -1:
                end_info = """{},贝德美
                                《淘宝客_定向计划_推广计划》数据错误！""".format(start_day)
            print(info)
            self._sql_server.save_message('贝德美.dbo.淘宝客_定向计划报表', info)
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)

    def _taobao_guest_directed_plan_report_request(self, cookie, day):
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            # 'content-length': '99',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': cookie,
            'origin': 'https://ad.alimama.com',
            'referer': 'https://ad.alimama.com/myunion.htm?spm=a21an.11816897.0.d0a3cf2d6.29cf61db3lnR5v',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3765.400 QQBrowser/10.6.4153.400',
            'x-requested-with': 'XMLHttpRequest'
        }
        url = 'https://ad.alimama.com/openapi/param2/1/gateway.unionadv/mkt.campaign.report.json'
        data = {
            # 't': '1617938521048',
            '_tb_token_': 'f5763b9b68be7',
            'campaignType': '2',
            'split': '1',
            'statisticMode': '1',
            'startTime': day,
            'endTime': day,
        }
        res = requests.get(url, headers=headers, params=data)
        print(res.text)
        return res.json()

    def _taobao_guest_directed_plan_report_request1(self, cookie, day, page):
        url = 'https://ad.alimama.com/openapi/param2/1/gateway.unionadv/mkt.campaign.report.json'
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            # 'content-length': '99',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': cookie,
            'origin': 'https://ad.alimama.com',
            'referer': 'https://ad.alimama.com/myunion.htm?spm=a21an.11816897.0.d0a3cf2d6.29cf61db3lnR5v',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3765.400 QQBrowser/10.6.4153.400',
            'x-requested-with': 'XMLHttpRequest'
        }
        data = {
            't': '1620957176116',
            '_tb_token_': 'f5763b9b68be7',
            'pageNo': page,
            'pageSize': '40',
            'campaignType': '2',
            'split': '1',
            'statisticMode': '6',
            'startTime': day,
            'endTime': day,
            'isToday': 'false',
        }
        res = requests.get(url, headers=headers, params=data).json()
        return res

    # 淘宝客_定向计划报表_淘宝客效果
    def taobao_guest_directed_plan_report_taobao_customer_effect_main(self, cookie, start_day, end_day):
        if not start_day:
            start_day = self._sql_server.get_start_day('贝德美.dbo.淘宝客_定向计划报表', '日期', '')
            print(start_day)
            if start_day == get_before_day(get_today()):
                return 0
            start_day = get_after_day(start_day)
        if not end_day:
            end_day = get_today()
        info = []
        while True:
            response = self._taobao_guest_directed_plan_report_taobao_customer_effect_request(cookie, start_day)
            for i in response['data'][0]['campaignIds']:
                campaignId = i['campaignId']  # 计划Id
                campaignTitle = i['campaignTitle']  # 计划名称
                result = self._taobao_guest_directed_plan_report_taobao_customer_effect_request1(cookie, start_day, campaignId)
                fk_all = result['data']['result'][0]['alipayAmt']
                fk = 0
                page = 1
                while 1:
                    res = self._taobao_guest_directed_plan_report_taobao_customer_effect_request2(start_day, campaignId, cookie, page)
                    for i in res['data']['result']:
                        campaignId = i['campaignId']  # 计划Id
                        pubId = i['pubId']  # 推广者ID
                        pubName = i['pubName']  # 推广者名称
                        enterShopPvTk = i['enterShopPvTk']  # 点击数
                        alipayNum = i['alipayNum']  # 付款笔数
                        alipayAmt = i['alipayAmt']  # 付款金额
                        preCommissionFee = i['preCommissionFee']  # 付款佣金支出
                        preCommissionRate = i['preCommissionRate']  # 付款佣金率
                        tkSuccCnt = i['tkSuccCnt']  # 确认收货笔数
                        tkSuccAmt = i['tkSuccAmt']  # 确认收货金额
                        cpsSettleNum = i['cpsSettleNum']  # 结算笔数
                        cpsSettleAmt = i['cpsSettleAmt']  # 结算金额
                        cmCommissionFee = i['cmCommissionFee']  # 结算佣金支出
                        cmCommissionRate = i['cmCommissionRate']  # 平均佣金比率
                        fk += alipayAmt
                        tup1 = (start_day, campaignId, pubId, pubName, enterShopPvTk, alipayNum, alipayAmt, preCommissionFee,
                                preCommissionRate, tkSuccCnt, tkSuccAmt, cpsSettleNum, cpsSettleAmt, cmCommissionFee,
                                cmCommissionRate)
                        info.append(tup1)
                        print(tup1)
                    if res['data']['hasNext'] and res['data']['result'] != []:
                        page += 1
                    else:
                        break
                if -1 < (fk - fk_all) < 1:
                    pass
                else:
                    print(fk_all, '  ', fk)
                    end_info = """{},贝德美
                                《淘宝客_定向计划报表_淘宝客效果》{}数据错误！""".format(start_day, campaignTitle + str(campaignId))
                    erro_dingding(end_info)
            self._sql_server.save_message('贝德美.dbo.淘宝客_定向计划报表_淘宝客效果', info)

    def _taobao_guest_directed_plan_report_taobao_customer_effect_request(self, cookie, day):
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': cookie,
            'pragma': 'no-cache',
            'referer': 'https://ad.alimama.com/fifth/pointed/report.htm?mode=media&startDate=2021-01-17&endDate=2021-01-17&campaignId=116092767',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400',
            'x-requested-with': 'XMLHttpRequest',
        }
        url = 'https://ad.alimama.com/openapi/param2/1/gateway.unionadv/mkt.rpt.lens.data.campaign_present_list.json'
        data = {
            't': '1618198343134',
            '_tb_token_': 'f5763b9b68be7',
            'startDate': day,
            'endDate': day,
            'rateSource': '2',
            'campaignId': '',
        }
        res = requests.get(url, headers=headers, params=data).json()
        return res

    def _taobao_guest_directed_plan_report_taobao_customer_effect_request1(self, cookie, start_day, campaignId):
        url = 'https://ad.alimama.com/openapi/param2/1/gateway.unionadv/mkt.campaign.report.json'
        data = {
            # 't': '1617938521048',
            '_tb_token_': 'f5763b9b68be7',
            'campaignType': '2',
            'split': '1',
            'statisticMode': '2',
            'startTime': start_day,
            'endTime': start_day,
            'campaignId': campaignId
        }
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': cookie,
            'pragma': 'no-cache',
            'referer': 'https://ad.alimama.com/fifth/pointed/report.htm?mode=media&startDate=2021-01-17&endDate=2021-01-17&campaignId=116092767',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400',
            'x-requested-with': 'XMLHttpRequest',
        }
        res = requests.get(url, headers=headers, params=data).json()
        return res

    def _taobao_guest_directed_plan_report_taobao_customer_effect_request2(self, start_day, campaignId, cookie, page):
        url = 'https://ad.alimama.com/openapi/param2/1/gateway.unionadv/mkt.campaign.report.json'
        data = {
            't': '1618198584497',
            '_tb_token_': 'f5763b9b68be7',
            'pageNo': page,
            'pageSize': 40,
            'campaignType': '2',
            'split': '1',
            'campaignId': campaignId,
            'statisticMode': '3',
            'startTime': start_day,
            'endTime': start_day,
        }
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': cookie,
            'pragma': 'no-cache',
            'referer': 'https://ad.alimama.com/fifth/pointed/report.htm?mode=media&startDate=2021-01-17&endDate=2021-01-17&campaignId=116092767',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400',
            'x-requested-with': 'XMLHttpRequest',
        }
        res = requests.get(url, headers=headers, params=data).json()
        return res

    # 淘宝客_效果概览
    def taobao_guest_effect_overview_main(self, cookie, start_day, end_day, shop_name):
        if shop_name == '贝德美':
            table = '贝德美.dbo.淘宝客_效果概览'
        else:
            table = '贝德美.BODORME.淘宝客_效果概览'
        if not start_day:
            start_day = self._sql_server.get_start_day(table, '日期', '')
            print(start_day)
            if start_day == get_before_day(get_today()):
                return 0
            start_day = get_after_day(start_day)
        if not end_day:
            end_day = get_today()
        while True:
            info = []
            res = self._taobao_guest_effect_overview_request(start_day, cookie)
            for i in res['data']['result']:
                preCommissionFee = i['preCommissionFee']  # 付款佣金支出
                preServiceFee = i['preServiceFee']  # 付款服务费支出
                preCommissionRate = i['preCommissionRate']  # 付款佣金率
                preServiceRate = i['preServiceRate']  # 付款服务费率
                alipayNum = i['alipayNum']  # 付款笔数
                alipayAmt = i['alipayAmt']  # 付款金额
                enterShopPvTk = i['enterShopPvTk']  # 进店量
                enterShopUvTk = i['enterShopUvTk']  # 进店人数
                cltAddItmCnt = i['cltAddItmCnt']  # 收藏宝贝量
                cartAddItmCnt = i['cartAddItmCnt']  # 添加购物车量
                cmTotalFee = i['cmTotalFee']  # 结算支出费用
                cpsSettleAmt = i['cpsSettleAmt']  # 结算金额
                cpsSettleNum = i['cpsSettleNum']  # 结算笔数
                cmServiceFee = i['cmServiceFee']  # 结算服务费支出
                preGPP = i['preGPP']  # 单件商品付款支出费用
                preTotalFee = i['preTotalFee']  # 付款支出费用
                alipayNumDepositPresale = i['alipayNumDepositPresale']  # 预售笔数
                alipayQuantity = i['alipayQuantity']  # 付款件数
                alipayByrCnt = i['alipayByrCnt']  # 付款人数
                alipayAmtDepositPresale = i['alipayAmtDepositPresale']  # 预售金额
                cmCommissionRate = i['cmCommissionRate']  # 结算佣金率
                cmCommissionFee = i['cmCommissionFee']  # 结算佣金支出
                cpsSettleByrCnt = i['cpsSettleByrCnt']  # 结算人数
                cmServiceRate = i['cmServiceRate']  # 结算服务费率
                tkPvItemCnt = i['tkPvItemCnt']  # 推广商品数
                tkCouponGetCnt = i['tkCouponGetCnt']  # 优惠券领取量
                tkSuccAmt = i['tkSuccAmt']  # 确认收货金额
                tkSuccCnt = i['tkSuccCnt']  # 确认收货笔数
                tkSuccByrCnt = i['tkSuccByrCnt']  # 确认收货人数

                tup1 = (start_day, preCommissionFee, preServiceFee, preCommissionRate, preServiceRate, alipayNum, alipayAmt,
                        enterShopPvTk,
                        enterShopUvTk, cltAddItmCnt, cartAddItmCnt, cmTotalFee, cpsSettleAmt, cpsSettleNum, cmServiceFee,
                        preGPP, preTotalFee,
                        alipayNumDepositPresale, alipayQuantity, alipayByrCnt, alipayAmtDepositPresale, cmCommissionRate,
                        cmCommissionFee,
                        cpsSettleByrCnt, cmServiceRate, tkPvItemCnt, tkCouponGetCnt, tkSuccAmt, tkSuccCnt, tkSuccByrCnt)
                print(tup1)
                info.append(tup1)
            # self._sql_server.save_message(table, info)
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)

    def _taobao_guest_effect_overview_request(self, start_day, cookie):
        url = 'https://ad.alimama.com/openapi/param2/1/gateway.unionadv/mkt.rpt.lens.data.account_effect.json?t=1596616875523&_tb_token_=d54eeb5eb3be&startDate={}&endDate={}&type=cps&split=1'.format(
            start_day, start_day)
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            # 'content-length': '48',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': cookie,
            'origin': 'https://ad.alimama.com',
            'referer': 'https://ad.alimama.com/dashboard.htm?startTime=2020-08-04&endTime=2020-08-04',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3765.400 QQBrowser/10.6.4153.400',
            'x-requested-with': 'XMLHttpRequest',
        }
        res = requests.get(url, headers=headers).json()
        return res

    # 淘宝客_推广产品看板
    def taobao_guest_product_promotion_board_main(self, cookie, start_day, end_day, shop_name):
        if shop_name == '贝德美':
            table = '贝德美.dbo.淘宝客_推广产品看板'
        else:
            table = '贝德美.BODORME.淘宝客_推广产品看板'
        if not start_day:
            start_day = self._sql_server.get_start_day(table, '日期', '')
            print(start_day)
            if start_day == get_before_day(get_today()):
                return 0
            start_day = get_after_day(start_day)
        if not end_day:
            end_day = get_today()
        while True:
            info = []
            campaign_list = ['营销计划', '通用计划', '定向计划']
            res = self._taobao_guest_product_promotion_board_request(start_day, cookie)
            all_number = 0
            for i in res['data']['result']:
                if i['campaign']['campaignName'] in campaign_list:
                    campaignName = i['campaign']['campaignName']  # 计划名称
                    click = i['totalData']['click']  # 点击数
                    cmAlipayNum = i['totalData']['cmAlipayNum']  # 付款笔数
                    cmAlipayAmt = i['totalData']['cmAlipayAmt']  # 付款金额（元）
                    print(cmAlipayAmt)
                    settleNum = i['totalData']['settleNum']  # 结算笔数
                    settleAmt = i['totalData']['settleAmt']  # 结算金额（元）
                    commisionRate = '%.4f' % (float(i['totalData']['commisionRate']) / 100) if i['totalData'][
                                                                                                   'commisionRate'] != None else None  # 佣金率
                    serviceRate = '%.4f' % (float(i['totalData']['serviceRate']) / 100) if i['totalData'][
                                                                                               'serviceRate'] != None else None  # 服务费率
                    totalPaid = i['totalData']['totalPaid']  # 支出金额（元）
                    tup1 = (
                    start_day, campaignName, click, cmAlipayNum, cmAlipayAmt, settleNum, settleAmt, commisionRate, serviceRate,
                    totalPaid)
                    print(tup1)
                    if not cmAlipayAmt:
                        cmAlipayAmt = 0
                    all_number += float(cmAlipayAmt)
                    info.append(tup1)
            sql = f"select 付款金额 from {table} where 日期 = '{start_day}'"
            pay_number = self._sql_server.check_message(sql, 0)
            print(pay_number, all_number)
            # if abs(pay_number - all_number) < 1:
            #     self._sql_server.save_message(table, info)
            # else:
            #     print('数据不一致')
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)

    def _taobao_guest_product_promotion_board_request(self, start_day, cookie):
        url = 'https://ad.alimama.com/cps/campaign/newlist.json?t=1596614174233&_tb_token_=d54eeb5eb3be'
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-length': '48',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': cookie,
            'origin': 'https://ad.alimama.com',
            'referer': 'https://ad.alimama.com/dashboard.htm?startTime=2020-08-04&endTime=2020-08-04',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3765.400 QQBrowser/10.6.4153.400',
            'x-requested-with': 'XMLHttpRequest',
        }
        data = {
            'startTime': start_day,
            'endTime': start_day,
            'type': 'cps',
        }
        res = requests.post(url, headers=headers, data=data).json()
        return res

    # 贝德美.dbo.淘宝客_效果报表_商品分析
    def taobao_guest_effect_report_commodity_analysis_main(self, cookie, start_day, end_day, shop_name):
        if shop_name == '贝德美':
            table = '贝德美.dbo.淘宝客_效果报表_商品分析'
        else:
            table = '贝德美.BODORME.淘宝客_效果报表_商品分析'
        if not start_day:
            start_day = self._sql_server.get_start_day(table, '日期', '')
            print(start_day)
            if start_day == get_before_day(get_today()):
                return 0
            start_day = get_after_day(start_day)
        if not end_day:
            end_day = get_today()
        while True:
            p = 1
            info = []
            while True:
                res = self._taobao_guest_effect_report_commodity_analysis_request(start_day, cookie, p)
                if res['data']['list'] == []:
                    break
                for i in res['data']['list']:
                    itemId = i['itemId']  # 商品ID
                    preCommissionFee = i['preCommissionFee']  # 付款佣金支出
                    preServiceFee = i['preServiceFee']  # 付款服务费支出
                    preTotalFee = i['preTotalFee']  # 付款支出费用
                    preCommissionRate = i['preCommissionRate']  # 付款佣金率
                    preServiceRate = i['preServiceRate']  # 付款服务费率
                    preGPP = i['preGPP']  # 单件商品付款支出费用
                    cmCommissionFee = i['cmCommissionFee']  # 结算佣金支出
                    cmServiceFee = i['cmServiceFee']  # 结算服务费支出
                    cmTotalFee = i['cmTotalFee']  # 结算支出费用
                    cmCommissionRate = i['cmCommissionRate']  # 结算佣金率
                    cmServiceRate = i['cmServiceRate']  # 结算服务费率
                    enterShopPvTk = i['enterShopPvTk']  # 进店量
                    enterShopUvTk = i['enterShopUvTk']  # 进店人数
                    couponDisRate = i['couponDisRate']  # 商品折扣率
                    avgCouponAmount = i['avgCouponAmount']  # 平均优惠券面额
                    cartAddItmCnt = i['cartAddItmCnt']  # 添加购物车量
                    cltAddItmCnt = i['cltAddItmCnt']  # 收藏宝贝量
                    alipayNumDepositPresale = i['alipayNumDepositPresale']  # 预售笔数（不清楚）
                    alipayAmtDepositPresale = i['alipayAmtDepositPresale']  # 预售金额（不清楚）
                    alipayByrCnt = i['alipayByrCnt']  # 付款人数
                    alipayAmt = i['alipayAmt']  # 付款金额
                    alipayNum = i['alipayNum']  # 付款笔数
                    alipayQuantity = i['alipayQuantity']  # 付款件数
                    tkSuccByrCnt = i['tkSuccByrCnt']  # 确认收货人数
                    tkSuccAmt = i['tkSuccAmt']  # 确认收货金额
                    tkSuccCnt = i['tkSuccCnt']  # 确认收货笔数
                    cpsSettleByrCnt = i['cpsSettleByrCnt']  # 结算人数
                    cpsSettleAmt = i['cpsSettleAmt']  # 结算金额
                    cpsSettleNum = i['cpsSettleNum']  # 结算笔数
                    tup1 = (
                    start_day, itemId, preCommissionFee, preServiceFee, preTotalFee, preCommissionRate, preServiceRate, preGPP,
                    cmCommissionFee,
                    cmServiceFee, cmTotalFee, cmCommissionRate, cmServiceRate, enterShopPvTk, enterShopUvTk, couponDisRate,
                    avgCouponAmount, cartAddItmCnt, cltAddItmCnt, alipayNumDepositPresale, alipayAmtDepositPresale,
                    alipayByrCnt,
                    alipayAmt, alipayNum, alipayQuantity, tkSuccByrCnt, tkSuccAmt, tkSuccCnt, cpsSettleByrCnt, cpsSettleAmt,
                    cpsSettleNum)
                    print(tup1)
                    info.append(tup1)
                p += 1
            # self._sql_server.save_message(table, info)
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)

    def _taobao_guest_effect_report_commodity_analysis_request(self, start_day, cookie, p):
        url = 'https://ad.alimama.com/openapi/param2/1/gateway.unionadv/mkt.rpt.lens.data.item_effect.json?t=1597124382920&_tb_token_=d54eeb5eb3be&startDate={}&endDate={}&q=&pageNo={}&pageSize=20&period=1d'.format(
            start_day, start_day, p)
        headers = {

            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            # 'content-length': '144',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': cookie,
            'origin': 'https://ad.alimama.com',
            'referer': 'https://ad.alimama.com/report/overview/orders.htm?startTime=2020-07-29&endTime=2020-07-29&pageNo=1&jumpType=-1&positionIndex=1596027196_1mhuHuuWUDZ2%7C1596031726_InAI9NiyYL2',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3765.400 QQBrowser/10.6.4153.400',
            'x-requested-with': 'XMLHttpRequest',
        }
        res = requests.get(url, headers=headers).json()
        return res


if __name__ == '__main__':
    dbo = Dbo()

    # bilibili_三连推广效果
    # dbo.bilibili_effect_of_three_consecutive_promotion_main('', '', bilibili_cookie)
    #
    # print('----------------------------------------------------------------------------------------')
    #
    # # # 二级流量来源_无线端_单品
    # dbo.secondary_flow_source_wireless_terminal_single_product_main('', dbo_cookie, '')
    #
    # # # 三级流量来源_无线端_单品
    # dbo.third_stage_flow_source_wireless_terminal_single_product_main('', '', dbo_cookie)
    #
    # # # 三级流量来源_无线端_店铺
    # dbo.third_stage_flow_source_wireless_terminal_shop_main('', '', dbo_cookie)
    #
    # # # 贝德美.dbo.取数_店铺整体_日  贝德美旗舰店
    # dbo.access_overall_store_day_main('', dbo_cookie, '贝德美旗舰店', '贝德美.dbo.取数_店铺整体_日')
    #
    # # # 贝德美.dbo.二级流量来源_商品效果_日
    # dbo.source_of_secondary_flow_commodities_commodity_effect_day_main('', '', dbo_cookie, '贝德美.dbo.二级流量来源_商品效果_日', '贝德美旗舰店')
    #
    # # # 贝德美.dbo.二级流量来源_无线端_店铺
    # dbo.secondary_flow_source_wireless_terminal_shop_main('', '', dbo_cookie, '贝德美.dbo.二级流量来源_无线端_店铺', '贝德美旗舰店')
    #
    # # # 贝德美.dbo.品类_宏观监控_标准类目_日
    # dbo.category_macro_monitoring_standard_category_main('', '', dbo_cookie, '贝德美.dbo.品类_宏观监控_标准类目_日', '贝德美旗舰店')
    #
    # # # 贝德美.dbo.品类_商品效果_日
    # dbo.category_commodity_effect_day_main('', '', dbo_cookie, '贝德美.dbo.品类_商品效果_日', '贝德美旗舰店')
    #
    # # 热浪联盟商品明细 热浪联盟_主播明细
    # dbo.heat_wave_alliance_commodity_details_day_main('', '', dbo_cookie)
    # #
    # # # 优惠券效果_日
    # dbo.coupon_effect_day_main('', '', dbo_cookie)
    #
    # # 热浪联盟_推广数据总览_日
    # dbo.heat_wave_alliance_overview_of_promotion_data_day_main('', '', dbo_cookie)
    #
    # # 引力魔方_报表_点击_主体汇总
    # dbo.gravitational_magic_cube_report_click_entity_summary_main('', '', dbo_cookie)
    #
    # # 贝德美.dbo.引力魔方_账户扣款明细
    # dbo.gravitational_magic_cube_deduction_data_main('', '', dbo_cookie, '贝德美.dbo.引力魔方_账户扣款明细')
    #
    # # 万象台批量报表下载主函数
    # dbo.vientiane_report_creativity_laxin_express_main(dbo_cookie)
    #
    # # 二级流量来源_无线端_店铺_月
    # dbo.secondary_flow_source_wireless_store_main('', '', dbo_cookie, '贝德美旗舰店')
    #
    # # 贝德美.dbo.品类_商品效果_月
    # dbo.commodity_effect_month_main('', '', dbo_cookie, '贝德美.dbo.品类_商品效果_月', '贝德美旗舰店')
    #
    # # 贝德美.dbo.万象台_账户扣款明细
    # dbo.vientiane_account_deduction_details_main(dbo_cookie, '贝德美.dbo.万象台_账户扣款明细')

    # # 直播_合作直播间_日
    # dbo.live_broadcast_cooperative_broadcast_room_day('', '', dbo_cookie)
    #
    # # 内容_全屏页视频_商品分析_达人带货视频
    # dbo.content_full_screen_video_commodity_analysis_videos_of_experts_carrying_goods_main('', '', dbo_cookie)
    #
    # print('----------------------------------------------------------------------------------------')
    #
    # # # 贝德美.BODORME.取数_店铺整体_日  BODORME
    # dbo.access_overall_store_day_main('', BODORME_cookie, 'bodormebaby旗舰店', '贝德美.BODORME.取数_店铺整体_日')
    #
    # # # 贝德美.BODORME.二级流量来源_商品效果_日
    # dbo.source_of_secondary_flow_commodities_commodity_effect_day_main('', '', BODORME_cookie, '贝德美.BODORME.二级流量来源_商品效果_日', 'bodormebaby旗舰店')
    #
    # # # 贝德美.BODORME.二级流量来源_无线端_店铺
    # dbo.secondary_flow_source_wireless_terminal_shop_main('', '', BODORME_cookie, '贝德美.BODORME.二级流量来源_无线端_店铺', 'bodormebaby旗舰店')
    #
    # # # 贝德美.BODORME.品类_宏观监控_标准类目_日
    # dbo.category_macro_monitoring_standard_category_main('', '', BODORME_cookie, '贝德美.BODORME.品类_宏观监控_标准类目_日', 'bodormebaby旗舰店')
    #
    # # # 贝德美.BODORME.品类_商品效果_日
    # dbo.category_commodity_effect_day_main('', '', BODORME_cookie, '贝德美.BODORME.品类_商品效果_日', 'bodormebaby旗舰店')
    #
    # # 贝德美.BODORME.引力魔方_账户扣款明细
    # dbo.gravitational_magic_cube_deduction_data_main('', '', BODORME_cookie, '贝德美.BODORME.引力魔方_账户扣款明细')

    # 贝德美.BODORME.万象台_账户扣款明细
    # dbo.vientiane_account_deduction_details_main(BODORME_cookie, '贝德美.BODORME.万象台_账户扣款明细')

    # print('----------------------------------------------------------------------------------------')

    # # Unidesk_报表_效果投放_日
    # dbo.unidesk_report_effect_delivery_day_main(ud_cookie, '', '')
    #
    # print('----------------------------------------------------------------------------------------')
    #
    # # 直通车token
    # dbo.check_user(bdm_ztc_cookie, '贝德美旗舰店')
    # token = dbo.get_subway_token(bdm_ztc_cookie)
    # # 贝德美.dbo.直通车_账户报表
    # dbo.through_train_account_statement_main('', '', bdm_ztc_cookie, '贝德美.dbo.直通车_账户报表', token)
    #
    # # 贝德美.dbo.直通车_单元报表
    # dbo.through_train_cell_report_main('', '', bdm_ztc_cookie, token)
    #
    # # # 贝德美.dbo.直通车_关键词报表
    # dbo.through_train_keyword_report_main('', bdm_ztc_cookie, '', token)
    #
    # print('----------------------------------------------------------------------------------------')

    # dbo.check_user(BODORME_ztc_cookie, 'bodormebaby旗舰店')
    # token = dbo.get_subway_token(BODORME_ztc_cookie)
    # dbo.through_train_account_statement_main('', '', BODORME_ztc_cookie, '贝德美.BODORME.直通车_账户报表', token)
    #
    # print('----------------------------------------------------------------------------------------')

    #  贝德美.dbo.淘宝客_定向计划报表
    # dbo.taobao_guest_directed_plan_report_main(tbk_cookie, '', '')

    #  贝德美.dbo.淘宝客_定向计划报表_淘宝客效果
    # dbo.taobao_guest_directed_plan_report_taobao_customer_effect_main(tbk_cookie, '', '')

    # 贝德美.dbo.淘宝客_效果概览
    # dbo.taobao_guest_effect_overview_main(tbk_cookie, '', '', '贝德美')

    # 贝德美.BODORME.淘宝客_效果概览
    # dbo.taobao_guest_effect_overview_main(BODORME_tbk_cookie, '', '', 'byd贝德美')

    # 贝德美.dbo.淘宝客_推广产品看板
    # dbo.taobao_guest_product_promotion_board_main(tbk_cookie, '', '', '贝德美')

    # 贝德美.BODORME.淘宝客_推广产品看板
    # dbo.taobao_guest_product_promotion_board_main(BODORME_tbk_cookie, '', '', 'byd贝德美')

    # 贝德美.dbo.淘宝客_效果报表_商品分析
    # dbo.taobao_guest_effect_report_commodity_analysis_main(tbk_cookie, '', '', '贝德美')

    # 贝德美.BODORME.淘宝客_效果报表_商品分析
    # dbo.taobao_guest_effect_report_commodity_analysis_main(BODORME_tbk_cookie, '2022-09-28', '2022-09-28', 'byd贝德美')



    ########################################################################################################################

    # # 监控店铺_竞店列表_月
    # dbo.monitor_stores_list_of_competing_stores_main('', '', hsxx_cookie)
    #
    # # 监控店铺_二级流量_月
    # dbo.secondary_flow_month_main('', '', hsxx_cookie)
    #
    # # 市场大盘全网类目月
    # dbo.market_network_category_month_start_main(122854005, '2022-08', '2022-08', dts_cookie, hsxx_cookie)

    # # 贝德美.dbo.市场排行_商品_高流量_天猫_类目_月
    # dbo.market_ranking_commodity_high_flow_tmall_category_month_main(start_day, '50012421', hsxx_cookie)
    #
    # # 市场排行_商品_高交易_天猫_类目_月
    # dbo.market_ranking_commodity_high_transaction_tmall_category_month_main(start_day, '50012421', hsxx_cookie)

    # 市场排行_品牌_高交易_天猫_类目_月
    # dbo.market_ranking_brand_high_transaction_tmall_category_month_start([50012412], '2021-09', hsxx_cookie, '2022-08')

    # 市场排行_品牌_高流量_天猫_类目_月
    # dbo.market_ranking_brand_high_flow_tmall_category_month_main('2021-03', hsxx_cookie, '50012414')
