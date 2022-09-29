from Setting import *


class TMCS:
    def __init__(self):
        self._sql_server = SqlServerConnect()

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

    # 天猫超市
    def get_sale_day_main(self, start_day, end_day, cookie):
        if not start_day:
            start_day = self._sql_server.get_start_day('贝德美.TMCS.成交概况_日', '日期', '')
            if start_day == get_before_day(get_today()):
                return 0
            start_day = get_after_day(start_day)
        if not end_day:
            end_day = get_before_day(get_today())
        _scm_token_ = 'QMGXB69YlgLeMdbUGcEQ9e9HEEU'
        print(start_day, end_day)
        while True:
            response = self.get_sale_day_request(start_day, cookie, _scm_token_)
            datas = response['data']['data'][0]
            pay_ord_amt_1d = datas['pay_ord_amt_1d']  # 支付金额
            pay_ord_cnt_1d = datas['pay_ord_cnt_1d']  # 支付子订单数
            pay_itm_qty_1d = datas['pay_itm_qty_1d']  # 支付商品件数
            pay_pit_1d = datas['pay_pit_1d']  # 子订单均价
            pay_pbt_1d = datas['pay_pbt_1d']  # 客单价
            pay_byr_rate_1d = datas['pay_byr_rate_1d']  # 支付转化率
            ipvuv_1d = datas['ipvuv_1d']  # ipvuv
            pay_byr_cnt_1d = datas['pay_byr_cnt_1d']  # 支付用户数
            value = (start_day, pay_ord_amt_1d, pay_ord_cnt_1d, pay_itm_qty_1d, pay_pit_1d, pay_pbt_1d, pay_byr_rate_1d,
                     ipvuv_1d, pay_byr_cnt_1d)
            self._sql_server.save_message('贝德美.TMCS.成交概况_日', [value])
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)
            time.sleep(5)

    def get_sale_day_request(self, start_day, cookie, _scm_token_):
        '''
        params:
            start_time: 抓取的开始时间
            end_time： 抓取的结束时间
        return:
            获取数据并入库会将结果输出到控制台
        '''
        session = requests.session()
        session.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-length': '678',
            'content-type': 'application/json;charset=UTF-8',
            'cookie': cookie,
            'origin': 'https://web.txcs.tmall.com',
            'pragma': 'no-cache',
            'referer': 'https://web.txcs.tmall.com/pages/chaoshi/common_tj_index?_c_lang=zh-cn&iframeContainerFrom=tm&__IFRAME_CONTAINER_IFRAME_ID__=1&supplier_c=111394844&supplier_n=',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }

        url1 = 'https://ascp-dc.tmall.com/api/v1/queryData/api-ascp-dc-common_tj_index/metrics?code=74&_code=tmcs_tj%3Btmcs_tj_trd_supp_ent_1d.query%3BWDK_SI_XING&_cId=chart_4&componentType=chart&immediately=1'
        data = {"id": 10745, "code": "74", "_code": "tmcs_tj;tmcs_tj_trd_supp_ent_1d.query;WDK_SI_XING",
                "where": {"pageIndex": 1, "pageSize": 100, "wheres": [{"key": "brand_id", "op": "=", "value": "all"},
                                                                      {"key": "mcas_cate4_id", "op": "=",
                                                                       "value": "all"},
                                                                      {"key": "merchant_code", "op": "=",
                                                                       "value": "MAOCHAO"},
                                                                      {"key": "biz_type", "op": "=", "value": "all"},
                                                                      {"key": "stat_type", "op": "=", "value": "day"},
                                                                      {"key": "date_c", "op": "=",
                                                                       "value": start_day.replace('-', '')},
                                                                      {"key": "p_stat_date", "op": "=",
                                                                       "value": get_before_day(start_day).replace('-',
                                                                                                                  '')}],
                          "sorts": [], "pageTag": False}, "_scm_token_": _scm_token_}
        response1 = session.post(url=url1, json=data).json()
        url2 = 'https://ascp-dc.tmall.com/api/v1/queryData/api-ascp-dc-common_tj_index/metrics?code=74&_code=tmcs_tj%3Btmcs_tj_trd_supp_ent_1d.query%3BWDK_SI_XING&_cId=chart_4&componentType=chart&immediately=1'
        data = {
            'code': '74',
            '_code': 'tmcs_tj;tmcs_tj_trd_supp_ent_1d.query;WDK_SI_XING',
            '_cId': 'chart_4',
            'componentType': 'chart',
            'immediately': '1'
        }
        response2 = session.options(url=url2, data=data).text
        url3 = 'https://ascp-dc.tmall.com/api/v1/queryData/api-ascp-dc-common_tj_index/metrics?code=74&_code=tmcs_tj%3Btmcs_tj_trd_supp_ent_1d.query%3BWDK_SI_XING&_cId=chart_4&componentType=chart&immediately=1'
        data = {"id": 10745, "code": "74", "_code": "tmcs_tj;tmcs_tj_trd_supp_ent_1d.query;WDK_SI_XING",
                "where": {"pageIndex": 1, "pageSize": 100, "wheres": [{"key": "brand_id", "op": "=", "value": "all"},
                                                                      {"key": "mcas_cate4_id", "op": "=",
                                                                       "value": "all"},
                                                                      {"key": "merchant_code", "op": "=",
                                                                       "value": "MAOCHAO"},
                                                                      {"key": "biz_type", "op": "=", "value": "all"},
                                                                      {"key": "stat_type", "op": "=", "value": "day"},
                                                                      {"key": "date_c", "op": "=",
                                                                       "value": start_day.replace('-', '')},
                                                                      {"key": "p_stat_date", "op": "=",
                                                                       "value": get_before_day(start_day).replace('-',
                                                                                                                  '')}],
                          "sorts": [], "pageTag": False}, "_scm_token_": _scm_token_}
        time.sleep(2)
        response3 = session.post(url=url3, json=data).json()
        print(response3)
        return response3

    def get_scm_token_request(self, cookie):
        url = 'https://web.txcs.tmall.com/pages/chaoshi/common_tj_item?_c_lang=zh-cn&iframeContainerFrom=tm&__IFRAME_CONTAINER_IFRAME_ID__=1'
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': cookie,
            'pragma': 'no-cache',
            'referer': 'https://web.txcs.tmall.com/?frameUrl=https%3A%2F%2Fweb.txcs.tmall.com%2Fpages%2Fchaoshi%2Fcommon_tj_index',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'same-origin',
            'sec-fetch-site': 'same-origin',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        response = requests.get(url=url, headers=headers).text
        # print(response)
        return response.split('window._scm_token_ = ')[1].split(';')[0]

    # TMCS.商品分析_日
    def get_goods_commodity_analysis_main(self, start_day, end_day, cookie):
        if not start_day:
            start_day = self._sql_server.get_start_day('贝德美.TMCS.商品分析_日', '日期', '')
            if start_day == get_before_day(get_today()):
                print('今日数据获取完毕')
                return 0
            start_day = get_after_day(start_day)
        if not end_day:
            end_day = get_before_day(get_today())
        _scm_token_ = self.get_scm_token_request(cookie)[1:-1]
        # _scm_token_ = 'p-s1Ax6uMtX5P8D3MzAr0LnJA4s'
        # print(_scm_token_)
        while True:
            page = 1
            while True:
                response = self.get_goods_commodity_analysis_request(cookie, _scm_token_, start_day, page)
                datas = response['data']['data']
                if not datas:
                    break
                for data in datas:
                    region_name = data['region_name']  # 区域名称
                    item_id = data['item_id']  # 商品id
                    item_name = data['item_name']  # 商品名称
                    brand_name = data['brand_name']  # 品牌名称
                    supplier_name = data['supplier_name']  # 供应商名称
                    mcas_cate4_name = data['mcas_cate4_name']  # 类目名称
                    reserve_price = data['reserve_price']  # 一口价
                    pay_ord_cnt_1d = data['pay_ord_cnt_1d']  # 支付子订单数
                    pay_ord_amt_1d = data['pay_ord_amt_1d']  # 支付金额
                    pay_byr_cnt_1d = data['pay_byr_cnt_1d']  # 支付用户数
                    ipvuv_1d = data['ipvuv_1d']  # ipvuv_1d
                    add_cart_ipvuv_1d = data['add_cart_ipvuv_1d']  # 加购uv
                    pay_itm_qty_1d = data['pay_itm_qty_1d']  # 支付件数

                    value = (
                        start_day, '111394844', supplier_name, 'all', region_name, item_id, item_name, brand_name,
                        mcas_cate4_name, reserve_price,
                        pay_ord_cnt_1d, pay_ord_amt_1d, pay_byr_cnt_1d, ipvuv_1d, add_cart_ipvuv_1d, pay_itm_qty_1d)

                    self._sql_server.save_message('贝德美.TMCS.商品分析_日', [value])
                    page += 1
                time.sleep(5)

            if start_day == end_day:
                break
            start_day = get_after_day(start_day)

    def get_goods_commodity_analysis_request(self, cookie, _scm_token_, start_day, page):
        url = 'https://ascp-dc.tmall.com/api/v1/queryData/api-ascp-dc-common_tj_item/metrics?code=105&_code=tmcs_tj%3Btmcs_tj_itm_sku_rank_top_1d.query%3BWDK_SI_XING&_cId=chart_4&componentType=chart'
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-length': '542',
            'content-type': 'application/json;charset=UTF-8',
            'cookie': cookie,
            'origin': 'https://web.txcs.tmall.com',
            'pragma': 'no-cache',
            'referer': 'https://web.txcs.tmall.com/pages/chaoshi/common_tj_item?_c_lang=zh-cn&iframeContainerFrom=tm&__IFRAME_CONTAINER_IFRAME_ID__=2&supplier_c=111394844&supplier_n=',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        data = {"id": 11287, "code": "105", "_code": "tmcs_tj;tmcs_tj_itm_sku_rank_top_1d.query;WDK_SI_XING",
                "where": {"pageIndex": page, "pageSize": 10, "wheres": [{"key": "region_id", "op": "=", "value": "all"},
                                                                        {"key": "merchant_code", "op": "=",
                                                                         "value": "MAOCHAO"},
                                                                        {"key": "biz_type", "op": "=", "value": "all"},
                                                                        {"key": "stat_type", "op": "=", "value": "day"},
                                                                        {"key": "start_date", "op": "=",
                                                                         "value": start_day.replace('-', '')},
                                                                        {"key": "end_date", "op": "=",
                                                                         "value": start_day.replace('-', '')}],
                          "sorts": [{"key": "pay_ord_amt_1d", "value": "DESC"}, {"key": "stat_date", "value": "DESC"}]},
                "_scm_token_": _scm_token_}
        response = requests.post(url=url, headers=headers, json=data)
        print(response.text)
        return response.json()

    # TMCS_账户总览
    def tmcs_account_overview_main(self, start_day, cookie, end_day):
        sql = f"""delete from 贝德美.TMCS.万象台_账户总览 where 转化周期 < 30"""
        self._sql_server.check_message(sql, 2)
        if not start_day:
            start_day = self._sql_server.get_start_day('贝德美.TMCS.万象台_账户总览', '日期', '')
            print(start_day)
            if start_day == get_before_day(get_today()):
                return 0
            start_day = get_after_day(start_day)
        if not end_day:
            end_day = get_today()
        self.tmcs_account_overview_request(start_day, cookie, end_day)

    def tmcs_account_overview_request(self, start_day, cookie, end_day):
        csrfID = self._getcsrftoken4(cookie)
        print(csrfID)
        url = 'https://adbrain.taobao.com/api/account/report/findOverProductAccountDayList.json'
        # url = 'https://adbrain.taobao.com/api/account/report/chargeSummary.json'
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
        re_time = int(time.time() * 1000)
        params = {
            'r': 'mx_4009',
            'startTime': f'{start_day}',
            'endTime': f'{end_day}',
            'effect': '30',
            'unifyType': 'zhai',
            'bizCode': 'dkx',
            'timeStr': f'{re_time}',
            'dynamicToken': '220204212220212224228192432216192428484204388420',
            'csrfID': f'{csrfID}',
            'webOpSessionId': 'lxsnrbknels'
        }
        response = requests.get(url=url, headers=headers, params=params).json()
        # print(response)
        # exit()
        datas = response['data']['list']
        for data in datas:
            # print(data)
            logDate = data['logDate']  # 日期
            charge = data['charge']  # 消耗
            adPv = data['adPv']  # 曝光量
            click = data['click']  # 点击量
            ctr = data['ctr']  # 点击率
            ecpc = data['ecpc']  # 点击成本
            cartNum = data['cartNum']  # 总加购量
            dirCartNum = data['dirCartNum']  # 直接加购数
            indirCartNum = data['indirCartNum']  # 间接加购数
            inshopItemColNum = data['inshopItemColNum']  # 总收藏量
            actionNum = data['actionNum']  # 加购收藏量
            inshopItemColCartNumCost = data['inshopItemColCartNumCost']  # 加购收藏成本
            alipayInshopAmt = data['alipayInshopAmt']  # 总成交金额
            dirAlipayInshopAmt = data['dirAlipayInshopAmt']  # 直接成交金额
            indirAlipayInshopAmt = data['indirAlipayInshopAmt']  # 间接成交金额
            alipayInShopNum = data['alipayInShopNum']  # 总成交笔数
            dirAlipayInShopNum = data['dirAlipayInShopNum']  # 直接成交笔数
            indirAlipayInShopNum = data['indirAlipayInShopNum']  # 间接成交笔数
            cvr = data['cvr']  # 成交转化率
            roi = data['roi']  # roi
            week = int((get_time_number(get_today()) - get_time_number(logDate)) / (60 * 60 * 24))
            if week > 30:
                week = 30
            value = (
                week, logDate, charge, adPv, click, ctr, ecpc, cartNum, dirCartNum, indirCartNum, inshopItemColNum,
                actionNum, inshopItemColCartNumCost, alipayInshopAmt, dirAlipayInshopAmt, indirAlipayInshopAmt,
                alipayInShopNum, dirAlipayInShopNum, indirAlipayInShopNum, cvr, roi, 0, 0)
            print(value)
            self._sql_server.save_message('贝德美.TMCS.万象台_账户总览', [value])

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


if __name__ == '__main__':
    tmcs = TMCS()
    # 贝德美.TMCS.直通车_账户报表
    tmcs.check_user(tmcs_ztc_cookie, '二级供应商_浙江孕町母婴用品有限公司-寄售')
    token = tmcs.get_subway_token(tmcs_ztc_cookie)
    tmcs.through_train_account_statement_main('', '', tmcs_ztc_cookie, '贝德美.TMCS.直通车_账户报表', token)

    # TMCS.成交概况_日
    tmcs.get_sale_day_main('', '', tmcs_cookie)

    # TMCS.商品分析_日
    tmcs.get_goods_commodity_analysis_main('', '', tmcs_cookie)