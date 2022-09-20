import requests,json,time,csv
from CurrencyModule import *
from Setting import *


class TBK:
    def __init__(self):
        self.ssc = SqlServerConnect()

    # 淘宝客_效果报表_订单结算
    def taobao_guest_effect_report_order_settlement(self, start_day, cookie):
        positionIndex = ''
        p = 1
        jumpType = 0
        info = {}
        check_word = {}
        while True:
            url = 'https://ad.alimama.com/report/tkTrans.json?t=1596079312185&_tb_token_=f5763b9b68be7'
            headers= {
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9',
                'content-length': '144',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'cookie': cookie,
                'origin': 'https://ad.alimama.com',
                'referer': 'https://ad.alimama.com/report/overview/orders.htm?startTime=2020-07-29&endTime=2020-07-29&pageNo=1&jumpType=-1&positionIndex=1596027196_1mhuHuuWUDZ2%7C1596031726_InAI9NiyYL2',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3765.400 QQBrowser/10.6.4153.400',
                'x-requested-with': 'XMLHttpRequest',
            }
            data = {
                'pageNo': p,
                'pageSize': 40,
                'startTime': start_day,
                'endTime': start_day,
                'status': '3',
                'positionIndex': positionIndex,
                'jumpType': jumpType,
            }
            res = requests.post(url,headers=headers,data=data)
            print(res.text)
            if json.loads(res.text)['data']['result'] == []:
                break
            positionIndex = json.loads(res.text)['data']['positionIndex']
            for i in json.loads(res.text)['data']['result']:
                tbTradeFinishTime = i['tbTradeFinishTime']  # 确认收货时间
                earningTime = i['earningTime']  # 账户支出时间
                tkEarningTime = i['tkEarningTime']  # 淘客结算时间
                if tkEarningTime not in info:
                    info[tkEarningTime] = []
                tbTradeCreateTime = i['tbTradeCreateTime']  # 创建时间
                campaignName = i['campaignName']  # 计划名称
                itemId = i['itemId']  # 商品ID
                tbAuctionTitle = i['tbAuctionTitle']  # 商品名称
                tbFinishTotalPrice = i['tbFinishTotalPrice']  # 实际成交价格
                tbAuctionNum = i['tbAuctionNum']  # 成交商品数
                fmtCommissionRate = float(i['fmtCommissionRate'].replace('%',''))/100  # 佣金比例
                fmtCommissionFee = i['fmtCommissionFee']  # 佣金
                serviceRate = i['serviceRate']/100 if i['serviceRate'] != None else None  # 服务费率
                serviceFee = i['serviceFee']  # 服务费金额
                tbTradeParentId = i['tbTradeParentId']  # 淘宝父订单编号
                tbTradeId = i['tbTradeId']  # 淘宝子订单编号
                nickname = i['nickname']  # 来源或淘客昵称
                tkCpPubName = i['tkCpPubName']  # 团长名称
                campaignId = i['campaignId']  # 计划ID
                pid = i['tkPubId']
                tup1 = (tbTradeFinishTime, earningTime, tkEarningTime, tbTradeCreateTime, campaignName, itemId, tbAuctionTitle, tbFinishTotalPrice, tbAuctionNum, fmtCommissionRate, fmtCommissionFee, serviceRate, serviceFee, tbTradeParentId, tbTradeId, nickname, tkCpPubName, campaignId, pid)
                info[tkEarningTime].append(tup1)
                if tkEarningTime not in check_word:
                    check_word[tkEarningTime] = 0
                check_word[tkEarningTime] += float(fmtCommissionFee)
                check_word[tkEarningTime] += float(serviceFee)
            p += 1
            jumpType = 1

        for cw in check_word:
            cm = self.check_msg(cw, cw, cookie)
            if abs(cm - check_word[cw]) < 5:
                self.ssc.save_message('贝德美.dbo.淘宝客_效果报表_订单结算', info[cw])



    def check_msg(self, start_day, end_day, cookie):
        url = 'https://ad.alimama.com/account/incomeDetail.json?t=1660280665923&_tb_token_=773875e5e31fb'
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-length': '60',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': cookie,
            'origin': 'https://ad.alimama.com',
            'referer': 'https://ad.alimama.com/user/account/detail.htm?spm=a21an.26925784.portalLayoutHeader._user_account_detail.617061db5x2k8l&startTime=2022-08-11&endTime=2022-08-11',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        data = {
            'pageNo': '1',
            'pageSize': '40',
            'startTime': start_day,
            'endTime': end_day,
        }
        response = requests.post(url=url, headers=headers, data=data).json()
        deductAmount = response['data']['result'][0]['deductAmount']
        return deductAmount


if __name__ == '__main__':
    tbk = TBK()
    cookie = 't=6711df92ba85c36afe639a438682e232; cna=nWYbGpuKHDsCAXkEs3F2iXa2; new-entrance-guide=true; cookie2=1bedca6edac0b7e0bf7cdbdc2502e1f1; v=0; _tb_token_=773875e5e31fb; alimamapwag=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEwMy4wLjAuMCBTYWZhcmkvNTM3LjM2; cookie32=303ec5c4dd8647c00cb35935f52fef4b; alimamapw=QCYCQXMGEXUEHHACQXEAEHtWQCcFQXRxEXV1HHICQXAGEH0nbFQGAAUEVQAGCVEFUwsBVl5WBlcE%0AVwJQBQAAXwcBAFdR; cookie31=Mzk4MzcwMDU1LCVFOCVCNCU5RCVFNSVCRSVCNyVFNyVCRSU4RSVFNiU5NyU5NyVFOCU4OCVCMCVFNSVCQSU5Nyxib2Rvcm1lQGNvc2Vhc3QuY29tLFRC; taokeisb2c=; taokeIsBoutiqueSeller=eQ%3D%3D; xlly_s=1; rurl=aHR0cDovL2FkLmFsaW1hbWEuY29tL3VzZXIvYWNjb3VudC9kZXRhaWwuaHRtP3NwbT1hMjFhbi4yNjkyNTc4NC5wb3J0YWxMYXlvdXRIZWFkZXIuX3VzZXJfYWNjb3VudF9kZXRhaWwuNjE3MDYxZGI1eDJrOGwmc3RhcnRUaW1lPTIwMjItMDgtMTEmZW5kVGltZT0yMDIyLTA4LTEx; login=VT5L2FSpMGV7TQ%3D%3D; tfstk=cZdCBVjobkqQ4Mm1b9gZUsT8wi5fZp4fPvsHRcvR2wBtggLCiKPVcPrkEuCPyN1..; l=eBL6dPl4gpC2g8L8BOfwourza77OSIRAguPzaNbMiOCPOD595eadW6YSbLLpC3GVh6V9R3Wrj_IwBeYBqIDKB0hjbFXWeLHmn; isg=BGlpTJR_L23ogxC_-6-ZmBepeBXDNl1oLJfydQte5dCP0onkU4ZtOFfElHZkyvWg'
    start_day = '2022-09-01'  # 结算时间
    while True:
        tbk.taobao_guest_effect_report_order_settlement(start_day, cookie)
        start_day = get_after_day(start_day)
        if start_day == '2022-09-15':
            break