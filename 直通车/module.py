import time

import requests
from Setting import *


class ThroughTrain:
    def __init__(self):
        self.sql_server = SqlServerConnect()

    # 贝德美.dbo.直通车_账户报表
    def account_statement_main(self, start_day, end_day, cookie, token, table):
        sql = f"""delete from {table} where 转化周期 < 30"""
        self.sql_server.check_message(sql, 2)
        if not start_day:
            start_day = self.sql_server.get_start_day(table, '日期', '')
            print(start_day)
            if start_day == get_before_day(get_today()):
                return 0
            start_day = get_after_day(start_day)
        if not end_day:
            end_day = get_today()
        page = 1
        while True:
            response = self.account_statement_request(page, start_day, end_day, cookie, token)
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
                    favItemTotalCoverage = round(float(data['favItemTotalCoverage'])/100, 4)  # 宝贝收藏率
                except:
                    favItemTotalCoverage = None
                try:
                    cartTotalCoverage = round(float(data['cartTotalCoverage'])/100, 4)  # 加购率
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
                    favItemTotal, favShopTotal, cartTotal, directCartTotal, indirectCartTotal, cartTotalCost, favItemTotalCostInYuan, favItemTotalCoverage, cartTotalCoverage,
                    eprePayAmtInYuan, indirEprePayCnt, zhijieyus, zhijiebs, indirEprePayAmtInYuan,
                    eprePayCnt, transactionTotalInYuan, directTransactionInYuan, indirectTransactionInYuan, transactionShippingTotal, directTransactionShipping, indirectTransactionShipping, trc,
                    coverage, zjdjzhl, clickShoppingNum, clickShoppingAmtInYuan,
                    searchImpression, searchTransactionInYuan, tqdjje, wkje, ykjje,
                    newAlipayUv, newAlipayUvRate, favAndCartTotal, cof, favItemAndCartTotal, cofa)
                self.sql_server.save_message(table, [value])
            page += 1

    def account_statement_request(self, page, start_day, end_day, cookie, token):
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
            'queryParam': '{"page":"' + str(page) + '","pageSize":"100","startDate":"' + start_day + '","endDate":"' + end_day + '","effectEqual":"30","pvType":["1","4","2","5","6"],"sortField":"cost","sortType":"desc"}',
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
    def unit_report_main(self, start_day, end_day, cookie, token):
        sql = f"""delete from 贝德美.dbo.直通车_单元报表 where 转化周期 < 30"""
        self.sql_server.check_message(sql, 2)
        if not start_day:
            start_day = self.sql_server.get_start_day('贝德美.dbo.直通车_单元报表', '日期', '')
            print(start_day)
            if start_day == get_before_day(get_today()):
                return 0
            start_day = get_after_day(start_day)
        if not end_day:
            end_day = get_today()
        self.unit_report_request(start_day, end_day, cookie)
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
                        save_value[10] = round(float(save_value[10])/100, 4)
                    except:
                        pass
                    save_value[0] = str(save_value[0])
                    if save_value[0] not in values:
                        values[save_value[0]] = []
                    try:
                        save_value[21] = round(float(save_value[21])/100, 4)
                    except:
                        pass
                    try:
                        save_value[22] = round(float(save_value[22])/100, 4)
                    except:
                        pass
                    try:
                        save_value[36] = round(float(save_value[36])/100, 4)
                    except:
                        pass
                    change_week = 30 if change_day >= 30 else change_day
                    save_value.insert(0, change_week)
                    values[save_value[1]].append(tuple(save_value))
                for value in values:
                    ur_cost = 0
                    for data in values[value]:
                        ur_cost += float(data[10])
                    ur_costs = self.check_unit_report_msg(value)[0]
                    print(ur_costs, ur_cost, value)
                    if abs(float(ur_costs) - ur_cost) < 1:
                        self.sql_server.save_message('贝德美.dbo.直通车_单元报表', values[value])
                    else:
                        raise '花费不一致'
            f.close()
            os.remove(file_path)

    def unit_report_request(self, start_day, end_day, cookie):
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
            with open('单元.zip', 'wb')as w:
                w.write(cont)
            w.close()
            break

    def check_unit_report_msg(self, start_day):
        sql = f"select 花费 from 贝德美.dbo.直通车_账户报表 where 日期='{start_day}'"
        return self.sql_server.check_message(sql, 0)

    # 贝德美.dbo.直通车_关键词报表
    def keyword_report_main(self, start_day, cookie, end_day, token):
        sql = f"""delete from 贝德美.dbo.直通车_关键词报表 where 转化周期 < 30"""
        self.sql_server.check_message(sql, 2)
        if not start_day:
            start_day = self.sql_server.get_start_day('贝德美.dbo.直通车_关键词报表', '日期', '')
            print(start_day)
            if start_day == get_before_day(get_today()):
                return 0
            start_day = get_after_day(start_day)
        if not end_day:
            end_day = get_today()
        self.keyword_report_request(start_day, cookie, end_day, token)
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
                        save_value[11] = round(float(save_value[11])/100, 4)
                    except:
                        pass
                    save_value[0] = str(save_value[0])
                    if save_value[0] not in values:
                        values[save_value[0]] = []
                    try:
                        save_value[22] = round(float(save_value[22])/100, 4)
                    except:
                        pass
                    try:
                        save_value[23] = round(float(save_value[23])/100, 4)
                    except:
                        pass
                    try:
                        save_value[37] = round(float(save_value[37])/100, 4)
                    except:
                        pass
                    try:
                        save_value[38] = round(float(save_value[38])/100, 4)
                    except:
                        pass
                    change_week = 30 if change_day >= 30 else change_day
                    save_value.insert(0, change_week)
                    try:
                        good_id = self.check_good_id(save_value[5], start_day)[0]
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
                    ur_costs = self.check_unit_report_msg(value)[0]
                    # print(ur_costs, ur_cost, value)
                    if abs(float(ur_costs) - ur_cost) < 1:
                        self.sql_server.save_message('贝德美.dbo.直通车_关键词报表', values[value])
                    else:
                        raise '花费不一致'
            f.close()
            os.remove(file_path)

    def keyword_report_request(self, start_day, cookie, end_day, token):
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

    def check_good_id(self, dy_id, start_day):
        sql = f"SELECT top 1 商品id FROM [dbo].[直通车_单元报表] where 单元ID='{dy_id}'"
        return self.sql_server.check_message(sql, 0)

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


if __name__ == '__main__':
    tt = ThroughTrain()
    # 贝德美.dbo.直通车_账户报表
    # cookie = 't=ba991419abcabe60cd3884e42a2b30f4; __wpkreporterwid_=8fa9f0f4-e1f9-4a14-05f9-1ce8b82ece5a; thw=cn; cookie2=1f9299af1907012d87ad1bdc6b31c185; _tb_token_=531317e3585e1; _samesite_flag_=true; _m_h5_tk=82c4e3c4b03a3506a3709fa99d1a8d2b_1664185432453; _m_h5_tk_enc=25cc6dc28487c2240d8689f9153ef899; unb=2212731641217; sn=%E8%B4%9D%E5%BE%B7%E7%BE%8E%E6%97%97%E8%88%B0%E5%BA%97%3A%E9%BE%99%E9%A3%9E; cancelledSubSites=empty; v=0; sgcookie=E1007v3wd4OpOoll%2Be1qFCdmQYeQI3%2BMWDtIfQaEzIqMTeUEb8ExUjYqBalVGm5ZUkANJZTXie13dIFyY%2FvOqXFlmHRlw7JmmQ%2BMOJTvU1%2BMlS4%3D; uc1=cookie14=UoeyChACxXTc%2Fg%3D%3D&cookie21=U%2BGCWk%2F7oPIg; csg=6811490b; skt=ffdefa33c2df5692; _cc_=Vq8l%2BKCLiw%3D%3D; cna=nWYbGpuKHDsCAXkEs3F2iXa2; xlly_s=1; JSESSIONID=185831310D92E7528FB78A4DDFCCF4A0; tfstk=cOsdBvXEU5V34yNkbHUMagTRIbSdZkVJ1vOo2gvWTsW_HCiRi_jcDrMgRLO29RC..; l=eBSlN7-VTNKFSRf8BOfwourza77OSIRAguPzaNbMiOCPOX5e5NghW6u4Gp8wC3GVh6LkR3z1UrspBeYBqIfQ2hv1MexHfhMmn; isg=BMbGrpb92eN_iI0jfHWpX2CDF7xIJwrh2IRgzrDvsunEs2bNGLda8axFi-9_GwL5'
    # tt.check_user(cookie, '贝德美旗舰店')
    # token = tt.get_subway_token(cookie)
    # tt.account_statement_main('', '', cookie, token, '贝德美.dbo.直通车_账户报表')
    # # # # 贝德美.dbo.直通车_单元报表
    # tt.unit_report_main('', '', cookie, token)
    # # # 贝德美.dbo.直通车_关键词报表
    # tt.keyword_report_main('', cookie, '', token)

    # # 贝德美.BODORME.直通车_账户报表
    # cookie = 't=da03a3a2ff72f7a25e393fbd232e1134; cookie2=121ead4360c93f87765c152c6653fe17; _tb_token_=389583a0e66ae; _samesite_flag_=true; xlly_s=1; XSRF-TOKEN=0a07593e-dae5-434c-a168-6a9ead814ce8; cancelledSubSites=empty; v=0; _m_h5_tk=dbddd03a9291277daff1922ca6ac0205_1663819051599; _m_h5_tk_enc=afc5228bc7cc37d15f85037abd6f2a2b; sgcookie=E100SDdK1Kc%2F%2FIWjnQKu91SzJFM6tbN2FYSZSyLApofoYjdfcZnHND3lhS49IIle9N4XPcwlB4dRLDmKZFuWUqhCLe8i%2BvfLnhSORNLjfTyE884%3D; uc1=cookie14=UoeyDbC5KAXFXQ%3D%3D&cookie21=URm48syIZx9a; unb=2213334203009; sn=bodormebaby%E6%97%97%E8%88%B0%E5%BA%97%3A%E9%BE%99%E9%A3%9E; csg=5751f6dd; skt=ad6535e0559ec321; _cc_=Vq8l%2BKCLiw%3D%3D; cna=jWCxGw8o4HwCAXPG25PMGsWZ; l=eBE4J76mTrlCldBMKOfZourza77TSIRAguPzaNbMiOCPOFSD54YcW6oMjd9kCnGVh6m6R3lMfBR8BeYBqCm36l0cMexHfhMmn; tfstk=cz-RBQmG_jckhrgY9p3cTwF1Flf5Z_ldG813vHf4o6UIvirdiPxMX8wmP91NwxC..; isg=BJiYBnWbT1DOgWPV8PQWg7x6acYqgfwLKAd9PNKJ6FOGbThXepINmytDpaXd_bTj'
    # tt.check_user(cookie, 'bodormebaby旗舰店')
    # token = tt.get_subway_token(cookie)
    # tt.account_statement_main('', '', cookie, token, '贝德美.BODORME.直通车_账户报表')

    # 贝德美.TMCS.直通车_账户报表
    # cookie = 't=da03a3a2ff72f7a25e393fbd232e1134; cookie2=121ead4360c93f87765c152c6653fe17; _tb_token_=389583a0e66ae; _samesite_flag_=true; __wpkreporterwid_=08eb790e-219c-4364-1c94-8cee8705e366; _m_h5_tk=e9ccdf0f241068825cafdc08487d0be3_1664397348721; _m_h5_tk_enc=508440ce92b2c8658f5fbb62ce6fc57c; xlly_s=1; mt=ci=0_0; cna=jWCxGw8o4HwCAXPG25PMGsWZ; sgcookie=E100YiC4sEbRiT2C3N4zp3t6TvZ3sqS6yqcjmJbbsjSpzqDqowl0G52IkU8mcr9zfy5AbO8Vql1Ys3AMWj1cT8YcrKNTvNcpdFFgjIpW934lNH0%3D; unb=2211227458136; uc1=pas=0&cookie21=UIHiLt3xSw%3D%3D&cookie15=URm48syIIVrSKA%3D%3D&cookie14=UoeyChYV97T6ww%3D%3D&existShop=false&cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D; uc3=lg2=W5iHLLyFOGW7aA%3D%3D&id2=UUpgR1CZuQznIbZW7g%3D%3D&vt3=F8dCv4Sm6nRTt59ecZc%3D&nk2=EF2TYQY0F0dH5%2F4%3D; csg=57fbbb68; lgc=scm27891300; cancelledSubSites=empty; cookie17=UUpgR1CZuQznIbZW7g%3D%3D; dnk=scm27891300; skt=742ab528c55b40b5; existShop=MTY2NDQxODg3Ng%3D%3D; uc4=nk4=0%40EoTGjVAUdXJN3jYc2LCfdK9jjo2K7Q%3D%3D&id4=0%40U2gqyO3pcEiZXLDSGE5mx%2FK2FQbrkFTt; tracknick=scm27891300; _cc_=Vq8l%2BKCLiw%3D%3D; _l_g_=Ug%3D%3D; sg=069; _nk_=scm27891300; cookie1=AV1z4DhgRbgAIDoG84bMNy0IaVRkH3WLBGTVZtNEzNo%3D; JSESSIONID=7D032BE8F990E76A09E7382B975CD24D; tfstk=cNMCBwTVnwbB-bplKytw8AM6FR2PZrSbVBanAFkm8rEXNriCioW4le-mZaez2l1..; l=eBE4J76mTrlClaWXKOfZnurza779sIRAguPzaNbMiOCPOjCp563AW6uSJv89CnGVh636R3lMfBR8BeYBqI0VCal1MexHfhHmn; isg=BPDwLcU2Z8avnjvd6Lzue0Sywb5COdSDgP-FNOpBv8sepZBPkkvCE9CT_a3FNYxb'
    # tt.check_user(cookie, '二级供应商_浙江孕町母婴用品有限公司-寄售')
    # token = tt.get_subway_token(cookie)
    # tt.account_statement_main('', '', cookie, token, '贝德美.TMCS.直通车_账户报表')



