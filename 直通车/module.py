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
    # cookie = 't=ba991419abcabe60cd3884e42a2b30f4; __wpkreporterwid_=8fa9f0f4-e1f9-4a14-05f9-1ce8b82ece5a; cookie2=1d11a579ddc9331e331a8cbf42b950a2; _samesite_flag_=true; _tb_token_=e3eb39a84fbbe; cancelledSubSites=empty; unb=2212731641217; sn=%E8%B4%9D%E5%BE%B7%E7%BE%8E%E6%97%97%E8%88%B0%E5%BA%97%3A%E9%BE%99%E9%A3%9E; v=0; _m_h5_tk=79c4475a191d2f2bb1ce1ac05e160c74_1658806564036; _m_h5_tk_enc=d771114e2758c6bb77ad4734ddd6bddc; xlly_s=1; sgcookie=E100oHWRNxqXFV4P0dlgtsIcwORjYTLF9J7nm60bohKR2x%2BRikUmpGE9irCJJdh8oOHuEB9BmTlG60Wx2DAd37FmV9IR0xJL0O2glFP2ppi32A0%3D; uc1=cookie14=UoexOtk7mzRdTw%3D%3D&cookie21=V32FPkk%2FhSg%2F; csg=fb052da9; skt=c44e2d5b3d943b29; _cc_=W5iHLLyFfA%3D%3D; cna=nWYbGpuKHDsCAXkEs3F2iXa2; JSESSIONID=99E7E53FC68B5484C2A9BE79E755C4CF; tfstk=cycNIQMAJCda1JMrLWN2liY_yvSbG_RZSqfUPRxSih27SdxzFu5mxiUnRPUUlwS0I; l=eB_anV6cgpC-RqEfBO5Zourza779mIRfGsPzaNbMiIncB6nsQFp1fN-Q0w90CW-5WhQNns6wR3Wrj_IwBR88Xy4Eh3pdVeW_-zSofdKP.; isg=BMPDrsgWpfXfXGrNZXRkfaukUodtOFd6enHoJ_WgnCKZtOfWfQxCy69iLkT6FK9y'
    # tt.check_user(cookie, '贝德美旗舰店')
    # token = tt.get_subway_token(cookie)
    # tt.account_statement_main('', '', cookie, token, '贝德美.dbo.直通车_账户报表')
    # # # # 贝德美.dbo.直通车_单元报表
    # tt.unit_report_main('', '', cookie, token)
    # # # 贝德美.dbo.直通车_关键词报表
    # tt.keyword_report_main('', cookie, '', token)
    # #
    # # 贝德美.BODORME.直通车_账户报表
    # cookie = '_samesite_flag_=true; cookie2=14ddb4a56cce7567b01d80c90c00b3c7; t=8017ee70287cb1ebffabe3247a6d01b6; _tb_token_=e9e673b74b6e3; XSRF-TOKEN=dfb7bae8-21bd-4be7-9e85-287334fce5d8; _m_h5_tk=ae505610c85892f299a18ae5bc89c96e_1663126727603; _m_h5_tk_enc=60a4ab18268e5e87c087799ea3a1c1c8; xlly_s=1; cancelledSubSites=empty; sgcookie=E100jOCGVi%2BGstR3ab4kEiGOAlPe3W0%2FqNL%2FgYLncNBdnVzM6Wa3Z8DFGLFzFRRo6W7yCA6hY0v7RqgQAj9Q1uocaI7G12nBziCuPHrymabs3uA%3D; uc1=cookie14=UoeyDblSPsq8AA%3D%3D&cookie21=UtASsssmfufd; unb=2213334203009; sn=bodormebaby%E6%97%97%E8%88%B0%E5%BA%97%3A%E9%BE%99%E9%A3%9E; _cc_=U%2BGCWk%2F7og%3D%3D; csg=e154af60; skt=b91b4ae2b8906609; cna=B86mGwVewTECAXPDhgk9aeut; l=eBNhYW9VTEW_wqrFKOfwourza77OSIRAguPzaNbMiOCP9Dbe5AiGW6obmPRwC3GVh6QvR3lMfBR8BeYBqIjO7aVGMexHfhMmn; tfstk=cl4lBdNS6uoWYmFaTzg58bmYjlMFZU8EIyzbu_HerIp_s8aVivx2bqMdiYX1UH1..; isg=BN_f1yB1wLd_P8SVgVR1qgWbbjNpRDPmO3qaaXEsew7VAP-CeRTDNl3WwpB-mAte'
    # tt.check_user(cookie, 'bodormebaby旗舰店')
    # token = tt.get_subway_token(cookie)
    # tt.account_statement_main('', '', cookie, token, '贝德美.BODORME.直通车_账户报表')

    # 贝德美.TMCS.直通车_账户报表
    # cookie = '_samesite_flag_=true; cookie2=14ddb4a56cce7567b01d80c90c00b3c7; t=8017ee70287cb1ebffabe3247a6d01b6; _tb_token_=e9e673b74b6e3; __wpkreporterwid_=8dec3a95-aa5c-4111-2538-f5e0c62b5403; xlly_s=1; _m_h5_tk=8b409ed1ea58cedcca7a884e578251a8_1663646528360; _m_h5_tk_enc=eed9cffc3ed4c1699ff07d661defb90d; thw=cn; cancelledSubSites=empty; cna=B86mGwVewTECAXPDhgk9aeut; sgcookie=E100f0zhn2FxqPNBhbvXJ7RdmiN%2BVZ4G2acAoIeuZF2XVqfZ41mz7PKEcOLtAgGOOIuh7MorNdC1xXSGO0qZ7K1blmT8a1JcrwZaQhcQIwmXlZs%3D; unb=2211227458136; uc1=cookie21=UIHiLt3xSw%3D%3D&cookie16=VT5L2FSpNgq6fDudInPRgavC%2BQ%3D%3D&cookie14=UoeyDb7mgWlyUA%3D%3D&pas=0&existShop=false&cookie15=V32FPkk%2Fw0dUvg%3D%3D; uc3=nk2=EF2TYQY0F0dH5%2F4%3D&vt3=F8dCv4U2YubqMJS9pXM%3D&id2=UUpgR1CZuQznIbZW7g%3D%3D&lg2=UtASsssmOIJ0bQ%3D%3D; csg=a49e7f1a; lgc=scm27891300; cookie17=UUpgR1CZuQznIbZW7g%3D%3D; dnk=scm27891300; skt=b96a81338081bf4a; existShop=MTY2MzY0MTk4NQ%3D%3D; uc4=id4=0%40U2gqyO3pcEiZXLDSGE5mx%2FKxMvyOimO4&nk4=0%40EoTGjVAUdXJN3jYc2LCfc0EN%2BWRPeA%3D%3D; tracknick=scm27891300; _cc_=Vq8l%2BKCLiw%3D%3D; _l_g_=Ug%3D%3D; sg=069; _nk_=scm27891300; cookie1=AV1z4DhgRbgAIDoG84bMNy0IaVRkH3WLBGTVZtNEzNo%3D; JSESSIONID=DA054F35DCF3700047CA23798C123C73; tfstk=cTslBAXWBa8Waakmxat7YaW1agm5ZDoesMSf08InMZOR1LjVi60q7nOLnQV_a21..; l=eBNhYW9VTEW_w_RXBOfZourza77TxIRAguPzaNbMiOCP_uvw5Mf5W6osMjjeCnGVhssJJ3lMfBR8BeYBqCm36l0mK6Po_fkmn; isg=BHd3Qpaf2Gc8zlzdViYva3BIBmvBPEueU_Jiockk2MateJe60A1T7l9WWtgmkCMW'
    # tt.check_user(cookie, '二级供应商_浙江孕町母婴用品有限公司-寄售')
    # token = tt.get_subway_token(cookie)
    # tt.account_statement_main('', '', cookie, token, '贝德美.TMCS.直通车_账户报表')



