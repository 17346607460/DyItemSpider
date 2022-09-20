from Setting import *
from CurrencyModule import *
import requests

class VipShop:
    def __init__(self):
        self.sql_server = SqlServerConnect()

    def transaction_analysis_main(self, start_day, end_day, cookie):
        while True:
            if not start_day:
                start_day = self.sql_server.get_start_day('贝德美.WPH.交易概况_日', '日期', '')
                if start_day == get_before_day(get_today()):
                    return 0
                start_day = get_after_day(start_day)
            if not end_day:
                end_day = get_before_day(get_today())
            response = self.transaction_analysis_request(cookie, start_day)
            datas = response['data']
            if not datas:
                break
            impressionFlow = datas['impressionFlow']  # 曝光流量
            pageMerDetailFlow = datas['pageMerDetailFlow']  # 浏览流量
            uv = datas['uv']  # 商详uv
            valueOfUv = datas['valueOfUv']  # uv价值
            addUserNum = datas['addUserNum']  # 加购人数
            merchandiseLikeUserNum = datas['merchandiseLikeUserNum']  # 收藏人数
            goodsActureAmt = datas['goodsActureAmt']  # 销售额
            goodsActureNum = datas['goodsActureNum']  # 销售量
            userNum = datas['userNum']  # 客户数
            childrenOrderNum = datas['childrenOrderNum']  # 子订单数
            userUnitPrice = datas['userUnitPrice']  # 客单价
            cartConvRate = round(datas['cartConvRate'] / 100, 4)  # 访问-加购转化率
            pageMerDetailConvRate = round(datas['pageMerDetailConvRate'] / 100, 4)  # 购买转化率
            payConvRate = round(datas['payConvRate'] / 100, 4)  # 加购-支付转化率
            value = [
                start_day, impressionFlow, pageMerDetailFlow, uv, valueOfUv, addUserNum, merchandiseLikeUserNum,
                cartConvRate,
                goodsActureAmt, goodsActureNum, userNum, childrenOrderNum, userUnitPrice, payConvRate,
                pageMerDetailConvRate]
            exit_info = self.exit_goods_info(cookie, start_day)
            value = value + exit_info
            self.sql_server.save_message('贝德美.WPH.交易概况_日', [tuple(value)])
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)
            time.sleep(3)

    def transaction_analysis_request(self, cookie, start_day):
        url = 'https://compass.vip.com/operate/sales/queryOverview'
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-length': '73',
            'content-type': 'application/json',
            'cookie': cookie,
            'origin': 'https://compass.vip.com',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        data = {"brandStoreSn": "all", "dtType": 0, "startDt": start_day.replace('-', ''),
                "endDt": start_day.replace('-', '')}
        response = requests.post(url=url, headers=headers, json=data)
        print(response.text)
        return response.json()

    def exit_goods_info(self, cookie, start_day):
        url = 'https://compass.vip.com/operate/afterSales/queryOverview'
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-length': '93',
            'content-type': 'application/json',
            'cookie': cookie,
            'origin': 'https://compass.vip.com',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
        }
        data = {"dtType":0,"startDt":f"{start_day.replace('-', '')}","endDt":f"{start_day.replace('-', '')}","brandStoreSn":"all","thirdCateIdSet":[]}
        response = requests.post(url=url, headers=headers, json=data).json()
        datas = response['data']
        goodsActureAmt = datas['goodsActureAmt']  # 销售额
        goodsActureNum = datas['goodsActureNum']  # 销售量
        rejectGoodsAmt = datas['rejectGoodsAmt']  # 拒收金额
        rejectItemNum = datas['rejectItemNum']  # 拒收件数
        rejectItemRate = datas['rejectItemRate']  # 拒收率
        returnGoodsAmt = datas['returnGoodsAmt']  # 退货金额
        returnItemNum = datas['returnItemNum']  # 退货件数
        returnItemRate = datas['returnItemRate']  # 退货率
        exchangeGoodsAmt = datas['exchangeGoodsAmt']  # 换货金额
        exchangeItemNum = datas['exchangeItemNum']  # 换货件数
        exchangeItemRate = datas['exchangeItemRate']  # 换货率
        rejectReturnGoodsAmt = datas['rejectReturnGoodsAmt']  # 据退金额
        rejectReturnItemNum = datas['rejectReturnItemNum']  # 拒退件数
        rejectReturnItemRate = datas['rejectReturnItemRate']  # 拒退率
        exit_info = [returnItemNum, returnGoodsAmt, returnItemRate, rejectItemNum, rejectGoodsAmt, rejectItemRate, rejectReturnItemNum, rejectReturnGoodsAmt, rejectReturnItemRate, exchangeItemNum, exchangeGoodsAmt, exchangeItemRate]
        return exit_info

    def talent_selling_goods_main(self, start_day, end_day, cookie):
        # https://e.vip.com/main.html#/
        while True:
            if not start_day:
                start_day = self.sql_server.get_start_day('贝德美.WPH.推广计划_达人卖货', '日期', '')
                if start_day == get_before_day(get_today()):
                    return 0
                start_day = get_after_day(start_day)
            if not end_day:
                end_day = get_before_day(get_today())
            response = self.talent_selling_goods_request(start_day, cookie)
            datas = response['data']['campaigns']
            for data in datas:
                v_id = data['id']  # id
                title = data['title']  # 计划名称
                startDate = data['startDate']  # 开始日期
                endDate = data['endDate']  # 结束日期
                startDate = get_number_day(int(startDate / 1000))
                endDate = get_number_day(int(endDate / 1000))
                contentId = data['wxkCampaignContents'][0]['contentId']
                commissionRate = data['commissionRate']  # 推广费比例
                goodsCost = int(data['statistics']['goodsCost']) / 100  # 推广费
                ordersIn24Hour = data['statistics']['ordersIn24Hour']  # 推广费订单
                salesIn24Hour = int(data['statistics']['salesIn24Hour']) / 100  # 销售额
                roiIn24Hour = data['statistics']['roiIn24Hour']  # 预估roi
                status = data['status']  # 推广中
                if status == 1:
                    info = '推广中'
                value = [start_day, v_id, title, f"{startDate}至{endDate}", contentId, None, None, info, commissionRate,
                         goodsCost, ordersIn24Hour, salesIn24Hour, roiIn24Hour]
                self.sql_server.save_message('贝德美.WPH.推广计划_达人卖货', [tuple(value)])
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)
            time.sleep(3)

    def talent_selling_goods_request(self, start_day, cookie):
        url = 'https://e.vip.com/wxk/campaigns'
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'advid': 'Civn4Z7P',
            'cache-control': 'no-cache',
            'cookie': cookie,
            'pragma': 'no-cache',
            'referer': 'https://e.vip.com/main.html',
            'requestid': '21a81210-a95b-43c0-a78d-0d59de8267ec',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        params = {
            'sd': str(get_time_number(start_day)) + '000',
            'ed': str(get_time_number(start_day)) + '000',
            'pi': '1',
            'pc': '20',
            'st': '3,2,5,6,4',
            'advid': '',
            'psd': '1658592000000',
            'ped': '1663862400000'
        }
        response = requests.get(url=url, headers=headers, params=params).json()
        return response


if __name__ == '__main__':
    vs = VipShop()
    start_day = ''
    end_day = ''
    cookie = 'PHPSESSID=a30lpvlba9dltri48irmtl6ff4; mars_pid=0; mars_sid=5671f938bcfa2104463a3f7178dc0b2d; vc_token=eyJ0b2tlbiI6IjlmZTc4YThhZTM3YTI0ZmIxNTcxYzUzNWQwNzFjZjU0IiwidG9rZW4xIjoiMzY0Y2Q1NDg3ZGVlM2MyM2VmZmU0YzVlMmY3YWYxY2EiLCJ2ZW5kb3JJZCI6IjQxNjkwIiwidXNlck5hbWUiOiIzNzE4MDY4NTRAcXEuY29tIiwidmVuZG9yQ29kZSI6IjYzNjQwNSIsInVzZXJJZCI6IjE1ODk5NCIsInZpc1Nlc3Npb25JZCI6ImEzMGxwdmxiYTlkbHRyaTQ4aXJtdGw2ZmY0IiwiYXBwTmFtZSI6InZpc1BDIiwidmlzaXRGcm9tIjoidmMifQ%3D%3D; visit_id=D9A4E5A43071E4FD626520FF93A1525B; mars_cid=1663038961991_98f75bd8bfe1b193bed9c1a8453651ed'
    vs.transaction_analysis_main(start_day, end_day, cookie)
    cookie = 'mars_pid=0; mars_sid=71178f999f35234ac22ac1f3e867d3cb; vip_tracker_source_from=; VipRUID=464359927; VipUID=0b3be767cafb06bafa093eba6c6486f8; VipRNAME=%E5%AD%90%E5%8D%A0; VipDegree=D1; visit_id=D505F2F7FDD1B1D352C65ED9C7663901; vipshop_passport_src=https%3A%2F%2Fe.vip.com%2Fmain.html; _jzqco=%7C%7C%7C%7C%7C1.601959504.1663039051066.1663557423317.1663640808164.1663557423317.1663640808164.0.0.0.6.6; pg_session_no=6; PASSPORT_ACCESS_TOKEN=4BAF2201117B2BDB5F5BDA1C4DC66D9DC5419862; VipLID=0%7C1663640816%7Ca5c346; user_class=c; JSESSIONID=D9002B8170FF2D19F181CC3512EA30C9-s1; mars_cid=1663039051036_cd26ac3cccf83c40d11433a016c30a0a'
    vs.talent_selling_goods_main('', '', cookie)