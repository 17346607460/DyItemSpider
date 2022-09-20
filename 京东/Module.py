import time

import requests
import random
import logging
# import pyautogui
from Setting import *
from CurrencyModule import *
from auto_login import *

# pyautogui.FAILSAFE = False


class JD:
    def __init__(self):
        self.citys_sheng = ['北京', '上海', '天津', '重庆', '河北', '山西', '河南', '辽宁', '吉林', '黑龙江', '内蒙古', '江苏', '山东', '安徽', '浙江',
                            '福建',
                            '湖北',
                            '湖南', '广东', '广西', '江西', '四川', '海南', '贵州', '云南', '西藏', '陕西', '甘肃', '青海', '宁夏', '新疆', '台湾',
                            '钓鱼岛', '港澳']
        self.chrome = ChromeOption()
        self._sql_server = SqlServerConnect()
        # https://ppzh.jd.com/brand/homePage/index.html
        # self._self_support_cookie = ''
        # self._self_cw_cookie = '__jdv=146207855|direct|-|none|-|1657174772032; __jdu=16571747720322026243301; ceshi3.com=000; wlfstk_smdl=z47tfge6mpo3h0dff11yqfckhcx8g41f; 3AB9D23F7A4B3C9B=QIA4VKJLEBK7HKLL45XNANJUBXCJI26WLREC3OYB5BO33SGYTSOE4O2VVR3FDTBV74CYZBBCBNY7PA5KMTAZT4M7ZE; TrackID=1Y5hz938czDNc2XvWh8QffAurSoXuTD3JrOAAooAkKEUL-J2XAlx_tX3kIsCokShfgI5EqfhWed6kBfosV0T30I0GsSv6GILhoDZS_aaU-xR3e54VagNLgn-ckbJrxqZ0; thor=9A571C89424631D43D598C3647724AB4B910591528150FF0BC01A7F959F9423E3211AD961913C2597F2A3376D049F41C9402496DD69D7977B977FDF0854726EE4E000F47DE2E463EB7FA0FA1D613BB6C0A7147282DCB2C848CDF30064D614EAE54E761406C1E32B95E2786E90E5559C622C82D141DDA9B2A5A5B279304D3360E7C4D8AAE5E9C33C422F6034A295D20E9; pinId=dgESutCIIA-zI_nYeeAplBYfvTcS11Tn; pin=%E6%9D%AD%E5%B7%9E%E8%B5%AB%E5%B0%94%E7%BD%97%E6%AF%8D%E5%A9%B4; unick=%E6%9D%AD%E5%B7%9E%E8%B5%AB%E5%B0%94%E7%BD%97%E6%AF%8D%E5%A9%B4; _tp=it4%2B14DOBPrvaj%2FPkNmMck7HSXyAUdxclPBSrzCyAlnZqdOuvNDQCy2LhRXlU5v0U8EDdqveOppmC%2B913hA9SQ%3D%3D; _pst=%E6%9D%AD%E5%B7%9E%E8%B5%AB%E5%B0%94%E7%BD%97%E6%AF%8D%E5%A9%B4; __jda=243891652.16571747720322026243301.1657174772.1657174772.1657245170.2; __jdb=243891652.8.16571747720322026243301|2.1657245170; __jdc=243891652'
        # https://shop.jd.com/
        # self._official_child_cookie = '__jdv=146207855|direct|-|none|-|1657174772032; __jdu=16571747720322026243301; wlfstk_smdl=z47tfge6mpo3h0dff11yqfckhcx8g41f; TrackID=1Y5hz938czDNc2XvWh8QffAurSoXuTD3JrOAAooAkKEUL-J2XAlx_tX3kIsCokShfgI5EqfhWed6kBfosV0T30I0GsSv6GILhoDZS_aaU-xR3e54VagNLgn-ckbJrxqZ0; language=zh_CN; thor=751715ACBEE2982718A7FEDE27313485895036B88C1B8053FCB6811E5E11B1F2903B9F2D7A367ABFE743336AE52BDBD6A00BCAFE197EB9C944D1934B03C88F74422311EBF664083D2CFACB3A1FB14175FBB1BF74107BCAC2925677277137D4DF86177888AD86C4A3DFDDFFBC3A5499ACF7428FAF3B86D32AA24A612BA98EACA509B03F6CD474A44AAB2D791EC6AB8BE1; pinId=B2ZA7eoLx8wzT_oMIL7_p7LMtnOLFJYo; pin=%E8%B4%9D%E5%BE%B7%E7%BE%8E-%E7%BB%83%E5%BA%86%E9%BE%99%E9%A3%9E; unick=%E8%B4%9D%E5%BE%B7%E7%BE%8E-%E7%BB%83%E5%BA%86%E9%BE%99%E9%A3%9E; ceshi3.com=000; _tp=upq2zdrgTySxIV7uWxDrIMmY%2FT1VqMClsHkqxT7lYiBR7TGb%2Fb3Gk5KxGzf7UV1akBbwNE%2F%2B750Hxs8edpL3O6h3%2F6KAnkKl%2FeXXhrn3lyk%3D; _pst=%E8%B4%9D%E5%BE%B7%E7%BE%8E-%E7%BB%83%E5%BA%86%E9%BE%99%E9%A3%9E; _BELONG_CLIENT_=WPSC4XJXWK5USS4JNZY2X7VRLR5MCBKRSVHEXABGTHDGISIQK5YOLZUXYE7IOIM7MOKO74H6CRN6WHAAR4TMDV3XZWMXZRCRT5XRNE3V356BTOB2Y7LPK66VWQK6HPTGWVXIDXDCPVE3W5WMHAIO6AT2LX2XXVNUCXR34ZWFK6HY45CORGIKOSYDYZBF27WOKTUX6BS4FZMIJWNUX6CB4JAA25ZLF7ZEKYOO4QV5HTSBXGNRM3E242MBI6V5D4C5VJDQ3EOYCOW5BMTUJZACIBHXQFAVLRF76VQY5PNJGGJNBEZHSFYYJA3YORRT7FB5AHCOIFQKF3W5RWNUX6CB4JAA26JNMO7AYWNUPZF5HTSBXGNRM3E242MBI6V5D4C5VJDQ3EOYCOW5BWZDKMOJ5BS6II53ERY6ALV3ZWPF42L4CPUHEGPYIII35KDC4FCNVCORCXFD6IVNLBEDPB2GGP4UHWNRUDOQBDIW7RZJXBA2WV5ANZOTEGUCDWYRVQS2YUTIZNZ276PRYG4N56V6YTII7MBKBC7LYHO7C555HTSBXGNRM3E466AYN67DHWVM5HQFJ4NFDO5BSSGPF3APAKXZWXSRGUYHICMMPZI; _vender_new_=GI63BGTJFDBQ4O2WMTYXOTMC3MTJZ6FVTAA6JXRVBKOK2RCXEP2DHWHCYDJJOUFL3LV7Y3FKP274A2LGYDALPI323MYXGKTUNCDY3I2J7TUZOTUHWDITKCU4VVCFOI7UUTDSONFJGYBN5NVIUAUPD2U4MRQMIY4EBHC2ZCSEYWNOT6OTGQSCPLHMOSK7627X7FZRW7AT4EHN34KWLQ7RNFQHQK6YDEYAAGI7MSP3KDUX6P7AC24M7PGGT6YDUZJFLTNYHULFPYG5XUMB5HWYNGXDK7Z5LCDSSOBDPFJIJEBIKUU2FDJQ2WCBSB6XFSFPKGUC3H6Z5LYILDSHB7PTQK7UJY2KIDIDPHM2QRXK2MKISKBQSYHJWJELNPO3FF32GSSA2A3Z3GUEN2WTCSESQMEWB2BTQTXFPJS7PSCFUGVPOP2ELQNSLNYPF252SDXJ524Q2TRYA7ADUMGAKLDRC4CRIYTQNS6YL25ZCMAVZTSFWARKKA6PH6BZN7TEZWTDTAY57FXQFRMTGZOSXX4O6GGMPIQDNEP7I4IXEJ7NE5U4CA2PMUML7YJB7HHP66XPV6XMQ7HNUIEAL5XWHQVPF4MKOBJVBQR3GD2FEYBEME5BJ6CWEDNW7UB3GE675BABZMOQJJSTUQMBL45RMCJAJE3OVUYWDXW5FAMLL2ECDZEUAGS3SFNQ; b-sec=XUROMNHNPTBCXRWO6JYKL4F4B3SWFIVXUZIQ5CSVYIN5OERFO2FB5YPCB6RAAVOX7K2TWB2QMDCWMJZTHRSPWIHSYQ; __jdc=27966078; __jdb=27966078.14.16571747720322026243301|2.1657245170; __jda=27966078.16571747720322026243301.1657174772.1657174772.1657245170.2; JSESSIONID=E8D62F7800C55943FF4BF7357764D044.s1; universityLanguage=zh_CN; xue_userTypeCookieName86415014f0f139efc1b2ea8ebce182dd="{\"1\":\"POP\"}"; xue_userTypePageCookieName86415014f0f139efc1b2ea8ebce182dd=1; 3AB9D23F7A4B3C9B=QIA4VKJLEBK7HKLL45XNANJUBXCJI26WLREC3OYB5BO33SGYTSOE4O2VVR3FDTBV74CYZBBCBNY7PA5KMTAZT4M7ZE; _base_=YKH2KDFHMOZBLCUV7NSRBWQUJPBI7JIMU5R3EFJ5UDHJ5LCU7R2NILKK5UJ6GLA2RGYT464UKXAI5KK7PNC5B5UHJ2HVQ4ENFP57OC6PFTNGK572BGCOBAL2DUH7NATOTCNE6YVKRXISVFYORKEVSXKKV3TPWA3DW2RLWZCSG4SOQWCP5WPWO6EFS7HEHMRWVKBRVHB33TFD4LPBGIUGI546P7NTVFOE5ALAQOKBFWQG5PUOLY7PCVS4H4LJMB4CXWAZGAABSH3ET62Q5F7T7YAWXDH3ZRU7WA5GKJMYGGXIN62B2M7UBSRP2BADLWCZOUWN37KLUDO7MEUW5GH7AED2SO23LPYV3KXRDQ3EEDABCU2WEDL6EFUQD4VXX623DGCJKY6NYXK7Y'

    # 精准通_京挑客主函数
    def _accurate_communication_jing_pick_guest_main(self, start_day, end_day, table):
        '''
        params:
            cookie:登录的账号信息
            start_time：开始抓取的日期
            end_time: 今天的日期，结束时间
        '''
        try:
            start_day, end_day, result = self._sql_server.get_day_to_start(start_day, end_day, table,
                                                                           '日期',
                                                                           '')
            print(result)
            if not result:
                msg = f'{start_day}~{end_day}: 《{table}》 数据已存在'
                return msg
            # while True:
            values = []
            datas = self._accurate_communication_jing_pick_guest_requests(start_day, end_day, table)
            for data in datas['result']['trendList']:
                if data['repDate'] == None:
                    continue
                repDate = data['repDate']
                planCost = data['planCost']  # 日结算
                inOrderComm = data['inOrderComm']  # 预估服务费
                inOrderCount = data['inOrderCount']  # 引入订单行量
                inOrderPrice = data['inOrderPrice']  # 引入订单金额
                inROI = data['inROI']  # 预估ROI
                carCount = data['carCount']  # 加购数

                value = (repDate, planCost, inOrderComm, inOrderCount, inOrderPrice, inROI, carCount)
                print(value)
                if value not in values:
                    values.append(value)
            print(values)
            self._sql_server.save_message(table, values, '')
            return f"""{start_day}~{end_day}:《{table}》 抓取成功"""
        except:
            error_message(0)
            return f"""{start_day}~{end_day}:《{table}》 抓取失败"""

    # 精准通_京挑客_请求函数
    def _accurate_communication_jing_pick_guest_requests(self, start_day, end_day, table):
        if table == '贝德美.JDGF.京准通_京挑客账户概况':
            cookie = self._official_cookie
        else:
            cookie = self._self_support_cookie
        try:
            url = 'https://jzt-api.jd.com/union/pop/report/jtk/trend?requestFrom=0'
            headers = {
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'no-cache',
                'content-length': '81',
                'content-type': 'application/json;charset=UTF-8',
                'cookie': cookie,
                'language': 'zh_CN',
                'origin': 'https://jzt.jd.com',
                'pragma': 'no-cache',
                'referer': 'https://jzt.jd.com/home/',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'siteid': '0',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
            }
            data = {"startDate": start_day, "endDate": end_day}
            response = requests.post(url, headers=headers, json=data).json()
            print(response)
            return response
        except:
            error_message(0)

    # 精准通_启动函数
    def accurate_communication_jing_pick_guest_jdgf_start(self):
        start_day = ''
        end_day = ''
        self._accurate_communication_jing_pick_guest_main(start_day, end_day, '贝德美.JDGF.京准通_京挑客账户概况')

    def accurate_communication_jing_pick_guest_jdzy_start(self):
        start_day = ''
        end_day = ''
        self._accurate_communication_jing_pick_guest_main(start_day, end_day, '贝德美.JDZY.京准通_京挑客账户概况')

    # 精准通_RTB账户主函数
    def _precision_RTB_account_main(self, start_day, end_day, data_type):
        try:
            if data_type == '自营':
                table = '贝德美.JDZY.京准通_RTB账户概况'
                req_cookie = self._self_support_cookie
            else:
                table = '贝德美.JDGF.京准通_RTB账户概况'
                req_cookie = self._official_cookie
            try:
                # end_time = get_before_day(end_time)
                start_day, end_day, result = self._sql_server.get_day_to_start(start_day, end_day, table, '日期',
                                                                               '')
                if not result:
                    msg = f'{start_day}~{end_day}: 《{table}》 数据已存在'
                    return msg
                values = []
                business_list = {1: '京东展位', -2: '京东直投', 2: '京东快车', 16777216: '购物触点', 524288: '京东海投'}
                url = 'https://jzt-api.jd.com/common/trendchart?requestFrom=0'
                headers = {
                    'accept': 'application/json, text/plain, */*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'zh-CN,zh;q=0.9',
                    'cache-control': 'no-cache',
                    'content-length': '81',
                    'content-type': 'application/json;charset=UTF-8',
                    'cookie': req_cookie,
                    'language': 'zh_CN',
                    'origin': 'https://jzt.jd.com',
                    'pragma': 'no-cache',
                    'referer': 'https://jzt.jd.com/home/',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'siteid': '0',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest',
                }
                for businessType in business_list:
                    data = {"businessType": businessType, "granularity": 1, "startDay": start_day, "endDay": end_day}
                    res = requests.get(url, headers=headers, json=data)
                    print(res.text)
                    business = business_list[businessType]
                    for i in res.json()['data']['main']:
                        if i['clickDate'] == None:
                            continue
                        clickDate = list(i['clickDate'])
                        cost = i['cost']  # 花费
                        impressions = i['impressions']  # 展示数
                        clicks = i['clicks']  # 点击数
                        CTR = float(i['CTR']) / 100  # 点击率
                        CPM = i['CPM']  # 平均千次展示成本
                        CPC = i['CPC']  # 平均点击成本
                        totalOrderCnt = i['totalOrderCnt']  # 总订单行
                        totalOrderSum = i['totalOrderSum']  # 总订单金额
                        if float(cost) + float(impressions) + float(clicks) + float(CPM) + float(CPC) + float(
                                totalOrderCnt) + float(totalOrderSum) + float(CTR) == 0:
                            continue
                        clickDate.insert(4, '-')
                        clickDate.insert(7, '-')
                        clickDate = ''.join(clickDate)
                        value = (
                        clickDate, business, cost, impressions, clicks, CTR, CPM, CPC, totalOrderCnt, totalOrderSum)
                        if value not in values:
                            values.append(value)
                        print(f'{clickDate}{business}获取完毕')
                print(values)
                self._sql_server.save_message(table, values, '')
                return f"""{start_day}~{end_day}:《{table}》 抓取成功"""
            except:
                error_message(0)
                return f"""{start_day}~{end_day}:《{table}》 抓取失败"""
        except:
            error_message(0)

    # 精准通_RTB账户启动函数
    def precision_RTB_account_jdgf_start(self):
        start_time = ''
        end_time = ''
        self._precision_RTB_account_main(start_time, end_time, '官方')

    def precision_RTB_account_jdzy_start(self):
        start_time = ''
        end_time = ''
        self._precision_RTB_account_main(start_time, end_time, '自营')


    # 交易构成_商品主函数
    def _transaction_constitute_commodity_main(self, start_day, end_day):
        try:
            start_day, end_day, result = self._sql_server.get_day_to_start(start_day, end_day, '贝德美.JDZY.交易构成_商品', '日期',
                                                                           '')
            if not result:
                msg = f'{start_day}~{end_day}: 《贝德美.JDZY.交易构成_商品》 数据已存在'
                return msg
            for d in range(int(time.mktime(time.strptime(start_day, "%Y-%m-%d"))),
                           int(time.mktime(time.strptime(end_day, "%Y-%m-%d"))) + 1, 86400):
                values = []
                timeArray = time.localtime(d)
                day = time.strftime("%Y-%m-%d", timeArray)
                skuId_list = [100008333825, 100008333905, 100019407056, 100019637510, 100019637498, 100019637512,
                              100016761168,
                              100019594750, 100019637492, 100014913294, 100016761134, 100016761136, 100010683173,
                              100010760081,
                              100008333811, 100021327704, 100011699503, 100011989337, 100023360866, 100023360878,
                              100023757526,
                              100023757528, 100024462256, 100024462258, 100013900817, 100025989296, 100026104644,
                              100026104638,
                              100026104612, 100014327793, 100027373054, 100027838440, 100014821475, 100016183375,
                              100029418390,
                              100029418366]
                for skuId in skuId_list:
                    params = {
                        'firstCategoryId': '',
                        'secondCategoryId': '',
                        'thirdCategoryId': 'all',  # 类目
                        'channel': '0',  # 终端
                        'brandId': 'all',  # 品牌
                        'shopType': 'all',  # 经营模式
                        'skuId': skuId,
                        'date': day,
                        'startDate': day,
                        'endDate': day,
                        'type': '1',
                        'uuid': 'df3106b9098069a0a950-17849845fd0',
                    }
                    res = self._transaction_constitute_commodity_request(params)
                    if res.json()['content'] == {}:
                        value = (day, skuId, None, None, None, None, None, None, None, None)
                    else:
                        pv = res.json()['content']['summary']['PV']['Value']  # 浏览量
                        UV = res.json()['content']['summary']['UV']['Value']  # 访客数
                        DealUser = res.json()['content']['summary']['DealUser']['Value']  # 成交人数
                        DealRate = res.json()['content']['summary']['DealRate']['Value']  # 成交转化率
                        DealNum = res.json()['content']['summary']['DealNum']['Value']  # 成交单量
                        DealProNum = res.json()['content']['summary']['DealProNum']['Value']  # 成交商品件数
                        DealAmt = res.json()['content']['summary']['DealAmt']['Value']  # 成交金额
                        DealPriceAvg = res.json()['content']['summary']['DealPriceAvg']['Value']  # 成交客单价
                        value = (day, skuId, pv, UV, DealUser, DealRate, DealNum, DealProNum, DealAmt, DealPriceAvg)
                        pid_list = self._sql_server.check_message(
                            "select * from 贝德美.JDZY.交易构成_商品 WHERE 日期 = '{}' and 商品ID = '{}'".format(day, skuId), 1)
                        if pid_list == []:
                            print(value)
                            values.append(value)
                print(f'{day}抓取完毕')
                self._sql_server.save_message('贝德美.JDZY.交易构成_商品', values)
            return f"""{start_day}~{end_day}:《贝德美.JDZY.交易构成_商品》 抓取成功"""
        except:
            error_message(0)
            return f"""{start_day}~{end_day}:《贝德美.JDZY.交易构成_商品》 抓取失败"""

    # 交易构成_商品_请求函数
    def _transaction_constitute_commodity_request(self, params):
        url = 'https://ppzh.jd.com/brand/dealAnalysis/dealSummary/getVenderDealSummayData.ajax'
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': self._self_support_cookie,
            'p-pin': 'gru33616540',
            'pragma': 'no-cache',
            'referer': 'https://ppzh.jd.com/brand/dealAnalysis/dealSummary.html',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'user-mnp': '68ba76c14801515f3e47fc80e56858a3',
            'user-mup': '1616140939720',
            'x-requested-with': 'XMLHttpRequest',
        }
        res = requests.get(url, headers=headers, params=params)
        return res

    # 交易构成_商品启动函数
    def transaction_constitute_commodity_start(self):
        start_time = ''
        end_time = ''
        self._transaction_constitute_commodity_main(start_time, end_time)


    # 京麦_财务管理_实销实结明细主函数
    def _details_of_actual_sales_and_actual_settlement_main(self, start_day, end_day, table, cookie, name):
        try:
            start_day, end_day, result = self._sql_server.get_day_to_start(start_day, end_day,
                                                                           table, '业务日期',
                                                                           {'供应商名称': name})
            page = 1
            while 1:
                values = []
                res = self._details_of_actual_sales_and_actual_settlement_request(start_day, end_day, page, cookie)
                # print(res.json())
                for i in res.json()['jsonList']:
                    refType = i['refType']
                    channelName = i['channelName']
                    refId = i['refId']
                    poId = i['poId']
                    orderNo = i['orderNo']
                    s_id = refId.split('-')[0] if refType == '售后退货' else None
                    buyerName = i['buyerName']
                    ouName = i['ouName']
                    sku = i['sku']
                    skuNum = i['skuNum']
                    amount = i['amount']
                    refDate = time.strftime("%Y-%m-%d", time.localtime(i['refDate'] / 1000))
                    if str(refDate) == get_today():
                        break
                    value = (
                        name, refType, channelName, refId, poId, orderNo, s_id, buyerName, ouName, None, sku, skuNum, amount,
                        refDate)
                    print(value)
                    select_sql = "select * from {} WHERE 订单号 = '{}' AND sku编号 = '{}' AND 业务日期 = '{}'AND 采购单号 = '{}'".format(
                        table, orderNo, sku, refDate, poId)
                    pid_list = self._sql_server.check_message(select_sql, 1)
                    # print(pid_list)
                    if pid_list == []:
                        if value not in values:
                            values.append(value)
                if page <= res.json()['total']:
                    page += 1
                else:
                    break
                self._sql_server.save_message(table, values)
            return f"""{start_day}~{end_day}:《{table}》 抓取成功"""
        except:
            error_message(1)
            return f"""{start_day}~{end_day}:《贝德美.JDZY.京麦_财务管理_实销实结明细》 抓取失败"""

    # 京麦_财务管理_实销实结明细请求函数
    def _details_of_actual_sales_and_actual_settlement_request(self, start_day, end_day, page, cookie):
        try:
            url = 'https://vcf.jd.com/sub_finance/saleBill/initJson'
            headers = {
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'no-cache',
                'content-length': '73',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'cookie': cookie,
                'origin': 'https://vcf.jd.com',
                'pragma': 'no-cache',
                'referer': 'https://vcf.jd.com/sub_finance/saleBill/init?_source=pop',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
            }
            data = {
                'refType': '70',
                'refDateFrom': start_day,
                'refDateTo': end_day,
                'length': '100',
                'page': page,
                'sidx': '',
                'sord': '',
            }
            res = requests.post(url, headers=headers, data=data)
            return res
        except:
            error_message(0)

    # 京麦_财务管理_实销实结明细启动函数
    def details_of_actual_sales_and_actual_settlement_zjyt_start(self):
        start_day = ''
        end_day = ''
        self._details_of_actual_sales_and_actual_settlement_main(start_day, end_day, '贝德美.JDZY.京麦_财务管理_实销实结明细', self._self_support_cookie, '浙江孕町母婴用品有限公司')

    # 京麦_财务管理_实销实结明细启动函数
    def details_of_actual_sales_and_actual_settlement_hel_start(self):
        start_day = ''
        end_day = ''
        self._details_of_actual_sales_and_actual_settlement_main(start_day, end_day, '贝德美.JDZY.京麦_财务管理_实销实结明细', self._self_cw_cookie, '杭州赫尔罗母婴用品有限公司')


    # 京东自营_报表_店铺_日主函数
    def _operated_statement_shop_day_main(self, start_day, end_day):
        try:
            start_day, end_day, result = self._sql_server.get_day_to_start(start_day, end_day, '贝德美.JDZY.报表_店铺_日', '日期',
                                                                           '')
            if not result:
                msg = f'{start_day}~{end_day}: 《贝德美.JDZY.报表_店铺_日》 数据已存在'
                return msg
            values = []
            for d in range(int(time.mktime(time.strptime(start_day, "%Y-%m-%d"))),
                           int(time.mktime(time.strptime(end_day, "%Y-%m-%d"))) + 1, 86400 * 35):
                start = time.strftime("%Y-%m-%d", time.localtime(d))
                end = time.strftime("%Y-%m-%d", time.localtime(d + 34 * 86400)) if d + 86400 * 34 <= int(
                    time.mktime(time.strptime(end_day, "%Y-%m-%d"))) else end_day
                params = {
                    'firstCategoryId': '',
                    'secondCategoryId': '',
                    'thirdCategoryId': '1555,1556,1557,1559,1560,28090,5000',  # 类目
                    'channel': '0',  # 终端
                    'brandId': '569468',  # 品牌
                    'shopType': 'all',  # 经营模式
                    'date': '10' + end,
                    'startDate': start,
                    'endDate': end,
                    'type': '1',
                    'uuid': 'df3106b9098069a0a950-17849845fd0',
                }
                res = self._operated_statement_shop_day_request(params)
                if not res.json()['content']:
                    continue
                print(res.json())
                date_list = res.json()['content']['trend']['categories']
                pp = ["贝德美（bodcrme）" for i in range(len(date_list))]
                pv = res.json()['content']['trend']['series'][0]['data']  # 浏览量
                UV = res.json()['content']['trend']['series'][1]['data']  # 访客数
                DealUser = res.json()['content']['trend']['series'][2]['data']  # 成交人数
                DealRate = res.json()['content']['trend']['series'][3]['data']  # 成交转化率
                DealNum = res.json()['content']['trend']['series'][4]['data']  # 成交单量
                DealProNum = res.json()['content']['trend']['series'][5]['data']  # 成交商品件数
                DealAmt = res.json()['content']['trend']['series'][6]['data']  # 成交金额
                DealPriceAvg = res.json()['content']['trend']['series'][7]['data']  # 成交客单价
                for value in zip(date_list, pp, pv, UV, DealUser, DealRate, DealNum, DealProNum, DealAmt, DealPriceAvg):
                    if start == end and value[0].split(' ')[0] != start:
                        continue
                    values.append(value)
                    print(f'{value[0]}获取完毕')
            if values:
                self._sql_server.save_message('贝德美.JDZY.报表_店铺_日', values)
            return f"""{start_day}~{end_day}:《贝德美.JDZY.报表_店铺_日》 抓取成功"""
        except:
            error_message(1)
            return f"""{start_day}~{end_day}:《贝德美.JDZY.报表_店铺_日》 抓取失败"""

    # 京东自营_报表_店铺_日请求函数
    def _operated_statement_shop_day_request(self, params):
        try:
            url = 'https://ppzh.jd.com/brand/dealAnalysis/dealSummary/getVenderDealSummayData.ajax'
            headers = {
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'no-cache',
                'cookie': self._self_cw_cookie,
                'p-pin': '%E6%9D%AD%E5%B7%9E%E8%B5%AB%E5%B0%94%E7%BD%97%E6%AF%8D%E5%A9%B4',
                'pragma': 'no-cache',
                'referer': 'https://ppzh.jd.com/brand/dealAnalysis/dealSummary.html',
                'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': "Windows",
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
                'user-mnp': 'bbe2c17f0fbfda839e3d2743e94b6838',
                'user-mup': '1652161641544',
                'x-requested-with': 'XMLHttpRequest',
            }
            res = requests.get(url, headers=headers, params=params)
            return res
        except:
            error_message(0)

    # 京东自营_报表_店铺_日启动函数
    def operated_statement_shop_day_start(self):
        start_day = ''
        end_day = ''
        msg = self._operated_statement_shop_day_main(start_day, end_day)


    # 官方报表店铺日主函数
    def _official_operated_statement_shop_day_main(self, start_day, end_day):
        while True:
            try:
                start_day, end_day, result = self._sql_server.get_day_to_start(start_day, end_day, '贝德美.JDGF.报表_店铺_日', '日期',
                                                                               '')
                if not result:
                    msg = f'{start_day}~{end_day}: 《贝德美.JDGF.报表_店铺_日》 数据已存在'
                    return msg
                values = []
                res = self._official_operated_statement_shop_day_request(start_day)
                response = self._official_operated_statement_shop_day_request1(start_day)
                AmtTH = response['content']['summary']['AmtTH']['value']
                print(res.text)
                for i in json.loads(res.text)['content']['pageList']['data']:
                    i.append(AmtTH)
                    value = tuple(i)
                    print(f'{value[0]}获取完毕')
                    values.append(value)
                self._sql_server.save_message('贝德美.JDGF.报表_店铺_日', values)
            except:
                error_message(1)
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)

    def _official_operated_statement_shop_day_request1(self, start_day):
        url = 'https://sz.jd.com/sz/api/serviceAnalysis/getSummaryData.ajax'
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': self._official_child_cookie,
            'p-pin': '%E8%B4%9D%E5%BE%B7%E7%BE%8E%E5%AE%98%E6%96%B9%E6%97%97%E8%88%B0%E5%BA%97',
            'referer': 'https://sz.jd.com/sz/view/serviceAnalysis/serviceMonitors.html',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
            'user-mnp': 'ab8bf93123746773d1d2e9300031cd89',
            'user-mup': '1650777883085',
            'uuid': '6a82d21161a8599e8c49-1805a0781cd'
        }
        params = {
            'date': start_day,
            'endDate': start_day,
            'startDate': start_day
        }
        response = requests.get(url=url, headers=headers, params=params).json()
        print(response)
        return response



    # 官方报表店铺日请求函数
    def _official_operated_statement_shop_day_request(self, start_day):
        try:
            url = f'https://sz.jd.com/sz/api/selfHelpAnalysis/createPagePreview.ajax?Indicators=%5B%7B%22value%22:%22APV%22,%22text%22:%22%E6%B5%8F%E8%A7%88%E9%87%8F-%E5%85%A8%E9%83%A8%E6%B8%A0%E9%81%93%22,%22selected%22:true,%22index%22:1%7D,%7B%22value%22:%22AUV%22,%22text%22:%22%E8%AE%BF%E5%AE%A2%E6%95%B0-%E5%85%A8%E9%83%A8%E6%B8%A0%E9%81%93%22,%22selected%22:true,%22index%22:2%7D,%7B%22value%22:%22AStayTi%22,%22text%22:%22%E5%B9%B3%E5%9D%87%E5%81%9C%E7%95%99%E6%97%B6%E9%95%BF(%E7%A7%92)-%E5%85%A8%E9%83%A8%E6%B8%A0%E9%81%93%22,%22selected%22:true,%22index%22:3%7D,%7B%22value%22:%22AOUV%22,%22text%22:%22%E8%80%81%E8%AE%BF%E5%AE%A2%E6%95%B0-%E5%85%A8%E9%83%A8%E6%B8%A0%E9%81%93%22,%22selected%22:true,%22index%22:4%7D,%7B%22value%22:%22AOrdAmt%22,%22text%22:%22%E6%88%90%E4%BA%A4%E9%87%91%E9%A2%9D-%E5%85%A8%E9%83%A8%E6%B8%A0%E9%81%93%22,%22selected%22:true,%22index%22:5%7D,%7B%22value%22:%22AOrdNum%22,%22text%22:%22%E6%88%90%E4%BA%A4%E5%8D%95%E9%87%8F-%E5%85%A8%E9%83%A8%E6%B8%A0%E9%81%93%22,%22selected%22:true,%22index%22:6%7D,%7B%22value%22:%22AOrdCustNum%22,%22text%22:%22%E6%88%90%E4%BA%A4%E5%AE%A2%E6%88%B7%E6%95%B0-%E5%85%A8%E9%83%A8%E6%B8%A0%E9%81%93%22,%22selected%22:true,%22index%22:7%7D,%7B%22value%22:%22AOrdProNum%22,%22text%22:%22%E6%88%90%E4%BA%A4%E5%95%86%E5%93%81%E4%BB%B6%E6%95%B0-%E5%85%A8%E9%83%A8%E6%B8%A0%E9%81%93%22,%22selected%22:true,%22index%22:8%7D,%7B%22value%22:%22ACustPriceAvg%22,%22text%22:%22%E5%AE%A2%E5%8D%95%E4%BB%B7-%E5%85%A8%E9%83%A8%E6%B8%A0%E9%81%93%22,%22selected%22:true,%22index%22:9%7D,%7B%22value%22:%22AToOrdRate%22,%22text%22:%22%E6%88%90%E4%BA%A4%E8%BD%AC%E5%8C%96%E7%8E%87-%E5%85%A8%E9%83%A8%E6%B8%A0%E9%81%93%22,%22selected%22:true,%22index%22:10%7D,%7B%22text%22:%22%E8%80%81%E5%AE%A2%E6%88%B7%E6%95%B0%22,%22value%22:%22OldUserNum%22,%22selected%22:true,%22index%22:11%7D,%7B%22text%22:%2230%E5%A4%A9%E9%87%8D%E5%A4%8D%E8%B4%AD%E4%B9%B0%E7%8E%87%22,%22value%22:%22The30Rate%22,%22selected%22:true,%22index%22:12%7D,%7B%22text%22:%2290%E5%A4%A9%E9%87%8D%E5%A4%8D%E8%B4%AD%E4%B9%B0%E7%8E%87%22,%22value%22:%22The90Rate%22,%22selected%22:true,%22index%22:13%7D,%7B%22value%22:%22AProPV%22,%22text%22:%22%E5%95%86%E5%93%81%E6%B5%8F%E8%A7%88%E9%87%8F-%E5%85%A8%E9%83%A8%E6%B8%A0%E9%81%93%22,%22selected%22:true,%22index%22:14%7D,%7B%22value%22:%22AProUV%22,%22text%22:%22%E5%95%86%E5%93%81%E8%AE%BF%E5%AE%A2%E6%95%B0-%E5%85%A8%E9%83%A8%E6%B8%A0%E9%81%93%22,%22selected%22:true,%22index%22:15%7D,%7B%22value%22:%22AVisNum%22,%22text%22:%22%E8%A2%AB%E8%AE%BF%E9%97%AE%E5%95%86%E5%93%81%E6%95%B0(SPU)-%E5%85%A8%E9%83%A8%E6%B8%A0%E9%81%93%22,%22selected%22:true,%22index%22:16%7D,%7B%22value%22:%22AAddPie%22,%22text%22:%22%E5%8A%A0%E8%B4%AD%E5%95%86%E5%93%81%E4%BB%B6%E6%95%B0-%E5%85%A8%E9%83%A8%E6%B8%A0%E9%81%93%22,%22selected%22:true,%22index%22:17%7D,%7B%22value%22:%22AAddCustNum%22,%22text%22:%22%E5%8A%A0%E8%B4%AD%E5%AE%A2%E6%88%B7%E6%95%B0-%E5%85%A8%E9%83%A8%E6%B8%A0%E9%81%93%22,%22selected%22:true,%22index%22:18%7D,%7B%22text%22:%22%E5%95%86%E5%93%81%E5%85%B3%E6%B3%A8%E6%95%B0%22,%22value%22:%22ACollNum%22,%22selected%22:true,%22index%22:19%7D,%7B%22text%22:%22%E5%BA%97%E9%93%BA%E5%85%B3%E6%B3%A8%E4%BA%BA%E6%95%B0%22,%22value%22:%22ShopCollNum%22,%22selected%22:true,%22index%22:20%7D%5D&ReportCycle=0&ReportDim=0&UpdateNum=0&endDate={start_day}&startDate={start_day}'
            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Cookie': self._official_child_cookie,
                'Host': 'sz.jd.com',
                'p-pin': '%E8%B4%9D%E5%BE%B7%E7%BE%8E-%E9%99%88%E8%B6%85',
                'Referer': 'https://sz.jd.com/sz/view/selfHelp/reportCreates.html',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                'User-mnp': 'ba66e4ccffa8c154e32a2944f088a9c1',
                'User-mup': '1613698893156',
                'uuid': '712aa0dd617ab6c09118-177b7f30564',
            }
            res = requests.get(url, headers=headers)
            return res
        except:
            error_message(0)

    # 官方报表店铺日启动函数
    def official_operated_statement_shop_day_start(self):
        start_day = ''
        end_day = ''
        self._official_operated_statement_shop_day_main(start_day, end_day)

    # 商品明细日主函数
    def _commodity_details_main(self, start_day, end_day):
        try:
            start_day, end_day, result = self._sql_server.get_day_to_start(start_day, end_day, '贝德美.JDZY.商品明细_日', '日期',
                                                                           '')
            if not result:
                msg = f'{start_day}~{end_day}: 《贝德美.JDZY.商品明细_日》 数据已存在'
                return msg
            while True:
                values = []
                page = 1
                while True:
                    response = self._commodity_details_request(start_day, page)
                    if not response['content']:
                        break
                    datas = response['content']['data']
                    if not datas:
                        break
                    for data in datas:
                        print(data)
                        ProName = data['ProName']  # 商品名称
                        SkuId = data['SkuId']  # 商品id
                        PV = data['PV']  # 浏览量
                        UV = data['UV']  # 访客数
                        AvgStayTime = round(data['AvgStayTime'])  # 平均停留时长
                        AvgVisitNum = round(data['AvgVisitNum'])  # 人均浏览量
                        ToCartUser = round(data['ToCartUser'], 4)  # 加购人数
                        CartProNum = round(data['CartProNum'], 4)  # 加购商品件数
                        DealUser = round(data['DealUser'], 4)  # 成交人数
                        DealNum = round(data['DealNum'], 4)  # 成交单量
                        DealProNum = round(data['DealProNum'], 4)  # 成交商品件数
                        DealAmt = round(data['DealAmt'], 4)  # 成交金额
                        DealRate = round(data['DealRate'], 4)  # 成交转化率
                        DealPriceAvg = round(data['DealPriceAvg'], 4)  # 成交客单价
                        ToCartRate = round(data['ToCartRate'], 4)  # 加购转化率
                        CollectNum = round(data['CollectNum'], 4)  # 关注人数
                        value = (
                        start_day, ProName, SkuId, PV, UV, AvgStayTime, AvgVisitNum, ToCartUser, CartProNum, DealUser,
                        DealNum, DealProNum, DealAmt, DealRate, DealPriceAvg, ToCartRate, CollectNum)
                        print(value)
                        if value not in values:
                            values.append(value)
                    page += 1
                    print('-------------------------------------')
                self._sql_server.save_message('贝德美.JDZY.商品明细_日', values)
                if start_day == end_day:
                    break
                start_day = get_after_day(start_day)
            return f"""{start_day}~{end_day}:《贝德美.JDZY.商品明细_日》 抓取成功"""
        except:
            error_message(1)
            return f"""{start_day}~{end_day}:《贝德美.JDZY.商品明细_日》 抓取失败"""

    # 商品明细日请求函数
    def _commodity_details_request(self, start_day, page):
        url = 'https://ppzh.jd.com/brand/productAnalysis/productDetail/getProData.ajax'
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': self._self_support_cookie,
            'p-pin': 'gru33616540',
            'pragma': 'no-cache',
            'referer': 'https://ppzh.jd.com/brand/productAnalysis/productDetail.html',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'user-mnp': '018f914af0d82271da89ae070e1d3649',
            'user-mup': '1640326141084',
            'x-requested-with': 'XMLHttpRequest'
        }
        params = {
            'thirdCategoryId': '1555,1556,1557,1558,1559,1560,21420,5000',
            'channel': '0',
            'brandId': '569468',
            'shopType': 'all',
            'date': f'{start_day}',
            'startDate': f'{start_day}',
            'endDate': f'{start_day}',
            'orderBy': 'PV desc',
            'pageNum': f'{page}',
            'pageSize': '10',
            'uuid': 'cf8bf017015f5590f204-17deb0e949c'
        }
        response = requests.get(url=url, headers=headers, params=params).json()
        print(response)
        return response

    # 商品明细日启动函数
    def commodity_details_start(self):
        start_day = ''
        end_day = ''
        msg = self._commodity_details_main(start_day, end_day)


    # 交易构成_城市主函数
    def _transaction_composition_city_main(self, start_day, end_day):
        try:
            start_day, end_day, result = self._sql_server.get_day_to_start(start_day, end_day, '贝德美.JDZY.交易构成_商品_城市', '日期',
                                                                           '')
            if not result:
                msg = f'{start_day}~{end_day}: 《贝德美.JDZY.交易构成_商品_城市》 数据已存在'
                return msg
            sql = f"SELECT top 15 商品ID FROM [JDZY].[商品明细_日] where 日期 = '{start_day}' order by [成交金额] desc"
            skuids = self._sql_server.check_message(sql, 1)
            print(skuids)
            while True:
                values = []
                for skuid in skuids:
                    for citys_s in self.citys_sheng:
                        params = {
                            'firstCategoryId': '',
                            'secondCategoryId': '',
                            'thirdCategoryId': 'all',
                            'channel': '0',
                            'brandId': 'all',
                            'shopType': 'all',
                            'skuId': skuid[0],
                            'date': start_day,
                            'startDate': start_day,
                            'endDate': start_day,
                            'pageOrder': 'descend',
                            'provinceName': citys_s,
                            'orderBy': 'DealAmt',
                            'uuid': '0916fff9c6ac7242a106-17dfa69124c'
                        }
                        response = self._transaction_composition_city_request(params)
                        if not response['content']:
                            continue
                        datas = response['content']['data']
                        for data in datas:
                            city = data['City']  # 城市
                            DealAmt = data['DealAmt']  # 成交金额
                            DealProNum = data['DealProNum']  # 成交件数
                            value = (start_day, skuid[0], citys_s, city, round(DealAmt, 2), DealProNum)
                            print(value)
                            values.append(value)
                self._sql_server.save_message('贝德美.JDZY.交易构成_商品_城市', values)
                if start_day == end_day:
                    break
                start_day = get_after_day(start_day)
            return f"""{start_day}~{end_day}:《贝德美.JDZY.交易构成_商品_城市》 抓取成功"""
        except:
            return f"""{start_day}~{end_day}:《贝德美.JDZY.交易构成_商品_城市》 抓取失败"""

    # 交易构成_城市请求
    def _transaction_composition_city_request(self, params):
        url = 'https://ppzh.jd.com/brand/dealAnalysis/dealConstitute/getAllColumnData.ajax'
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': self._self_support_cookie,
            'p-pin': 'gru33616540',
            'pragma': 'no-cache',
            'referer': 'https://ppzh.jd.com/brand/dealAnalysis/dealConstitute.html',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'user-mnp': 'd215ec3116dfca415ba24f662f27612e',
            'user-mup': '1640582110492',
            'x-requested-with': 'XMLHttpRequest'
        }
        response = requests.get(url=url, headers=headers, params=params).json()
        print(response)
        return response

    # 交易构成_城市启动函数
    def transaction_composition_city_start(self):
        start_day = ''
        end_day = ''
        self._transaction_composition_city_main(start_day, end_day)


    def get_sku_infos_main(self, start_day, end_day):
        while True:
            if not start_day:
                start_day = self._sql_server.get_start_day('贝德美.JDZY.交易构成_商品', '日期', '')
                if start_day == get_before_day(get_today()):
                    return 0
                start_day = get_after_day(start_day)
            if not end_day:
                end_day = get_before_day(get_today())

            sql = f"SELECT distinct sku编号 FROM 贝德美.[JDZY].[京麦_财务管理_实销实结明细] where 业务日期 BETWEEN '{get_day_before_today(start_day, 6)}' and '{start_day}'"
            print(sql)
            sku_ids = self._sql_server.check_message(sql, 1)
            for skuId in sku_ids:
                response = self.get_sku_infos_request(skuId, start_day)
                if not response['content']:
                    continue
                datas = response['content']['summary']
                PV = datas['PV']['Value']  # 浏览量
                UV = datas['UV']['Value']  # 访客数
                DealUser = datas['DealUser']['Value']  # 成交人数
                DealRate = datas['DealRate']['Value']  # 成交转化率
                DealNum = datas['DealNum']['Value']  # 成交单量
                DealProNum = datas['DealProNum']['Value']  # 成交商品件数
                DealAmt = datas['DealAmt']['Value']  # 成交金额
                DealPriceAvg = datas['DealPriceAvg']['Value']  # 成交客单价
                value = (start_day, skuId, PV, UV, DealUser, DealRate, DealNum, DealProNum, DealAmt, DealPriceAvg)
                print(value)
                self._sql_server.save_message('贝德美.JDZY.交易构成_商品', [value])
                time.sleep(1)
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)

    def get_sku_infos_request(self, skuId, start_day):
        url = 'https://ppzh.jd.com/brand/dealAnalysis/dealSummary/getVenderDealSummayData.ajax'
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': self._self_cw_cookie,
            'p-pin': '%E6%9D%AD%E5%B7%9E%E8%B5%AB%E5%B0%94%E7%BD%97%E6%AF%8D%E5%A9%B4',
            'pragma': 'no-cache',
            'referer': 'https://ppzh.jd.com/brand/dealAnalysis/dealSummary.html',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'user-mnp': '6a10e27838b00827c12e08f703a5ba9b',
            'user-mup': '1652421734674',
            'x-requested-with': 'XMLHttpRequest'
        }
        params = {
            'firstCategoryId': '',
            'secondCategoryId': '',
            'thirdCategoryId': 'all',
            'channel': '0',
            'brandId': 'all',
            'shopType': 'all',
            'skuId': skuId,
            'date': start_day,
            'startDate': start_day,
            'endDate': start_day,
            'type': '1',
            'uuid': 'd1d85ca301e5ef0f326f-180bc02b111'
        }
        response = requests.get(url=url, headers=headers, params=params).json()
        return response


if __name__ == '__main__':
    jd = JD()
    # chrome = ChromeOption()
    # # 京东官方账号 cookie获取
    # jd._official_cookie = chrome.jzt_login()
    # #
    # # 贝德美.JDGF.京准通_京挑客账户概况
    # jd.accurate_communication_jing_pick_guest_jdgf_start()
    # # 贝德美.JDGF.京准通_RTB账户概况
    # jd.precision_RTB_account_jdgf_start()
    # chrome.__del__()
    #
    # chrome = ChromeOption()
    # # # 京东自营账号 cookie获取
    # jd._self_support_cookie = chrome.jdsz_login()
    # #
    # # # # 贝德美.JDZY.京准通_京挑客账户概况
    # jd.accurate_communication_jing_pick_guest_jdzy_start()
    # # # 贝德美.JDZY.京准通_RTB账户概况
    # jd.precision_RTB_account_jdzy_start()
    # # # # 贝德美.JDZY.京麦_财务管理_实销实结明细  浙江孕
    # jd.details_of_actual_sales_and_actual_settlement_zjyt_start()
    # # # # 贝德美.JDZY.交易构成_商品
    # # jd.transaction_constitute_commodity_start()
    # # # # 贝德美.JDZY.商品明细_日
    # jd.commodity_details_start()
    # # # # 贝德美.JDZY.交易构成_商品_城市
    # jd.transaction_composition_city_start()
    # chrome.__del__()

    # # 京东自营账号 cookie获取
    chrome = ChromeOption()
    jd._self_cw_cookie = chrome.jdsz_login1()
    #
    # # 贝德美.JDZY.京麦_财务管理_实销实结明细
    jd.details_of_actual_sales_and_actual_settlement_hel_start()
    # # # 贝德美.JDZY.报表_店铺_日
    jd.operated_statement_shop_day_start()
    # # 贝德美.JDZY.交易构成_商品
    jd.get_sku_infos_main('', '')
    chrome.__del__()

    chrome = ChromeOption()
    # 京麦 cookie
    jd._official_child_cookie = chrome.jm_login()
    # jd._official_child_cookie = '__jdv=122270672|direct|-|none|-|1663034274607; __jdu=16630342746061404225074; ipLoc-djd=15-1213-3410-0; areaId=15; PCSYCityID=CN_330000_330100_330105; shshshfp=228a0fb76f5c24ff23e7d284acaf3e2d; shshshfpa=5d9500ec-4419-61af-faec-9cf866d039f2-1663034350; shshshfpb=xmy5px1NLamCjG6Hr0I8kYQ; bjd.advert.popup=3ffeaa3db27984751629b6d6c55222d8; language=zh_CN; _BELONG_CLIENT_=WPSC4XJXWK5USS4JNZY2X7VRLR5MCBKRSVHEXABGTHDGISIQK5YOLZUXYE7IOIM7MOKO74H6CRN6WHAAR4TMDV3XZWMXZRCRT5XRNE3V356BTOB2Y7LPK66VWQK6HPTGWVXIDXDCPVE3W5WMHAIO6AT2LX2XXVNUCXR34ZWFK6HY45CORGIKOSYDYZBF27WOKTUX6BS4FZMIJWNUX6CB4JAA25ZLF7ZEKYOO4QV5HTSBXGNRM3E242MBI6V5D4C5VJDQ3EOYCOW5BMTUJZACIBHXQFAVLRF76VQY5PNJGGJNBEZHSFYYJA3YORRT7FB5AHCOIFQKF3W5RWNUX6CB4JAA26JNMO7AYWNUPZF5HTSBXGNRM3E242MBI6V5D4C5VJDQ3EOYCOW5BWZDKMOJ5BS6II53ERY6ALV3ZWPF42L4CPUHEGPYIII35KDC4FCNVCORCXFD6IVNLBEDPB2GGP4UHWNRUDOQBDIW7RZJXBA2WV5ANZOTEGUCDWYRVQS2YUTIZNZ276PRYG4N56V6YTII7MBKBC7LYHO7C555HTSBXGNRM3E466AYN67DHWVM5HQFJ4NFDO5BSNAUBA65S657ZP5V5KGPLMBYJGY; __USE_NEW_PAGEFRAME__=false; QRCodeKEY=E29A22746B2767243AC1E753B92BA8EF560CCAD56E9CE96330AA0AAB75ACB9D79D2938D1818DA81A6C2501F503C01641; AESKEY=ACC86026EF03F85D; UIDKEY=14492156876089809; thor=751715ACBEE2982718A7FEDE273134858A7CCCDE0EA04AC8B3101D9ED364F93408CF2EBEB69025B83C540D492813AB2D7B456AD94C9D9134FD4D115AF0BB596900F839283F0AC6DE43F0798A2B8B8783ECC7C68A4EB2C2E3B4BA9A9DF28660107C79CB8861E3842B8DB7D62D6D7951CD6B79644115A96745AA0A29FD309516B22D316695DB9276E56974F8B9EB85779A; pinId=B2ZA7eoLx8wzT_oMIL7_p7LMtnOLFJYo; pin=%E8%B4%9D%E5%BE%B7%E7%BE%8E-%E7%BB%83%E5%BA%86%E9%BE%99%E9%A3%9E; unick=%E8%B4%9D%E5%BE%B7%E7%BE%8E-%E7%BB%83%E5%BA%86%E9%BE%99%E9%A3%9E; ceshi3.com=000; _tp=upq2zdrgTySxIV7uWxDrIMmY%2FT1VqMClsHkqxT7lYiBR7TGb%2Fb3Gk5KxGzf7UV1akBbwNE%2F%2B750Hxs8edpL3O6h3%2F6KAnkKl%2FeXXhrn3lyk%3D; _pst=%E8%B4%9D%E5%BE%B7%E7%BE%8E-%E7%BB%83%E5%BA%86%E9%BE%99%E9%A3%9E; 3AB9D23F7A4B3C9B=TFCFOJHRQZOYLK2FWKQSSM6DXK5TSPNZUKXEB3IOZDHWGCSNRIR7CJUCCFYMD33WRIOPG4UWO2T75KEVEBR6P46MTQ; _base_=YKH2KDFHMOZBLCUV7NSRBWQUJPBI7JIMU5R3EFJ5UDHJ5LCU7R2NILKK5UJ6GLA2RGYT464UKXAI5KK7PNC5B5UHJ2HVQ4ENFP57OC6PFTNGK572BGCOBAL2DUH7NATOTCNE6YVKRXISVFYORKEVSXKKV3TPWA3DW2RLWZCSG4SOQWCP5WPWO6EFS7HEHMRWVKBRVHB33TFD4LPBGIUGI546P7NTVFOE5ALAQOKBFWQG5PUOLY7PCVS4H4LJMB4CXWAZGAABSH3ET62Q5F7T7YAWXDH3ZRU7WA5GKJMYGGXIN62B2M7UBSRP2BADLWCZD5LBBSV6RY6N5R2F5ALQO3KIKG23LPYV3KXRDQ3EEDABCU2WEDL6EFUQD4VXX623DGCJKY6NYXK7Y; _vender_new_=GI63BGTJFDBQ4O2WMTYXOTMC3MTJZ6FVTAA6JXRVBKOK2RCXEP2DHWHCYDJJOUFL3LV7Y3FKP274A2LGYDALPI323MYXGKTUNCDY3I2J7TUZOTUHWDITKCU4VVCFOI7UUTDSONFJGYBN5NVIUAUPD2U4MRQMIY4EBHC2ZCSEYWNOT6OTGQSCPLHMOSK7627X7FZRW7AT4EHN34KWLQ7RNFQHQK6YDEYAAGI7MSP3KDUX6P7AC24M7PGGT6YDUZJFLTNYHULFPYG5XUMB5HWYNGXDK7Z5LCDSSOBDPFJIJEBIKUU2FDJQ2WCBSB6XFSFPKGUC3H6Z5LYILDSHB7PTQK7UJY2KIDIDPHM2QRQMKE2RKB2TOGIVGEC6G5QLJAQFGSSA2A3Z3GUEMDCRGUKQOU3RSE7YWKFHXGIGQO2FUGVPOP2ELQNSLNYPF252SDXJ524Q2TRYA7ADUMGAKLDRC4CRIYTQNS6YL25ZCMAVZTSFWARKKA6PH6BZN7TEZWTDTAY57FXQFRMTGZOSXX4O6GGMPIQDNEP7I4IXEJ7NE5U4CA2PMUML7YJB7HHP66XPV6XMQ7HNUIEAL5XWHQVPF4MKOBJVBQR3GD2FEYBEME5BJ6CWEDNW7UB3GE675BABZMOQJJSTUQMBKMLCH5VPFEFPKSAA647OHAXCBPFLUBCRKBPTIOIA; __jda=27966078.16630342746061404225074.1663034275.1663034275.1663036605.2; __jdc=27966078; JSESSIONID=626A3673BC8CC39564F358B5E93F937F.s1; __jdb=27966078.3.16630342746061404225074|2.1663036605'
    # 贝德美.JDGF.报表_店铺_日
    jd.official_operated_statement_shop_day_start()