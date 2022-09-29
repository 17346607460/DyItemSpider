import time

import requests
import xlrd
from lxml import etree
import execjs
from auto_login import *
from Setting import *



class LittleRedBook:
    def __init__(self):
        self._sql_server = SqlServerConnect()

    # 创意报告主函数
    def creative_report_main(self, start_day, end_day, cookie, table, user_name):
        try:
            if not start_day:
                sql1 = f"""select 日期 from {table} where 推广者 = '{user_name}' order by 日期 desc"""
                day = self._sql_server.check_message(sql1, 0)[0]
                if str(day) == get_before_day(get_today()):
                    print('今天数据已经跑完')
                    return 0
                start_day = get_after_day(
                    self._sql_server.get_start_day(table, '日期', {'转化周期': 7, '推广者': user_name}))
            if not end_day:
                end_day = get_before_day(get_today())
            # sql = f"""delete from {table} where 转化周期 < 7 and 推广者 = '{user_name}'"""
            # self._sql_server.check_message(sql, 2)
            print(start_day, end_day)
            while True:
                values = []
                page = 1
                while 1:
                    response = self.creative_report_request(start_day, start_day, cookie, table, page)
                    print(response)
                    datas = response['data']['detailList']
                    if not datas:
                        break
                    for data in datas:
                        print(data)
                        save_time = data['time']  # 日期
                        campaignId = data['campaignId']  # 计划id
                        campaignName = data['campaignName']  # 计划名称
                        unitId = data['unitId']  # 单元id
                        unitName = data['unitName']  # 单元名称
                        creativityId = data['creativityId']  # 创意id
                        marketingTargetName = data['marketingTargetName']  # 营销目标
                        promotionTargetName = data['promotionTargetName']  # 投放目标
                        promotionTargetId = data['promotionTargetId']  # 投放目标id
                        placementName = data['placementName']  # 投放范围
                        materialTypeName = data['materialTypeName']  # 创意类型
                        materialTypeId = data['materialTypeId']  # 创意类型id
                        jumpTypeName = data['jumpTypeName']  # 跳转类型
                        impression = data['impression']  # 展现量
                        click = data['click']  # 点击量
                        fee = data['fee']  # 消费

                        ctr = round(float(data['ctr']) / 100, 4)  # 点击率
                        acp = data['acp']  # 平均点击成本
                        cpm = data['cpm']  # 平均千次展现费用
                        fav = data['fav']  # 点赞
                        comment = data['comment']  # 评论
                        collect = data['collect']  # 收藏
                        messageCount = data['messageCount']  # 私信条数
                        messageUser = data['messageUser']  # 私信人数
                        follow = data['follow']  # 关注
                        rgmv = data['rgmv']  # rgmv
                        addCart = data['addCart']  # 加入购物车次数
                        totalOrder = data['totalOrder']  # 下单订单数
                        successOrder = data['successOrder']  # 成交订单数
                        buyNow = data['buyNow']  # 立即购买次数
                        roi = data['roi']  # 投入产出比
                        clickCvr = data['clickCvr']  # 点击转化率
                        goodsViewPv = data['goodsViewPv']  # 商品访问量
                        ldyfwl = 0  # 落地页访问量
                        bdanbgl = 0  # 表单按钮曝光量
                        actionButtonClickNum = data['actionButtonClickNum']  # 行动按钮点击量
                        try:
                            actionButtonCtr = round(float(data['actionButtonCtr']) / 100, 4)  # 行动按钮点击率
                        except:
                            pass

                        week = int((get_time_number(get_today()) - get_time_number(save_time)) / (60 * 60 * 24))
                        if week > 7:
                            week = 7
                        if table == '贝德美.XHS.企业号_推广中心_创意报表':
                            value = [
                                save_time, week, user_name, campaignId, campaignName, unitId, unitName, creativityId,
                                marketingTargetName,
                                promotionTargetName, promotionTargetId, placementName, materialTypeName, materialTypeId,
                                jumpTypeName, impression, click, fee, ctr, acp, cpm, fav, comment, collect, follow,
                                ldyfwl,
                                bdanbgl,
                                actionButtonClickNum, actionButtonCtr, addCart, buyNow, totalOrder, successOrder, rgmv,
                                roi,
                                goodsViewPv, clickCvr, 0, 0, messageUser,
                                messageCount]
                        if table == '贝德美.XHS.企业号_推广中心_计划报表':
                            value = [save_time, week, user_name, campaignName, campaignId, marketingTargetName, None,
                                     None, None, None, None, None, fee, impression, click, ctr, acp, cpm, fav, comment,
                                     collect, follow, None, None, None, actionButtonClickNum, actionButtonCtr, None,
                                     None, addCart, buyNow, totalOrder, successOrder, clickCvr, rgmv, roi, goodsViewPv,
                                     0, 0, ldyfwl, bdanbgl, messageUser, messageCount, None]
                        if table == '贝德美.XHS.企业号_推广中心_单元报表':
                            value = [
                                save_time, week, user_name, campaignId, campaignName, unitId, unitName,
                                marketingTargetName, promotionTargetName, promotionTargetId, placementName,
                                jumpTypeName,
                                impression, click, fee, ctr, acp, cpm, fav, comment, collect, follow, ldyfwl, bdanbgl,
                                actionButtonClickNum, actionButtonCtr, addCart, buyNow, totalOrder, successOrder,
                                rgmv, roi, goodsViewPv, clickCvr, 0, 0, messageUser,
                                messageCount]
                        if table == '贝德美.XHS.企业号_推广中心_关键词报表':
                            bidword = data['bidword']  # 搜索词
                            value = [
                                save_time, week, user_name, campaignId, campaignName, unitId, unitName, bidword,
                                marketingTargetName, promotionTargetName, promotionTargetId,
                                impression, click, fee, ctr, acp, cpm, fav, comment, collect, follow, ldyfwl, bdanbgl,
                                addCart, buyNow, totalOrder, successOrder,
                                rgmv, roi, goodsViewPv, clickCvr, 0, 0]
                        new_value = []
                        for item in value:
                            if item == '-':
                                item = None
                            new_value.append(item)
                        print(new_value)
                        if new_value not in values:
                            try:
                                self._sql_server.save_message(table, [tuple(new_value)])
                            except:
                                pass
                            values.append(tuple(new_value))
                    page += 1
                    time.sleep(5)
                if start_day == end_day:
                    break
                start_day = get_after_day(start_day)
            # self._sql_server.save_message(table, values)
        except:
            error_message(0)

    # 创意报告请求函数
    def creative_report_request(self, start_day, end_day, cookie, table, page):
        url = 'https://pro.xiaohongshu.com/api/eros/rtb/get_common_data_report'
        if table == '贝德美.XHS.企业号_推广中心_创意报表':
            data = {"reportType": "CREATIVITY", "startDate": start_day, "endDate": end_day, "timeUnit": "DAY",
                    "sorts": [{"column": "rgmv", "sort": "desc"}], "splitColumns": ["placement", "jumpType"],
                    "columns": ["time", "creativityId", "placementName", "jumpTypeName", "campaignName",
                                "campaignId",
                                "marketingTargetName", "unitName", "unitId", "promotionTargetName",
                                "promotionTargetId",
                                "materialTypeName", "materialTypeId", "bidType", "fee", "impression", "click",
                                "ctr",
                                "acp",
                                "cpm", "addCart", "buyNow", "totalOrder", "successOrder", "clickCvr", "rgmv", "roi",
                                "goodsViewPv", "leads", "cpl", "landingPagePv", "landingFormImpNum", "validLeads",
                                "validCpl", "fav", "comment", "collect", "follow", "share", "interaction", "cpi",
                                "actionButtonClickNum", "actionButtonCtr", "messageUser", "messageCount",
                                "messageOpenCount"], "pageIndex": page, "pageSize": 20, "needTotal": True,
                    "needSize": True,
                    "needList": True}
        if table == '贝德美.XHS.企业号_推广中心_计划报表':
            data = {"reportType": "CAMPAIGN", "startDate": start_day, "endDate": end_day, "timeUnit": "DAY",
                    "sorts": [], "splitColumns": ["placement", "jumpType"],
                    "columns": ["time", "placementName", "jumpTypeName", "campaignName", "campaignId",
                                "marketingTargetName", "fee", "impression", "click", "ctr", "acp", "cpm", "addCart",
                                "buyNow", "totalOrder", "successOrder", "clickCvr", "rgmv", "roi", "goodsViewPv",
                                "leads", "cpl", "landingPagePv", "landingFormImpNum", "validLeads", "validCpl",
                                "fav",
                                "comment", "collect", "follow", "share", "interaction", "cpi",
                                "actionButtonClickNum",
                                "actionButtonCtr", "messageUser", "messageCount", "messageOpenCount"],
                    "pageIndex": page,
                    "pageSize": 20, "needTotal": True, "needSize": True, "needList": True}
        if table == '贝德美.XHS.企业号_推广中心_单元报表':
            data = {"reportType": "UNIT", "startDate": start_day, "endDate": end_day, "timeUnit": "DAY",
                    "sorts": [], "splitColumns": ["jumpType", "placement"],
                    "columns": ["time", "placementName", "jumpTypeName", "campaignName", "campaignId",
                                "marketingTargetName", "unitName", "unitId", "promotionTargetName",
                                "promotionTargetId",
                                "bidType", "fee", "impression", "click", "ctr", "acp", "cpm", "addCart", "buyNow",
                                "totalOrder", "successOrder", "clickCvr", "rgmv", "roi", "goodsViewPv", "leads",
                                "cpl",
                                "landingPagePv", "landingFormImpNum", "validLeads", "validCpl", "fav", "comment",
                                "collect", "follow", "share", "interaction", "cpi", "actionButtonClickNum",
                                "actionButtonCtr", "messageUser", "messageCount", "messageOpenCount"],
                    "pageIndex": page,
                    "pageSize": 20, "needTotal": True, "needSize": True, "needList": True}
        if table == '贝德美.XHS.企业号_推广中心_关键词报表':
            data = {"reportType": "BIDWORD", "startDate": start_day, "endDate": end_day, "timeUnit": "DAY",
                    "sorts": [], "splitColumns": ["campaignId", "unitId"],
                    "columns": ["time", "bidword", "campaignName", "campaignId", "marketingTargetName", "unitName",
                                "unitId", "promotionTargetName", "promotionTargetId", "bidType", "fee",
                                "impression",
                                "click", "ctr", "acp", "cpm", "firstRank", "thirdRank", "sov", "firstClickRank",
                                "thirdClickRank", "addCart", "buyNow", "totalOrder", "successOrder", "clickCvr",
                                "rgmv",
                                "roi", "goodsViewPv", "leads", "cpl", "landingPagePv", "landingFormImpNum",
                                "validLeads", "validCpl", "fav", "comment", "collect", "follow", "optimizeTarget"],
                    "pageIndex": page, "pageSize": 20, "needTotal": True, "needSize": True, "needList": True}
        with open(r'C:\Users\lianqinglongfei\Desktop\DyItemSpider\小红书\x-t.js', 'r') as f:
            b = f.read()
        msg = '/api/eros/rtb/get_common_data_report'
        infos = execjs.compile(b).call('get_info', msg, data)
        print(infos)
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-length': '288',
            'content-type': 'application/json;charset=UTF-8',
            'cookie': cookie,
            'origin': 'https://pro.xiaohongshu.com',
            'pragma': 'no-cache',
            'referer': 'https://pro.xiaohongshu.com/ares/advertising/microapp/datareport/creativity',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'x-b3-traceid': infos[2],
            'x-s': infos[0],
            'x-t': str(infos[1])
        }
        response = requests.post(url=url, headers=headers, json=data).json()
        return response

    # 商品整体日
    def commodity_as_a_whole_main(self, start_day, end_day, cookie):
        while True:
            if not start_day:
                start_day = self._sql_server.get_start_day('贝德美.XHS.商品效果_日', '日期', '')
                if str(start_day) == get_before_day(get_today()):
                    print('今天数据已经跑完')
                    return 0
                start_day = get_after_day(start_day)
            if not end_day:
                end_day = get_before_day(get_today())
            data = {"task_name": "batch_download_data_ark_hive", "module_name": "ark_data_center", "input": {
                "extra": {"type": 1, "data_type": 1, "seller_id": "5ee9bc9021adbc000127ef5a",
                          "fields": ["goods_name", "country", "barcode", "create_time", "spu_id", "goods_id", "skucode",
                                     "ipq", "first_category_name", "second_category_name", "third_category_name",
                                     "forth_category_name", "business_line", "brand_name", "buyable",
                                     "in_stock_inventory",
                                     "is_new_goods", "price_pre_tax", "price_post_tax", "price_tax_amount",
                                     "price_tax_rate", "min_price_pre_tax_30d", "min_price_post_tax_30d",
                                     "strict_min_price_pre_tax_90d", "strict_min_price_post_tax_90d", "price_type",
                                     "uv",
                                     "pv", "pv_uv_rate", "wish_list_user_cnt", "wish_list_user_cnt_acc",
                                     "add_cart_user_cnt", "add_cart_user_cnt_acc", "add_cart_goods_cnt",
                                     "add_cart_goods_cnt_acc", "frequent_visitor", "new_visitor", "pgmv_without_refund",
                                     "deal_gmv", "up_uv_rate_without_refund", "rgmv_uv_rate",
                                     "pgmv_up_rate_without_refund",
                                     "refund_amount", "up_without_refund", "sale_qty_without_refund",
                                     "frequent_customer_cnt_without_refund", "new_customer_cnt_without_refund"],
                          "start_date": start_day, "end_date": start_day, "first_category_name": "",
                          "second_category_name": "", "buyable": ""}}}
            response = self.Commodity_as_a_whole_request(data, cookie)
            task_id = response['data']['task_id']
            time.sleep(1)
            while True:
                try:
                    response = self.Commodity_as_a_whole_request2(task_id, cookie)
                    print(response)
                    private_url = response['data']['private_url']
                    print(private_url)
                    time.sleep(5)
                    self.Commodity_as_a_whole_request3(private_url, cookie)
                    break
                except:
                    time.sleep(5)
                    pass
            values = []
            with open(f'11.csv', 'r', encoding='utf-8') as f:
                f_csv = csv.reader(f)
                for row in f_csv:
                    if '\ufeff周期' in row:
                        title = row
                        continue
                    info_dic = {a.strip(): None if b == '' or b == ' ' else b.strip() for a, b in zip(title, row)}
                    value = (start_day, info_dic['商品名称'], info_dic['国家/地区'], info_dic['BARCODE'], info_dic['商品创建时间'],
                             info_dic['SPUID'], info_dic['商品ID'], info_dic['SKU编码'], info_dic['打包数量'], info_dic['一级类目'],
                             info_dic['二级类目'], info_dic['三级类目'], info_dic['四级类目'], info_dic['业务条线'], info_dic['品牌名称'],
                             1 if info_dic['可购买'] else 0, info_dic['SKU在库库存'], 1 if info_dic['新草标'] else 0,
                             info_dic['最新商品税前价'],
                             info_dic['最新商品税后价(跨境商品)'], info_dic['最新商品税金(跨境商品)'], info_dic['最新商品跨境税率(跨境商品)'],
                             info_dic['过去30天最低税前价'], info_dic['过去30天最低税后价(跨境商品)'], info_dic['过去90天最低税前价'],
                             info_dic['过去90天最低税后价(跨境商品)'], info_dic['价格是否包税(跨境商品)'], info_dic['访客数'], info_dic['浏览量'],
                             info_dic['人均浏览量'], info_dic['新增加入心愿单人数'], info_dic['加入心愿单人数'], info_dic['新增加购人数'],
                             info_dic['加购人数'], info_dic['新增加购件数'], info_dic['加购件数'], info_dic['老访客数'], info_dic['新访客数'],
                             info_dic['支付金额'], info_dic['实付金额'], info_dic['支付转化率'], info_dic['UV价值'], info_dic['客单价'],
                             info_dic['成功退款金额'], info_dic['支付买家数'], info_dic['支付件数'], info_dic['支付老买家数'],
                             info_dic['支付新买家数'])
                    if value not in values:
                        values.append(value)
            f.close()
            self._sql_server.save_message('贝德美.XHS.商品效果_日', values)
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)

    # 店铺整体日
    def overall_store_day_main(self, start_day, end_day, cookie):
        while True:
            if not start_day:
                start_day = self._sql_server.get_start_day('贝德美.XHS.店铺整体_日', '日期', '')
                if str(start_day) == get_before_day(get_today()):
                    print('今天数据已经跑完')
                    return 0
                start_day = get_after_day(start_day)
            if not end_day:
                end_day = get_before_day(get_today())
            data = {"task_name": "batch_download_data_ark_hive", "module_name": "ark_data_center", "input": {
                "extra": {"type": 1, "data_type": 3, "seller_id": "5ee9bc9021adbc000127ef5a",
                          "fields": ["uv", "pv", "pv_uv_rate", "wish_list_user_cnt", "wish_list_user_cnt_acc",
                                     "add_cart_user_cnt", "add_cart_user_cnt_acc", "add_cart_goods_cnt",
                                     "add_cart_goods_cnt_acc", "ads_uv", "ads_pv", "frequent_visitor", "new_visitor",
                                     "pgmv_without_refund", "deal_gmv", "up_uv_rate_without_refund", "rgmv_uv_rate",
                                     "pgmv_up_rate_without_refund", "refund_amount", "up_without_refund",
                                     "sale_qty_without_refund", "frequent_customer_cnt_without_refund",
                                     "new_customer_cnt_without_refund", "ads_order_user_cnt", "ads_rgmv", "ads_fee"],
                          "start_date": start_day, "end_date": start_day}}}
            response = self.Commodity_as_a_whole_request(data, cookie)
            task_id = response['data']['task_id']
            time.sleep(1)
            while True:
                try:
                    response = self.Commodity_as_a_whole_request2(task_id, cookie)
                    print(response)
                    private_url = response['data']['private_url']
                    print(private_url)
                    time.sleep(5)
                    # private_url = "https://bricole.xhscdn.com/jbds%2Fbatch_download_data_ark_hive%2F09f27b6ab08c614f790b500e69065073.csv?attname=%E5%BA%97%E9%93%BA%E6%95%B0%E6%8D%AE%E6%8C%89%E6%97%A52022-06-13_2022-06-13.csv&e=1655181370&token=edMBpdzSWI2pH13onoAIcpYw7pSU2tplRrPTySQO:ShUfnjWZNEJG84OdTIS2kjhu5r4="
                    self.Commodity_as_a_whole_request3(private_url, cookie)
                    break
                except:
                    time.sleep(5)
                    pass
            values = []
            with open(f'11.csv', 'r', encoding='utf-8') as f:
                f_csv = csv.reader(f)
                for row in f_csv:
                    if '\ufeff周期' in row:
                        title = row
                        continue
                    info_dic = {a.strip(): None if b == '' or b == ' ' else b.strip() for a, b in zip(title, row)}
                    value = (start_day, info_dic['访客数'], info_dic['浏览量'], info_dic['人均浏览量'], info_dic['新增加入心愿单人数'],
                             info_dic['加入心愿单人数'], info_dic['新增加购人数'], info_dic['加购人数'], info_dic['新增加购件数'],
                             info_dic['加购件数'],
                             info_dic['广告访客数'], info_dic['广告浏览量'], info_dic['老访客数'], info_dic['新访客数'], info_dic['支付金额'],
                             info_dic['实付金额'],
                             info_dic['支付转化率'], info_dic['UV价值'], info_dic['客单价'],
                             info_dic['成功退款金额'], info_dic['支付买家数'], info_dic['支付件数'],
                             info_dic['支付老买家数'], info_dic['支付新买家数'], info_dic['广告交易买家数'], info_dic['广告交易金额'],
                             info_dic['广告花费'])
                    if value not in values:
                        values.append(value)
            f.close()
            self._sql_server.save_message('贝德美.XHS.店铺整体_日', values)
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)

    # 店铺整体月
    def overall_store_month_main(self, start_day, end_day, cookie):
        while True:
            if not start_day:
                start_day = self._sql_server.get_start_day('贝德美.XHS.店铺整体_月', '月份', '')
                if start_day[4:] + start_day[:-2] == get_before_month(get_month()):
                    print('今天数据已经跑完')
                    return 0
                start_day = get_after_day(start_day)
            if not end_day:
                end_day = get_before_day(get_today())
            data = {"task_name": "batch_download_data_ark_hive", "module_name": "ark_data_center", "input": {
                "extra": {"type": 1, "data_type": 3, "seller_id": "5ee9bc9021adbc000127ef5a",
                          "fields": ["uv", "pv", "pv_uv_rate", "wish_list_user_cnt", "wish_list_user_cnt_acc",
                                     "add_cart_user_cnt", "add_cart_user_cnt_acc", "add_cart_goods_cnt",
                                     "add_cart_goods_cnt_acc", "ads_uv", "ads_pv", "frequent_visitor", "new_visitor",
                                     "pgmv_without_refund", "deal_gmv", "up_uv_rate_without_refund", "rgmv_uv_rate",
                                     "pgmv_up_rate_without_refund", "refund_amount", "up_without_refund",
                                     "sale_qty_without_refund", "frequent_customer_cnt_without_refund",
                                     "new_customer_cnt_without_refund", "ads_order_user_cnt", "ads_rgmv", "ads_fee"],
                          "start_date": start_day, "end_date": start_day}}}
            response = self.Commodity_as_a_whole_request(data, cookie)
            task_id = response['data']['task_id']
            time.sleep(1)
            while True:
                try:
                    response = self.Commodity_as_a_whole_request2(task_id, cookie)
                    print(response)
                    private_url = response['data']['private_url']
                    print(private_url)
                    self.Commodity_as_a_whole_request3(private_url, cookie)
                    break
                except:
                    time.sleep(5)
                    pass
            values = []
            with open(f'11.csv', 'r', encoding='utf-8') as f:
                f_csv = csv.reader(f)
                for row in f_csv:
                    if '\ufeff周期' in row:
                        title = row
                        continue
                    info_dic = {a.strip(): None if b == '' or b == ' ' else b.strip() for a, b in zip(title, row)}
                    value = (start_day, info_dic['访客数'], info_dic['浏览量'], info_dic['人均浏览量'], info_dic['新增加入心愿单人数'],
                             info_dic['加入心愿单人数'], info_dic['新增加购人数'], info_dic['加购人数'], info_dic['新增加购件数'],
                             info_dic['加购件数'],
                             info_dic['广告访客数'], info_dic['广告浏览量'], info_dic['老访客数'], info_dic['新访客数'], info_dic['支付金额'],
                             info_dic['实付金额'],
                             info_dic['支付转化率'], info_dic['UV价值'], info_dic['客单价'],
                             info_dic['成功退款金额'], info_dic['支付买家数'], info_dic['支付件数'],
                             info_dic['支付老买家数'], info_dic['支付新买家数'], info_dic['广告交易买家数'], info_dic['广告交易金额'],
                             info_dic['广告花费'])
                    if value not in values:
                        values.append(value)
            f.close()
            self._sql_server.save_message('贝德美.XHS.店铺整体_月', values)
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)

    def Commodity_as_a_whole_request(self, data, cookie):
        url = 'https://ark.xiaohongshu.com/ark/api/v1/long_task/task/submit'
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-length': '1157',
            'content-type': 'application/json;charset=UTF-8',
            'cookie': cookie,
            'origin': 'https://ark.xiaohongshu.com',
            'pragma': 'no-cache',
            'referer': 'https://ark.xiaohongshu.com/ark/sale-data/download-center/takeFew',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'x-b3-traceid': 'b6394c8cbd783a45'
        }
        response = requests.post(url=url, headers=headers, json=data).json()
        print(response)
        return response

    def Commodity_as_a_whole_request2(self, task_id, cookie):
        url = f'https://ark.xiaohongshu.com/ark/api/v1/long_task/download_token?task_id={task_id}'
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': cookie,
            'pragma': 'no-cache',
            'referer': 'https://ark.xiaohongshu.com/ark/sale-data/download-center/downloadRecord',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'x-b3-traceid': '207507972124e8ea'
        }
        response = requests.get(url=url, headers=headers).json()
        return response

    def Commodity_as_a_whole_request3(self, url, cookie):
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        response = requests.get(url=url, headers=headers).content
        with open('11.csv', 'wb') as w:
            w.write(response)
        w.close()

    def spotlight_platform_main(self, start_day, end_day, cookie):
        # sql = 'delete from 贝德美.XHS.企业号_推广中心_计划报表 where 转化周期 < 7'
        # self._sql_server.check_message(sql, 2)
        if not start_day:
            start_day = self._sql_server.get_start_day('贝德美.XHS.企业号_推广中心_计划报表', '日期', '')
            if start_day == get_before_day(get_today()):
                print('今天数据获取完毕')
                return 0
            start_day = get_after_day(start_day)
        if not end_day:
            end_day = get_before_day(get_today())
        while True:
            page = 1
            while True:
                response = self.spotlight_platform_request(start_day, cookie, page)
                print(response)
                datas = response['data']['list']
                if not response['data']['list']:
                    break
                for data in datas:
                    week = int((get_time_number(get_today()) - get_time_number(start_day)) / (60 * 60 * 24))
                    if week > 7:
                        week = 7
                    print(data)
                    campaignName = data['campaignName']  # 计划名称
                    campaignId = data['campaignId']  # 计划id
                    marketingTargetName = data['marketingTargetName']  # 营销目标
                    placementName = data['placementName']  # 广告类型
                    optimizeTargetName = data['optimizeTargetName']  # 推广目标
                    biddingStrategyName = data['biddingStrategyName']  # 出价方式
                    promotionTargetName = data['promotionTargetName']  # 推广标的类型
                    jumpTypeName = data['jumpTypeName']  # 创意跳转类型
                    itemId = data['itemId']  # 商品id
                    fee = data['fee']  # 消费
                    impression = data['impression']  # 展现量
                    click = data['click']  # 点击量
                    acp = data['acp']  # 平均点击成本
                    cpm = data['cpm']  # 平均千次展现费用
                    try:
                        ctr = float(data['ctr'].replace('%', '')) / 100  # 点击率
                    except:
                        ctr = None

                    like = data['like']  # 点赞
                    comment = data['comment']  # 评论
                    collect = data['collect']  # 收藏
                    follow = data['follow']  # 关注
                    share = data['share']  # 分享
                    interaction = data['interaction']  # 互动量
                    cpi = data['cpi']  # 平均互动成本
                    actionButtonClick = data['actionButtonClick']  # 行动按钮点击量
                    try:
                        actionButtonCtr = round(float(data['actionButtonCtr'].replace('%', '')) / 100, 4)  # 行动按钮点击率
                    except:
                        actionButtonCtr = None
                    screenshot = data['screenshot']  # 截图
                    picSave = data['picSave']  # 保存图片
                    shoppingCartAdd = data['shoppingCartAdd']  # 加入购物车次数
                    buyNow = data['buyNow']  # 立即购买次数
                    goodsOrder = data['goodsOrder']  # 下单订单数
                    successGoodsOrder = data['successGoodsOrder']  # 成交订单数
                    try:
                        clickOrderCvr = round(float(data['clickOrderCvr'].replace('%', '')) / 100, 4)  # 点击转化率
                    except:
                        clickOrderCvr = None
                    rgmv = data['rgmv']  # rgmv
                    roi = data['roi']  # 投入产出比
                    goodsVisit = data['goodsVisit']  # 商品访问量
                    ldyfwl = 0  # 落地页访问量
                    bdanbgl = 0  # 表单按钮曝光量
                    message = data['message']  # 私信条数
                    messageUser = data['messageUser']  # 私信人数
                    messageConsult = data['messageConsult']  # 私信咨询数
                    value = (start_day, week, '拾光宝盒（贝德美）', campaignName, campaignId, marketingTargetName, placementName,
                             optimizeTargetName, biddingStrategyName, promotionTargetName, jumpTypeName, itemId, fee,
                             impression, click, ctr, acp, cpm, like, comment, collect,
                             follow, share, interaction, cpi, actionButtonClick, actionButtonCtr, screenshot, picSave,
                             shoppingCartAdd, buyNow, goodsOrder, successGoodsOrder, clickOrderCvr, rgmv, roi,
                             goodsVisit,
                             0, 0, ldyfwl, bdanbgl, messageUser, message, messageConsult)
                    save_value = []
                    for v in value:
                        if not v:
                            v = None
                        save_value.append(v)
                    try:
                        self._sql_server.save_message('贝德美.XHS.企业号_推广中心_计划报表', [tuple(save_value)])
                    except:
                        pass
                page += 1
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)

    def spotlight_platform_request(self, start_day, cookie, page):
        url = 'https://ad.xiaohongshu.com/api/leona/rtb/data/report'
        data = '{"vSellerId":"5f0ea4f8a7b903000179140a","columns":["campaignName","campaignId","marketingTarget","placement","optimizeTarget","biddingStrategy","promotionTarget","jumpType","itemId","fee","impression","click","ctr","acp","cpm","like","comment","collect","follow","share","interaction","cpi","actionButtonClick","actionButtonCtr","screenshot","picSave","shoppingCartAdd","buyNow","goodsOrder","successGoodsOrder","clickOrderCvr","rgmv","roi","goodsVisit","leads","leadsCpl","landingPageVisit","leadsButtonImpression","validLeads","validLeadsCpl","leadsCvr","messageUser","message","messageConsult","wordAvgLocation","wordImpressionRankFirst","wordImpressionRateFirst","wordImpressionRankThird","wordImpressionRateThird","wordClickRankFirst","wordClickRateFirst","wordClickRankThird","wordClickRateThird"],"splitColumns":["marketingTarget","placement","optimizeTarget","biddingStrategy","promotionTarget","jumpType","itemId"],"needTotal":true,"needList":true,"needSize":true,"timeUnit":"DAY","pageSize":10,"pageNum":' + str(
            page) + ',"sorts":[],"reportType":"CAMPAIGN","startDate":"' + start_day + '","endDate":"' + start_day + '","filters":[]}'
        with open(r'F:\lqlf\日常程序\plug_in_unit\new_x-t.js', 'r') as f:
            b = f.read()
        msg = '/api/leona/rtb/data/report'
        infos = execjs.compile(b).call('sign', msg, data)
        print(infos)
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-length': '560',
            'content-type': 'application/json;charset=UTF-8',
            'cookie': cookie,
            'origin': 'https://ad.xiaohongshu.com',
            'pragma': 'no-cache',
            'referer': 'https://ad.xiaohongshu.com/aurora/ad/datareports-basic/campaign',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            # 'x-b3-traceid': "f0bc6e2dde913c4b",
            # 'x-t': '1653643509278',
            'x-t': str(infos['X-t']),
            'x-s': infos['X-s']
            # 'x-s': "sislsB9lsY5GsgaU1g1i0jaJ1l5LOgdkOYFiZj1+02M3"
        }
        response = requests.post(url=url, headers=headers, data=data).json()
        print(response)
        return response

    def spotlight_platform_account_book_main(self, start_day, end_day, cookie):
        if not start_day:
            start_day = self._sql_server.get_start_day('贝德美.XHS.企业号_推广中心_笔记报表', '日期', '')
            if start_day == get_before_day(get_today()):
                print('今天数据获取完毕')
                return 0
            start_day = get_after_day(start_day)
        if not end_day:
            end_day = get_before_day(get_today())
        while True:
            page = 1
            while True:
                response = self.spotlight_platform_account_book_request(start_day, cookie, page)
                datas = response['data']['list']
                print(datas, 111111111111111111111111111111111111)
                if not datas:
                    break
                for data in datas:
                    week = int((get_time_number(get_today()) - get_time_number(start_day)) / (60 * 60 * 24))
                    if week > 7:
                        week = 7
                    noteId = data['noteId']  # 笔记id
                    marketingTargetName = data['marketingTargetName']  # 营销目标
                    placementName = data['placementName']  # 广告类型
                    optimizeTargetName = data['optimizeTargetName']  # 推广目标
                    # biddingStrategyName = data['biddingStrategyName']  # 出价方式
                    promotionTargetName = data['promotionTargetName']  # 推广标的类型
                    jumpTypeName = data['jumpTypeName']  # 创意跳转类型
                    itemId = data['itemId']  # 商品id
                    fee = data['fee']  # 消费
                    impression = data['impression']  # 展现量
                    click = data['click']  # 点击量
                    acp = data['acp']  # 平均点击成本
                    cpm = data['cpm']  # 平均千次展现费用
                    try:
                        ctr = float(data['ctr'].replace('%', '')) / 100  # 点击率
                    except:
                        ctr = None

                    like = data['like']  # 点赞
                    comment = data['comment']  # 评论
                    collect = data['collect']  # 收藏
                    follow = data['follow']  # 关注
                    share = data['share']  # 分享
                    interaction = data['interaction']  # 互动量
                    cpi = data['cpi']  # 平均互动成本
                    actionButtonClick = data['actionButtonClick']  # 行动按钮点击量
                    try:
                        actionButtonCtr = round(float(data['actionButtonCtr'].replace('%', '')) / 100, 4)  # 行动按钮点击率
                    except:
                        actionButtonCtr = None
                    screenshot = data['screenshot']  # 截图
                    picSave = data['picSave']  # 保存图片
                    shoppingCartAdd = data['shoppingCartAdd']  # 加入购物车次数
                    buyNow = data['buyNow']  # 立即购买次数
                    goodsOrder = data['goodsOrder']  # 下单订单数
                    successGoodsOrder = data['successGoodsOrder']  # 成交订单数
                    try:
                        clickOrderCvr = round(float(data['clickOrderCvr'].replace('%', '')) / 100, 4)  # 点击转化率
                    except:
                        clickOrderCvr = None
                    rgmv = data['rgmv']  # rgmv
                    roi = data['roi']  # 投入产出比
                    goodsVisit = data['goodsVisit']  # 商品访问量
                    ldyfwl = 0  # 落地页访问量
                    bdanbgl = 0  # 表单按钮曝光量
                    message = data['message']  # 私信条数
                    messageUser = data['messageUser']  # 私信人数
                    messageConsult = data['messageConsult']  # 私信咨询数
                    value = (start_day, 1, '拾光宝盒（贝德美）', noteId, marketingTargetName, placementName,
                             optimizeTargetName, promotionTargetName, jumpTypeName, itemId, fee,
                             impression, click, ctr, acp, cpm, like, comment, collect,
                             follow, share, interaction, cpi, actionButtonClick, actionButtonCtr, screenshot, picSave,
                             shoppingCartAdd, buyNow, goodsOrder, successGoodsOrder, clickOrderCvr, rgmv, roi,
                             goodsVisit,
                             0, 0, ldyfwl, bdanbgl, messageUser, message, messageConsult)
                    save_value = []
                    for v in value:
                        if not v:
                            v = None
                        save_value.append(v)
                    self._sql_server.save_message('贝德美.XHS.企业号_推广中心_笔记报表', [tuple(save_value)])
                page += 1
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)

    def spotlight_platform_account_book_request(self, start_day, cookie, page):
        url = 'https://ad.xiaohongshu.com/api/leona/rtb/data/report'
        # data = '{"input":{"extra":{"v_seller_id":"5f0ea4f8a7b903000179140a","columns":["marketingTarget","placement","optimizeTarget","biddingStrategy","promotionTarget","jumpType","itemId","fee","impression","click","ctr","acp","cpm","like","comment","collect","follow","share","interaction","cpi","actionButtonClick","actionButtonCtr","screenshot","picSave","shoppingCartAdd","buyNow","goodsOrder","successGoodsOrder","clickOrderCvr","rgmv","roi","goodsVisit","leads","leadsCpl","landingPageVisit","leadsButtonImpression","validLeads","validLeadsCpl","leadsCvr","messageUser","message","messageConsult"],"split_columns":["marketingTarget","placement","optimizeTarget","biddingStrategy","promotionTarget","jumpType","itemId"],"need_total":true,"need_list":true,"need_size":true,"time_unit":"DAY","page_size":200,"page_num":1,"sorts":[],"report_type":"ACCOUNT","start_date":"' + start_day + '","end_date":"' + start_day + '","filters":[]}},"task_name":"leona_ad_common_data_report_download","module_name":"leona"}'
        # data = '{"vSellerId":"5f0ea4f8a7b903000179140a","columns":["noteId","marketingTarget","placement","optimizeTarget","biddingStrategy","promotionTarget","jumpType","itemId","fee","impression","click","ctr","acp","cpm","like","comment","collect","follow","share","interaction","cpi","actionButtonClick","actionButtonCtr","screenshot","picSave","shoppingCartAdd","buyNow","goodsOrder","successGoodsOrder","clickOrderCvr","rgmv","roi","goodsVisit","leads","leadsCpl","landingPageVisit","leadsButtonImpression","validLeads","validLeadsCpl","leadsCvr","messageUser","message","messageConsult"],"splitColumns":["marketingTarget","placement","optimizeTarget","biddingStrategy","promotionTarget","jumpType","itemId"],"needTotal":true,"needList":true,"needSize":true,"timeUnit":"DAY","pageSize":100,"pageNum":' + str(
        #     page) + ',"sorts":[],"reportType":"NOTE","startDate":"' + start_day + '","endDate":"' + start_day + '","filters":[]}'
        data = '{"vSellerId":"5f0ea4f8a7b903000179140a","columns":["noteId","marketingTarget","placement","optimizeTarget","promotionTarget","jumpType","itemId","fee","impression","click","ctr","acp","cpm","like","comment","collect","follow","share","interaction","cpi","actionButtonClick","actionButtonCtr","screenshot","picSave","shoppingCartAdd","buyNow","goodsOrder","successGoodsOrder","clickOrderCvr","rgmv","roi","goodsVisit","leads","leadsCpl","landingPageVisit","leadsButtonImpression","validLeads","validLeadsCpl","leadsCvr","messageUser","message","messageConsult","wordAvgLocation","wordImpressionRankFirst","wordImpressionRateFirst","wordImpressionRankThird","wordImpressionRateThird","wordClickRankFirst","wordClickRateFirst","wordClickRankThird","wordClickRateThird"],"splitColumns":["marketingTarget","placement","optimizeTarget","promotionTarget","jumpType","itemId"],"needTotal":true,"needList":true,"needSize":true,"timeUnit":"DAY","pageSize":20,"pageNum":' + str(
            page) + ',"sorts":[],"reportType":"NOTE","startDate":"' + start_day + '","endDate":"' + start_day + '","filters":[]}'
        with open(r'F:\lqlf\日常程序\plug_in_unit\x-t.js', 'r') as f:
            b = f.read()
        msg = '/api/leona/rtb/data/report'
        infos = execjs.compile(b).call('get_info', msg, data)
        print(infos)
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-length': '884',
            'content-type': 'application/json;charset=UTF-8',
            'cookie': cookie,
            'origin': 'https://ad.xiaohongshu.com',
            'pragma': 'no-cache',
            'referer': 'https://ad.xiaohongshu.com/aurora/ad/datareports-basic/note',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'x-b3-traceid': infos[2],
            'x-s': infos[0],
            'x-t': str(infos[1])
        }
        response = requests.post(url=url, headers=headers, data=data).json()
        print(response)
        return response

    def promotion_center_unit_report_main(self, start_day, end_day, cookie):
        if not start_day:
            start_day = self._sql_server.get_start_day('贝德美.XHS.企业号_推广中心_单元报表', '日期', '')
            if start_day == get_before_day(get_today()):
                print('今天数据获取完毕')
                return 0
            start_day = get_after_day(start_day)
        if not end_day:
            end_day = get_before_day(get_today())
        while True:
            self.promotion_center_unit_report_request(start_day, cookie, '单元')
            with open(r'C:\Users\lianqinglongfei\Desktop\DyItemSpider\小红书\单元.csv', 'r', encoding='utf8') as f:
                reader = csv.reader(f)
                for row in reader:
                    row = row[:-9]
                    if '时间' in row[0] or '合计' in row[0]:
                        continue
                    week = int((get_time_number(get_today()) - get_time_number(row[0])) / (60 * 60 * 24))
                    if week > 7:
                        week = 7
                    row.insert(1, str(week))
                    row.insert(2, '拾光宝盒（贝德美）')
                    value = []
                    for val in row:
                        if '%' in val:
                            try:
                                val = float(val.replace('%', ''))/100
                            except:
                                val = 0
                        value.append(val)
                    print(value)
                    self._sql_server.save_message('贝德美.XHS.企业号_推广中心_单元报表', [tuple(value)])
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)
            time.sleep(2)

    def promotion_center_unit_report_request(self, start_day, cookie, data_type):
        url = 'https://ad.xiaohongshu.com/api/leona/longTask/download/commit_task'
        if data_type == '单元':
            data = '{"input":{"extra":{"v_seller_id":"5f0ea4f8a7b903000179140a","columns":["unitName","unitId","marketingTarget","buildType","placement","optimizeTarget","biddingStrategy","promotionTarget","jumpType","itemId","campaignName","campaignId","fee","impression","click","ctr","acp","cpm","like","comment","collect","follow","share","interaction","cpi","actionButtonClick","actionButtonCtr","screenshot","picSave","shoppingCartAdd","buyNow","goodsOrder","successGoodsOrder","clickOrderCvr","rgmv","roi","goodsVisit","leads","leadsCpl","landingPageVisit","leadsButtonImpression","validLeads","validLeadsCpl","leadsCvr","messageUser","message","messageConsult","wordAvgLocation","wordImpressionRankFirst","wordImpressionRateFirst","wordImpressionRankThird","wordImpressionRateThird","wordClickRankFirst","wordClickRateFirst","wordClickRankThird","wordClickRateThird"],"split_columns":["marketingTarget","buildType","placement","optimizeTarget","biddingStrategy","promotionTarget","jumpType","itemId"],"need_total":true,"need_list":true,"need_size":true,"time_unit":"DAY","page_size":20,"page_num":1,"sorts":[],"report_type":"UNIT","start_date":"' + start_day + '","end_date":"' + start_day + '","filters":[]}},"task_name":"leona_ad_common_data_report_download","module_name":"leona"}'
        else:
            data = '{"input":{"extra":{"v_seller_id":"5f0ea4f8a7b903000179140a","columns":["creativityImage","creativityName","creativityId","noteId","unitName","unitId","campaignName","campaignId","fee","impression","click","ctr","acp","cpm","like","comment","collect","follow","share","interaction","cpi","actionButtonClick","actionButtonCtr","screenshot","picSave","shoppingCartAdd","buyNow","goodsOrder","successGoodsOrder","clickOrderCvr","rgmv","roi","goodsVisit","leads","leadsCpl","landingPageVisit","leadsButtonImpression","validLeads","validLeadsCpl","leadsCvr","messageUser","message","messageConsult","wordAvgLocation","wordImpressionRankFirst","wordImpressionRateFirst","wordImpressionRankThird","wordImpressionRateThird","wordClickRankFirst","wordClickRateFirst","wordClickRankThird","wordClickRateThird"],"split_columns":[],"need_total":true,"need_list":true,"need_size":true,"time_unit":"DAY","page_size":20,"page_num":1,"sorts":[],"report_type":"CREATIVITY","start_date":"' + start_day + '","end_date":"' + start_day + '","filters":[]}},"task_name":"leona_ad_common_data_report_download","module_name":"leona"}'
        with open(r'F:\lqlf\日常程序\plug_in_unit\x-t.js', 'r') as f:
            b = f.read()
        msg = '/api/leona/longTask/download/commit_task'
        infos = execjs.compile(b).call('get_info', msg, data)
        print(infos)
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-length': '576',
            'content-type': 'application/json;charset=UTF-8',
            'cookie': cookie,
            'origin': 'https://ad.xiaohongshu.com',
            'pragma': 'no-cache',
            'referer': 'https://ad.xiaohongshu.com/aurora/ad/datareports-basic/unit',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'x-b3-traceid': infos[2],
            'x-s': infos[0],
            'x-t': str(infos[1])
        }
        response = requests.post(url=url, headers=headers, data=data).json()
        task_id = response['data']['task_id']
        print(task_id)
        while True:
            response1 = self.get_unit_report_status(cookie, task_id)
            print(response1)
            try:
                url = response1['data']['result']['file_url']
                break
            except:
                time.sleep(3)
        self.get_unit_report_excel(url, data_type)
        return response

    def get_unit_report_status(self, cookie, task_id):
        url = f'https://ad.xiaohongshu.com/api/leona/longTask/download/task/result?task_id={task_id}'
        with open(r'F:\lqlf\日常程序\plug_in_unit\x-t.js', 'r') as f:
            b = f.read()
        msg = '/api/leona/longTask/download/task/result'
        infos = execjs.compile(b).call('get_info', msg)
        print(infos)
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': cookie,
            'pragma': 'no-cache',
            'referer': 'https://ad.xiaohongshu.com/aurora/ad/datareports-basic/unit',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'x-b3-traceid': infos[2],
            'x-s': infos[0],
            'x-t': str(infos[1])
        }
        response = requests.get(url=url, headers=headers).json()
        return response

    def get_unit_report_excel(self, url, data_type):
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'origin': 'https://ad.xiaohongshu.com',
            'pragma': 'no-cache',
            'referer': 'https://ad.xiaohongshu.com/',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        response = requests.get(url=url, headers=headers).content
        with open(f'{data_type}.csv', 'wb')as w:
            w.write(response)
        w.close()

    def promotion_center_report_request(self, start_day, cookie, page):
        url = 'https://ad.xiaohongshu.com/api/leona/rtb/data/report'
        data = '{"vSellerId":"5f0ea4f8a7b903000179140a","columns":["creativityImage","creativityName","creativityId","marketingTarget","buildType","placement","optimizeTarget","biddingStrategy","promotionTarget","jumpType","itemId","noteId","unitName","unitId","campaignName","campaignId","fee","impression","click","ctr","acp","cpm","like","comment","collect","follow","share","interaction","cpi","actionButtonClick","actionButtonCtr","screenshot","picSave","shoppingCartAdd","buyNow","goodsOrder","successGoodsOrder","clickOrderCvr","rgmv","roi","goodsVisit","leads","leadsCpl","landingPageVisit","leadsButtonImpression","validLeads","validLeadsCpl","leadsCvr","messageUser","message","messageConsult","wordAvgLocation","wordImpressionRankFirst","wordImpressionRateFirst","wordImpressionRankThird","wordImpressionRateThird","wordClickRankFirst","wordClickRateFirst","wordClickRankThird","wordClickRateThird"],"splitColumns":["marketingTarget","buildType","placement","optimizeTarget","biddingStrategy","promotionTarget","jumpType","itemId"],"needTotal":true,"needList":true,"needSize":true,"timeUnit":"DAY","pageSize":20,"pageNum":' + str(
            page) + ',"sorts":[],"reportType":"CREATIVITY","startDate":"' + start_day + '","endDate":"' + start_day + '","filters":[]}'
        with open(r'F:\lqlf\日常程序\plug_in_unit\x-t.js', 'r') as f:
            b = f.read()
        msg = '/api/leona/rtb/data/report'
        infos = execjs.compile(b).call('get_info', msg, data)
        print(infos)
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-length': '576',
            'content-type': 'application/json;charset=UTF-8',
            'cookie': cookie,
            'origin': 'https://ad.xiaohongshu.com',
            'pragma': 'no-cache',
            'referer': 'https://ad.xiaohongshu.com/aurora/ad/datareports-basic/unit',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'x-b3-traceid': infos[2],
            'x-s': infos[0],
            'x-t': str(infos[1])
        }
        response = requests.post(url=url, headers=headers, data=data).json()
        print(response)
        return response

    def promotion_center_creative_report_main(self, start_day, end_day, cookie):
        if not start_day:
            start_day = self._sql_server.get_start_day('贝德美.XHS.企业号_推广中心_创意报表', '日期', '')
            if start_day == get_before_day(get_today()):
                print('今天数据获取完毕')
                return 0
            start_day = get_after_day(start_day)
        if not end_day:
            end_day = get_before_day(get_today())
        while True:
            page = 1
            xhs_values = []
            while 1:
                response = self.promotion_center_report_request(start_day, cookie, page)
                datas = response['data']['list']
                if not response['data']['list']:
                    break
                for data in datas:
                    week = int((get_time_number(get_today()) - get_time_number(start_day)) / (60 * 60 * 24))
                    if week > 7:
                        week = 7
                    print(data)
                    creativityName = data['creativityName']  # 创意名称
                    creativityId = data['creativityId']  # 创意名称
                    unitName = data['campaignName']  # 单元名称
                    unitId = data['campaignId']  # 单元id
                    marketingTargetName = data['marketingTargetName']  # 营销诉求
                    buildTypeName = data['buildTypeName']  # 搭建方式
                    placementName = data['placementName']  # 广告类型
                    optimizeTargetName = data['optimizeTargetName']  # 推广目标
                    biddingStrategyName = data['biddingStrategyName']  # 出价方式
                    promotionTargetName = data['promotionTargetName']  # 推广标的类型
                    jumpTypeName = data['jumpTypeName']  # 创意跳转类型
                    itemId = data['itemId']  # 商品id
                    noteId = data['noteId']  # 笔记id
                    campaignName = data['unitName']  # 计划名称
                    campaignId = data['unitId']  # 计划id
                    fee = data['fee']  # 消费
                    impression = data['impression']  # 展现量
                    click = data['click']  # 点击量
                    acp = data['acp']  # 平均点击成本
                    cpm = data['cpm']  # 平均千次展现费用
                    try:
                        ctr = float(data['ctr'].replace('%', '')) / 100  # 点击率
                    except:
                        ctr = None

                    like = data['like']  # 点赞
                    comment = data['comment']  # 评论
                    collect = data['collect']  # 收藏
                    follow = data['follow']  # 关注
                    share = data['share']  # 分享
                    interaction = data['interaction']  # 互动量
                    cpi = data['cpi']  # 平均互动成本
                    actionButtonClick = data['actionButtonClick']  # 行动按钮点击量
                    try:
                        actionButtonCtr = round(float(data['actionButtonCtr'].replace('%', '')) / 100, 4)  # 行动按钮点击率
                    except:
                        actionButtonCtr = None
                    screenshot = data['screenshot']  # 截图
                    picSave = data['picSave']  # 保存图片
                    shoppingCartAdd = data['shoppingCartAdd']  # 加入购物车次数
                    buyNow = data['buyNow']  # 立即购买次数
                    goodsOrder = data['goodsOrder']  # 下单订单数
                    successGoodsOrder = data['successGoodsOrder']  # 成交订单数
                    try:
                        clickOrderCvr = round(float(data['clickOrderCvr'].replace('%', '')) / 100, 4)  # 点击转化率
                    except:
                        clickOrderCvr = None
                    rgmv = data['rgmv']  # rgmv
                    roi = data['roi']  # 投入产出比
                    goodsVisit = data['goodsVisit']  # 商品访问量

                    ldyfwl = 0  # 落地页访问量
                    bdanbgl = 0  # 表单按钮曝光量
                    message = data['message']  # 私信条数
                    messageUser = data['messageUser']  # 私信人数
                    messageConsult = data['messageConsult']  # 私信咨询数
                    value = (
                        start_day, week, '拾光宝盒（贝德美）', creativityName, creativityId, marketingTargetName, buildTypeName,
                        placementName, optimizeTargetName, biddingStrategyName, promotionTargetName, jumpTypeName,
                        itemId, noteId, campaignName, campaignId, unitName, unitId, fee, impression, click, ctr, acp, cpm,
                        like, comment, collect,
                        follow, share, interaction, cpi, actionButtonClick, actionButtonCtr, screenshot, picSave,
                        shoppingCartAdd, buyNow, goodsOrder, successGoodsOrder, clickOrderCvr, rgmv, roi,
                        goodsVisit, 0, 0, ldyfwl, bdanbgl, 0, 0, 0, message, messageUser, messageConsult)
                    save_value = []
                    for v in value:
                        if not v:
                            v = None
                        save_value.append(v)
                    xhs_values.append(tuple(save_value))
                    self.check_xhs_id(noteId)
                page += 1
            try:
                self._sql_server.save_message('贝德美.XHS.企业号_推广中心_创意报表', xhs_values)
            except:
                pass
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)
            time.sleep(2)


    def check_xhs_id(self, xhs_id):
        if xhs_id:
            sql = f"select * from 贝德美.XHS.企业号_笔记基本信息 where 笔记ID='{xhs_id}'"
            res = self._sql_server.check_message(sql, 0)
            print(res)
            if not res:
                url = f'https://www.xiaohongshu.com/discovery/item/{xhs_id}'
                headers = {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'accept-language': 'zh-CN,zh;q=0.9',
                    'cache-control': 'no-cache',
                    'cookie': 'xhsTrackerId=2d0b6641-7fde-4445-c498-6289fae63430; timestamp2=16617520098012315f299566efc87f4223bcdf76d989aa80a795d2647313759; timestamp2.sig=hpND3mdUQoGZXvG01jIEu-e6BBNwJpxv8LtP12orotg; a1=182e823673dz40hj7b4224ts276qm9x7kjuz6us1500000385222; smidV2=20220829134650a64efa08cc33751942556788610ea3ed006ead04379f23780; gid=yYJdYJqKY2TKyYJdYJqKWV7Mqfu48xVWD4JJ7y249MJWKu88A6jCWK888qY2JJJ8fJY4fdfj; gid.sig=OxnepXSMBXiE73QuvoFy8o3zI1T4ukJ8Oh_2FBrNRqc; gid.sign=WjTCyOvbqKg6VQN8GEd3UO3cXaA=; gid.sign.sig=X1SYMqidHFCbYOdN9GsX4NaiG_AorCPBZQmXMTnRkic; extra_exp_ids=wx_engage_bar_exp,wx_launch_open_app_duration_origin,wx_launch_open_app_decrement_v2_exp,wx_launch_open_app_decrement_clt,wx_launch_open_app_duration_origin,recommend_comment_hide_exp2,recommend_comment_hide_v2_clt,recommend_comment_hide_v3_origin,supervision_exp,supervision_v2_exp,commentshow_clt1,gif_clt1,ques_clt2',
                    'pragma': 'no-cache',
                    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': 'Windows',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'none',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
                }
                response = requests.get(url=url, headers=headers).text
                title = response.split('"name": "')[1].split('",')[0]
                date = response.split('发布于 ')[1].split('<')[0].split(' ')[0]
                name = response.split('"author"')[1].split('"name": "')[1].split('",')[0]
                values = (date, xhs_id, title, name, None, None, None)
                self._sql_server.save_message('贝德美.XHS.企业号_笔记基本信息', [values])

    def promotion_center_creative_report_request(self, start_day, cookie, page):
        url = 'https://ad.xiaohongshu.com/api/leona/rtb/data/report'
        data = '{"vSellerId":"5f0ea4f8a7b903000179140a","columns":["creativityImage","creativityName","creativityId","marketingTarget","buildType","placement","optimizeTarget","biddingStrategy","promotionTarget","jumpType","itemId","noteId","unitName","unitId","campaignName","campaignId","fee","impression","click","ctr","acp","cpm","like","comment","collect","follow","share","interaction","cpi","actionButtonClick","actionButtonCtr","screenshot","picSave","shoppingCartAdd","buyNow","goodsOrder","successGoodsOrder","clickOrderCvr","rgmv","roi","goodsVisit","leads","leadsCpl","landingPageVisit","leadsButtonImpression","validLeads","validLeadsCpl","leadsCvr","messageUser","message","messageConsult","wordAvgLocation","wordImpressionRankFirst","wordImpressionRateFirst","wordImpressionRankThird","wordImpressionRateThird","wordClickRankFirst","wordClickRateFirst","wordClickRankThird","wordClickRateThird"],"splitColumns":["marketingTarget","buildType","placement","optimizeTarget","biddingStrategy","promotionTarget","jumpType","itemId"],"needTotal":true,"needList":true,"needSize":true,"timeUnit":"DAY","pageSize":20,"pageNum":' + str(
            page) + ',"sorts":[],"reportType":"CREATIVITY","startDate":"' + start_day + '","endDate":"' + start_day + '","filters":[]}'
        with open(r'C:\Users\lianqinglongfei\Desktop\DyItemSpider\小红书\x-t.js', 'r') as f:
            b = f.read()
        msg = '/api/leona/rtb/data/report'
        infos = execjs.compile(b).call('get_info', msg, data)
        print(infos)
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-length': '576',
            'content-type': 'application/json;charset=UTF-8',
            'cookie': cookie,
            'origin': 'https://ad.xiaohongshu.com',
            'pragma': 'no-cache',
            'referer': 'https://ad.xiaohongshu.com/aurora/ad/datareports-basic/unit',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'x-b3-traceid': infos[2],
            'x-s': infos[0],
            'x-t': str(infos[1])
        }
        response = requests.post(url=url, headers=headers, data=data).json()
        print(response)
        return response


if __name__ == '__main__':
    chrome = ChromeOption()
    xhs = LittleRedBook()
    # #
    # 小红书后台cookie
    xhs_cookie = chrome.xhs_login()
    # # # # 贝德美.XHS.商品效果_日
    xhs.commodity_as_a_whole_main('', '', xhs_cookie)
    # # # # 贝德美.XHS.店铺整体_日
    xhs.overall_store_day_main('', '', xhs_cookie)
    chrome.__del__()
    time.sleep(3)
    # #
    chrome = ChromeOption()
    # # 小红书蒲公英cookie
    xhs_cookie = chrome.xhsjg_login()
    # 贝德美.XHS.企业号_推广中心_计划报表
    xhs.spotlight_platform_main('', '', xhs_cookie)
    # 贝德美.XHS.企业号_推广中心_笔记报表
    xhs.spotlight_platform_account_book_main('', '', xhs_cookie)
    # # # # 贝德美.XHS.企业号_推广中心_单元报表
    xhs.promotion_center_unit_report_main('', '', xhs_cookie)
    # # # # # 贝德美.XHS.企业号_推广中心_创意报表
    xhs.promotion_center_creative_report_main('', '', xhs_cookie)
    # xhs.check_xhs_id('62ea4dd30000000012004b3a')