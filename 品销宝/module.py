import execjs

from Setting import *


class PinXiaoBao:
    def __init__(self):
        self.sql_server = SqlServerConnect()

    def run_main(self, start_day, cookie):
        if not start_day:
            start_day = self.sql_server.get_start_day('贝德美.dbo.品销宝_明星店铺_点击_账户', '日期', '')
            if start_day == get_before_day(get_today()):
                print('数据获取完毕')
                return 0
            start_day = get_before_day(get_today())
        self.delete_30_change()
        csrfID = self.getcsrftoken(cookie)
        print(csrfID)
        print(start_day)
        url = f'https://brandsearch.taobao.com/report/query/rptAdvertiserSubListNew.json?attribution=click&startDate={get_day_before_today(start_day, 29)}&endDate={start_day}&effectConversionCycle=30&trafficType=%5B1%2C2%2C4%2C5%5D&productId=101005202&t={int(time.time()*1000)}&csrfID={csrfID}&_bx-v=1.1.20'
        print(url)
        # url = 'https://brandsearch.taobao.com/report/query/rptAdvertiserSubListNew.json?attribution=click&startDate=2022-06-27&endDate=2022-07-26&effectConversionCycle=30&trafficType=%5B1%2C2%2C4%2C5%5D&productId=101005202&t=1658914255635&csrfID=165891403178008409542458425027917&_bx-v=1.1.20'
        # url = 'https://brandsearch.taobao.com/report/query/rptAdvertiserSubListNew.json?attribution=click&startDate=2022-06-27&endDate=2022-07-26&effectConversionCycle=30&trafficType=%5B1%2C2%2C4%2C5%5D&productId=101005202&t=1658914885851&csrfID=165891103300308409542458425027917&_bx-v=1.1.20'
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': cookie,
            'origin': 'https://branding.taobao.com',
            'referer': 'https://branding.taobao.com/index.action',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        response = requests.get(url=url, headers=headers)
        print(response.text)
        data_info = response.json()['data']['rptQueryResp']['rptDataDaily']
        print(data_info)
        for i in data_info:
            print(i)
            try:
                thedate = i['thedate']  # 日期
                requestCnt = i['requestCnt']  # 搜索量
                requestUvHllc = i['requestUvHllc']  # 搜索访客数
                try:
                    impression = i['impression']  # 展现量
                except:
                    impression = None
                try:
                    cpc = i['cpc']/100  # 点击单价（元）
                except:
                    cpc = None
                try:
                    shopcpc = i['shopcpc']/100  # 跳转点击单价(元)
                except:
                    shopcpc = None
                try:
                    uv = i['uv']  # 触达访客数
                except:
                    uv = None
                try:
                    cpm = i['cpm']/100  # 千次展现成本（元）
                except:
                    cpm = None
                try:
                    click = i['click']  # 点击量
                except:
                    click = None
                try:
                    interactclick = i['interactclick']  # 互动点击量
                except:
                    interactclick = None
                try:
                    ctr = i['ctr']  # 点击率
                except:
                    ctr = None
                try:
                    favshoptotal = i['favshoptotal']  # 店铺收藏数
                except:
                    favshoptotal = None
                try:
                    favitemtotal = i['favitemtotal']  # 宝贝收藏数
                except:
                    favshoptotal = None
                try:
                    carttotal = i['carttotal']  # 宝贝加购数
                except:
                    carttotal = None
                try:
                    transactionshippingtotal = i['transactionshippingtotal']  # 成交笔数
                except:
                    transactionshippingtotal = None
                try:
                    transactiontotal = i['transactiontotal']/100  # 成交金额
                except:
                    transactiontotal = None
                try:
                    roi = i['roi']  # 回报率
                except:
                    roi = None
                try:
                    prepayInshopNum = i['prepayInshopNum']  # 预售成交笔数
                except:
                    prepayInshopNum = None
                try:
                    prepayInshopAmt = i['prepayInshopAmt']/100  # 预售成交金额
                except:
                    prepayInshopAmt = None
                try:
                    item_fav_uv = i['item_fav_uv']  # 宝贝收藏访客数
                except:
                    item_fav_uv = None
                try:
                    cart_uv = i['cart_uv']  # 宝贝加购访客数
                except:
                    cart_uv = None
                try:
                    searchimpression = i['searchimpression']  # 自然流量增量曝光
                except:
                    searchimpression = None
                try:
                    cost = i['cost']/100  # 消耗
                except:
                    cost = None
                try:
                    shopclick = i['shopclick']  # 跳转点击量
                except:
                    shopclick = None
                try:
                    click_uv = i['click_uv']  # 点击访客数
                except:
                    click_uv = None
                try:
                    shopctr = i['shopctr']  # 跳转点击率
                except:
                    shopctr = None
                try:
                    visitorUvHllc = i['visitorUvHllc']  # 进店访客数
                except:
                    visitorUvHllc = None
                try:
                    cpt_cvr = i['cpt_cvr']  # 转化率
                except:
                    cpt_cvr = None
                try:
                    searchtransactiontotal = i['searchtransactiontotal']/100  # 自然流量增量成交
                except:
                    searchtransactiontotal = None
                try:
                    actionUvHllc = i['actionUvHllc']  # 行动访客数
                except:
                    actionUvHllc = None
                try:
                    transaction_uv = i['transaction_uv']  # 成交访客数
                except:
                    transaction_uv = None
                try:
                    shop_fav_uv = i['shop_fav_uv']  # 店铺收藏访客数
                except:
                    shop_fav_uv = None
                try:
                    searchCarttotal = i['searchCarttotal']  # 宝贝收藏访客数
                except:
                    searchCarttotal = None
                timeArray = time.strptime(thedate, "%Y-%m-%d")
                timeStamp = int(time.mktime(timeArray))
                change_week = int((int(time.time()) - timeStamp) / 60 / 60 / 24)
                if change_week > 30:
                    change_week = 30
                try:
                    cc = uv / requestUvHllc
                except:
                    cc = None
                try:
                    aa = visitorUvHllc / uv
                except:
                    aa = None
                try:
                    bb = actionUvHllc / visitorUvHllc
                except:
                    bb = None
                try:
                    dd = transaction_uv / actionUvHllc
                except:
                    dd = None
                print([change_week, thedate, requestCnt, requestUvHllc, cc, impression, searchimpression, cost, uv, cpm, cpc, shopcpc, click, shopclick, click_uv, interactclick, ctr, shopctr, visitorUvHllc, favshoptotal, favitemtotal, carttotal, actionUvHllc, shop_fav_uv, searchCarttotal, cart_uv, transactionshippingtotal, transactiontotal, roi, cpt_cvr, searchtransactiontotal, prepayInshopNum, prepayInshopAmt, transaction_uv, aa, bb, dd])
                            # 转化周期    日期       搜索量       搜索访客数       访客触达率           展现量     自然流量增量曝光 消耗 触达访客数 千次展现成本 点击单价 跳转点击单价 点击量 跳转点击量   点击访客数  互动点击量     点击率 跳转点击率 进店访客数       店铺收藏数      宝贝收藏数     宝贝加购数  行动访客数       店铺收藏访客数   宝贝收藏访客数  宝贝加购访客数 成交笔数  成交金额 回报率 转化率 自然流量增量成交 预售成交笔数 预售成交金额 成交访客数
                self.save_info([change_week, thedate, requestCnt, requestUvHllc, cc, impression, searchimpression, cost, uv, cpm, cpc, shopcpc, click, shopclick, click_uv, interactclick, ctr, shopctr, visitorUvHllc, favshoptotal, favitemtotal, carttotal, actionUvHllc, shop_fav_uv, item_fav_uv, cart_uv, transactionshippingtotal, transactiontotal, roi, cpt_cvr, searchtransactiontotal, prepayInshopNum, prepayInshopAmt, transaction_uv, aa, bb, dd])
            except Exception as e:
                print(e)
                pass

    def save_info(self, save_info):
        if save_info[0] >= 30:
            save_info[0] = 30
        self.sql_server.save_message('贝德美.dbo.品销宝_明星店铺_点击_账户', [tuple(save_info)])

    def delete_30_change(self):
        d_sql = f"delete from 贝德美.dbo.品销宝_明星店铺_点击_账户 where 转化周期<30"
        print(d_sql)
        self.sql_server.check_message(d_sql, 2)

    def getcsrftoken(self, cookie):
        url = 'https://branding.taobao.com/login/userInfo.json?r=mx_4&_bx-v=1.1.20'
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': cookie,
            'referer': 'https://branding.taobao.com/index_plus.action',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }

        response = requests.get(url=url, headers=headers).json()
        # response = response.split('_1646738316862(')[1][:-1]
        # response = demjson.decode(response)
        csrfID = response['data']['csrfID']
        return csrfID


if __name__ == '__main__':
    pxb = PinXiaoBao()
    cookie = 't=ba991419abcabe60cd3884e42a2b30f4; thw=cn; cookie2=1f9299af1907012d87ad1bdc6b31c185; _tb_token_=531317e3585e1; _samesite_flag_=true; cancelledSubSites=empty; xlly_s=1; unb=2212731641217; sn=%E8%B4%9D%E5%BE%B7%E7%BE%8E%E6%97%97%E8%88%B0%E5%BA%97%3A%E9%BE%99%E9%A3%9E; v=0; _m_h5_tk=c0f0651696f7be9bb658358dccfe52f0_1664164784815; _m_h5_tk_enc=98147579e3cc44473dd76e6a1e2e633b; sgcookie=E100SBmzOwRVvLbAXNvGf%2FHi3jfjCE7wJ7q2wz3ub70ErlZxAenrF48OxSG4upmOtoItoO4UUmw%2BP%2FYeJNtz6omS40whFWO8KOF21JL2j81rjoM%3D; uc1=cookie14=UoeyChPsK0ZV5w%3D%3D&cookie21=UtASsssmfufd; csg=8afe183c; skt=09abfd5f5d644e79; _cc_=Vq8l%2BKCLiw%3D%3D; cna=nWYbGpuKHDsCAXkEs3F2iXa2; isg=BJ-ftDsiAGf4QwRcvTZg-BFQLvMpBPOmCbepETHsI86VwL9COdaZ9hqWglC-2Mse; tfstk=cc01B-ZMmOX_KQ8cSROeQNoYgnr5ZQ17Ghwi1pRl5G99zzh1iX7zF6WmmtU4MW1..; l=eBSlN7-VTNKFSd7ABOfwourza77t7IRAguPzaNbMiOCPOq695gTOW6ujy7-pCnGVhs96R3z1UrspBeYBqIqBHo1ShXHmKYMmn'
    pxb.run_main('', cookie)
