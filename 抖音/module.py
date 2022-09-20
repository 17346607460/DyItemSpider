import time

import execjs, demjson

from CurrencyModule import *
from Setting import *


class TikTok:
    def __init__(self):
        self.date_type = {'30天': 23, '日': 2, '月': 4, '90天': 24}
        self.source_type = {1: ['直播', '短视频', '橱窗', '企业主页', '其他'], 2: ['联盟带货', '渠道账号', '官方账号', '其他'], 3: ['新客', '老客'],
                            4: ['抖音', '抖音火山版', '今日头条', '西瓜视频', '其他']}
        self.source_type_dr = {
            1: ['直播', '短视频', '橱窗', '搜索', '其他'],
            2: ['新粉丝', '老粉丝', '路人'],
            3: ['新客', '老客']
        }
        self.app_info = {1: '千川PC', 2: '小店随心推'}
        self.target = ['pay_gmv', 'pay_gmv_ratio', 'pay_user_cnt', 'pay_per_price']
        self.target_dr = ['pay_gmv', 'pay_rate', 'pay_per_price', 'actual_commission']
        self.component_type = {1: '来源构成', 2: '账号构成', 3: '新客构成', 4: '终端构成'}
        self.component_type_dr = {1: '来源构成', 2: '粉丝构成', 3: '新客构成'}
        self.campaignTypes = {1: '通投广告', 2: '搜索广告'}  # 广告类型
        self.ideaTypes = {1: '自定义创意', 2: '程序化创意'}  # 创意类型
        self.marGoals = {1: '短视频/图文带货', 2: '直播带货'}  # 营销目标
        self.promWays = {1: '极速推广', 2: '专业推广'}  # 推广方式
        self.smartBidTypes = {0: '控制成本投放', 7: '放量投放', 106: '放量投放'}  # 投放方式
        self.externalActions = {96: '商品购买', 169: '直播间成交', 171: '进入直播间', 172: '直播间下单', 269: '粉丝提升', 270: '内容种草'}  # 转化目标
        self._sql_server = SqlServerConnect()

    def _get_all_user_info(self, cookie):
        url = 'https://qianchuan.jinritemai.com/ad/ecom/marketing/api/v1/user/user_list'
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cookie': cookie,
            'Host': 'qianchuan.jinritemai.com',
            'Pragma': 'no-cache',
            'Referer': 'https://qianchuan.jinritemai.com/report/live?aavid=1696543798927432',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'X-CSRFToken': 'MlFg8nMPIRD0UGvZFhZVkxzM'
        }
        params = {
            'page': '1',
            'limit': '100',
            'aavid': '1696543798927432',
            'gfversion': '1.0.0.4956'
        }
        response = requests.get(url=url, headers=headers, params=params, verify=False)
        print(response.text)
        response = response.json()['data']['userAccountInfos']
        ids = []
        for i in response:
            # print(i['id'])
            ids.append(i['id'])
        if len(ids) != 13:
            raise '账户数量不对'
        return ids

    # 抖音计划报表
    def plan_report_form_main(self, cookie, start_day, end_day):
        if not start_day:
            start_day = self._sql_server.get_start_day('贝德美.DDGF.巨量千川_基础报表_计划', '日期', '')
            if start_day == get_before_day(get_today()):
                print('今天数据已经抓取完毕')
                return 0
            start_day = get_after_day(start_day)
        if not end_day:
            end_day = get_before_day(get_today())
        user_ids = self._get_all_user_info(cookie)
        print(user_ids)
        while True:
            statCosts = 0
            values = []
            for user_id in user_ids:
                res = {'直播带货': 1, '短视频/图文带货': 1}
                page = 1
                while True:
                    if res['直播带货'] == 0 and res['短视频/图文带货'] == 0:
                        break
                    # 直播-计划data 视频-计划data
                    datas = {
                        '直播带货': {"orderBy": [{"type": 2, "field": "stat_cost"}], "rangeFilter": {},
                                 "adFilter": {"pricingCategory": 2, "app": 0, "marGoal": 2, "externalAction": [],
                                              "optimizeGoal": []},
                                 "creativeFilter": {"app": 0, "marGoal": 2}, "listType": 1, "startTime": start_day,
                                 "endTime": start_day, "pageParams": {"page": page, "pageSize": 50},
                                 "metrics": ["mar_goal", "aweme_user_info", "promway", "external_action", "app",
                                             "campaign_type",
                                             "manage_type", "smart_bid_type", "deep_external_action", "stat_cost",
                                             "ctr",
                                             "show_cnt",
                                             "click_cnt", "convert_cnt", "convert_cost", "convert_rate",
                                             "all_order_create_roi_7days",
                                             "all_order_pay_roi_7days", "pay_order_count", "prepay_and_pay_order_roi",
                                             "create_order_amount", "pay_order_amount", "create_order_count",
                                             "create_order_roi",
                                             "prepay_order_count", "create_order_coupon_amount", "prepay_order_amount",
                                             "pay_order_coupon_amount", "indirect_order_create_count_7days",
                                             "indirect_order_pay_count_7days", "indirect_order_prepay_count_7days",
                                             "indirect_order_create_gmv_7days", "indirect_order_pay_gmv_7days",
                                             "indirect_order_prepay_gmv_7days", "dy_follow",
                                             "live_watch_one_minute_count",
                                             "luban_live_slidecart_click_cnt", "luban_live_comment_cnt",
                                             "luban_live_enter_cnt",
                                             "live_fans_club_join_cnt", "luban_live_click_product_cnt",
                                             "luban_live_share_cnt",
                                             "luban_live_gift_amount", "luban_live_gift_cnt", "dy_share", "dy_like",
                                             "play_duration_3s",
                                             "play_50_feed_break", "play_over", "play_over_rate", "play_75_feed_break",
                                             "play_25_feed_break", "total_play", "dy_comment",
                                             "qianchuan_first_order_cnt",
                                             "qianchuan_first_order_convert_cost",
                                             "qianchuan_first_order_direct_pay_order_roi",
                                             "qianchuan_first_order_rate", "qianchuan_first_order_direct_pay_gmv",
                                             "qianchuan_first_order_ltv30", "qianchuan_first_order_roi30"],
                                 "timeDimension": "stat_time_day", "aavid": f"{user_id}"},
                        '短视频/图文带货': {"orderBy": [{"type": 2, "field": "stat_cost"}], "rangeFilter": {},
                                     "adFilter": {"pricingCategory": 2, "app": 0, "marGoal": 1, "externalAction": [],
                                                  "optimizeGoal": []},
                                     "creativeFilter": {"app": 0, "marGoal": 1}, "listType": 1, "startTime": start_day,
                                     "endTime": start_day, "pageParams": {"page": page, "pageSize": 50},
                                     "metrics": ["manage_type", "mar_goal", "aweme_user_info", "app", "external_action",
                                                 "promway",
                                                 "campaign_type", "all_order_pay_roi_7days",
                                                 "indirect_order_pay_gmv_7days",
                                                 "goods_info",
                                                 "smart_bid_type", "deep_external_action", "stat_cost", "ctr",
                                                 "click_cnt",
                                                 "convert_rate",
                                                 "convert_cost", "convert_cnt", "cpm", "show_cnt",
                                                 "all_order_create_roi_7days",
                                                 "pay_order_count", "prepay_and_pay_order_roi", "create_order_count",
                                                 "pay_order_amount",
                                                 "create_order_roi", "create_order_amount", "prepay_order_count",
                                                 "prepay_order_amount",
                                                 "indirect_order_create_count_7days", "indirect_order_create_gmv_7days",
                                                 "indirect_order_pay_count_7days", "indirect_order_prepay_count_7days",
                                                 "indirect_order_prepay_gmv_7days", "dy_follow",
                                                 "live_watch_one_minute_count",
                                                 "luban_live_enter_cnt", "live_fans_club_join_cnt",
                                                 "luban_live_slidecart_click_cnt",
                                                 "luban_live_click_product_cnt", "luban_live_comment_cnt",
                                                 "luban_live_share_cnt",
                                                 "luban_live_gift_cnt", "luban_live_gift_amount", "dy_share", "dy_like",
                                                 "play_duration_3s",
                                                 "play_50_feed_break", "play_over", "play_over_rate",
                                                 "play_75_feed_break",
                                                 "play_25_feed_break", "total_play", "dy_comment",
                                                 "create_order_coupon_amount",
                                                 "pay_order_coupon_amount", "qianchuan_first_order_cnt",
                                                 "qianchuan_first_order_convert_cost",
                                                 "qianchuan_first_order_direct_pay_order_roi",
                                                 "qianchuan_first_order_roi30", "qianchuan_first_order_ltv30",
                                                 "qianchuan_first_order_direct_pay_gmv", "qianchuan_first_order_rate"],
                                     "timeDimension": "stat_time_day", "aavid": f"{user_id}"}
                    }
                    for data in datas:
                        if not res[data]:
                            continue
                        response = self.report_requests(user_id, datas[data], cookie)
                        print(response)
                        if not response['data']['objStatsMap']:
                            res[data] = 0
                            continue
                        data_infos = response['data']["adInfos"]
                        user_infos = response['data']["adUserInfoMap"]
                        msg_infos = response['data']["objStatsMap"]
                        for data_info in data_infos:
                            marGoal = self.marGoals[int(data_info['marGoal'])]
                            promWay = self.promWays[int(data_info['promWay'])]
                            smartBidType = self.smartBidTypes[int(data_info['smartBidType'])]
                            try:
                                externalAction = self.externalActions[int(data_info['externalAction'])]
                            except:
                                externalAction = None
                            campaignType = self.campaignTypes[int(data_info['campaignType'])]
                            jh_id = data_info['id']  # 计划id
                            app = data_info['app']
                            pt = self.app_info[app]  # 平台
                            jh_name = data_info['name']  # 计划名称
                            dy_id = user_infos[data_info['id']][0]['uniqueId']  # 抖音号id
                            if not dy_id:
                                dy_id = user_infos[data_info['id']][0]['shortId']  # 抖音号id
                            dy_name = user_infos[data_info['id']][0]['name']  # 抖音号名称
                            statCost = float(msg_infos[jh_id]['metrics']['statCost']['value']) / 100000  #
                            if not statCost:
                                res[data] = 0
                                continue
                            print(statCost, user_id, page, data)
                            statCosts = float(statCosts) + statCost
                            showCnt = float(msg_infos[jh_id]['metrics']['showCnt']['value'])  # 展示次数
                            clickCnt = float(msg_infos[jh_id]['metrics']['clickCnt']['value'])  # 点击次数
                            convertCnt = float(msg_infos[jh_id]['metrics']['convertCnt']['value'])  # 转化数
                            convertCost = float(msg_infos[jh_id]['metrics']['convertCost']['value']) / 100000  # 转化成本
                            allOrderPayRoi7Days = float(
                                msg_infos[jh_id]['metrics']['allOrderPayRoi7Days']['value'])  # 总支付ROI
                            allOrderCreateRoi7Days = float(
                                msg_infos[jh_id]['metrics']['allOrderCreateRoi7Days']['value'])  # 总下单ROI
                            payOrderCount = float(msg_infos[jh_id]['metrics']['payOrderCount']['value'])  # 成交订单数
                            payOrderAmount = float(
                                msg_infos[jh_id]['metrics']['payOrderAmount']['value']) / 100000  # 支付金额
                            createOrderCount = float(msg_infos[jh_id]['metrics']['createOrderCount']['value'])  # 下单订单数
                            createOrderAmount = float(
                                msg_infos[jh_id]['metrics']['createOrderAmount']['value']) / 100000  # 下单订单金额
                            prepayOrderCount = float(msg_infos[jh_id]['metrics']['prepayOrderCount']['value'])  # 预售订单数
                            prepayOrderAmount = float(
                                msg_infos[jh_id]['metrics']['prepayOrderAmount']['value']) / 100000  # 预售订单金额
                            indirectOrderCreateCount7Days = \
                                msg_infos[jh_id]['metrics']['indirectOrderCreateCount7Days'][
                                    'value']  # 间接下单订单数
                            indirectOrderCreateGmv7Days = float(
                                msg_infos[jh_id]['metrics']['indirectOrderCreateGmv7Days']['value']) / 100000  # 间接下单金额
                            indirectOrderPayCount7Days = msg_infos[jh_id]['metrics']['indirectOrderPayCount7Days'][
                                'value']  # 间接成交订单数
                            indirectOrderPayGmv7Days = float(
                                msg_infos[jh_id]['metrics']['indirectOrderPayGmv7Days']['value']) / 100000  # 间接成交金额

                            dyFollow = float(msg_infos[jh_id]['metrics']['dyFollow']['value'])  # 新增粉丝数
                            lubanLiveEnterCnt = float(
                                msg_infos[jh_id]['metrics']['lubanLiveEnterCnt']['value'])  # 直播间观看人次
                            liveWatchOneMinuteCount = float(
                                msg_infos[jh_id]['metrics']['liveWatchOneMinuteCount']['value'])  # 直播间超过1分钟观看人次
                            liveFansClubJoinCnt = float(
                                msg_infos[jh_id]['metrics']['liveFansClubJoinCnt']['value'])  # 直播间新加团人次
                            lubanLiveSlidecartClickCnt = float(
                                msg_infos[jh_id]['metrics']['lubanLiveSlidecartClickCnt']['value'])  # 直播间查看购物车次数
                            lubanLiveClickProductCnt = float(
                                msg_infos[jh_id]['metrics']['lubanLiveClickProductCnt']['value'])  # 直播间商品点击次数
                            lubanLiveShareCnt = float(
                                msg_infos[jh_id]['metrics']['lubanLiveShareCnt']['value'])  # 直播间分享次数
                            lubanLiveGiftCnt = float(
                                msg_infos[jh_id]['metrics']['lubanLiveGiftCnt']['value'])  # 直播间打赏次数
                            lubanLiveGiftAmount = float(
                                msg_infos[jh_id]['metrics']['lubanLiveGiftAmount']['value'])  # 直播间音浪
                            dyShare = float(msg_infos[jh_id]['metrics']['dyShare']['value'])  # 分享次数
                            lubanLiveCommentCnt = float(
                                msg_infos[jh_id]['metrics']['lubanLiveCommentCnt']['value'])  # 直播间评论次数
                            dyComment = float(msg_infos[jh_id]['metrics']['dyComment']['value'])  # 评论次数
                            dyLike = float(msg_infos[jh_id]['metrics']['dyLike']['value'])  # 点赞次数
                            totalPlay = float(msg_infos[jh_id]['metrics']['totalPlay']['value'])  # 播放数
                            playDuration3S = float(msg_infos[jh_id]['metrics']['playDuration3S']['value'])  # 3秒播放数
                            play25FeedBreak = float(msg_infos[jh_id]['metrics']['play25FeedBreak']['value'])  # 25%进度播放数
                            play50FeedBreak = float(msg_infos[jh_id]['metrics']['play50FeedBreak']['value'])  # 50%进度播放数
                            play75FeedBreak = float(msg_infos[jh_id]['metrics']['play75FeedBreak']['value'])  # 75%进度播放数
                            playOver = float(msg_infos[jh_id]['metrics']['playOver']['value'])  # 播放完成数
                            try:
                                bfwcl = (playOver / totalPlay) * 100  # 播放完成率
                            except:
                                bfwcl = 0
                            try:
                                djl = int((clickCnt / showCnt) * 100000) / 1000  # 点击率
                            except:
                                djl = 0
                            try:
                                qczsfy = int((statCost / showCnt) * 100000) / 100  # 平均前次展示费用
                            except:
                                qczsfy = 0
                            try:
                                zhl = int((convertCnt / clickCnt) * 10000) / 100  # 转化率
                            except:
                                zhl = 0
                            try:
                                zfroi = int((payOrderAmount / statCost) * 100) / 100  # 支付roi
                            except:
                                zfroi = 0
                            try:
                                xdroi = int((createOrderAmount / statCost) * 100) / 100  # 下单roi
                            except:
                                xdroi = 0
                            if data != '直播带货':
                                shop_infos = response['data']["adGoodsMap"]
                                shop_id = shop_infos[jh_id][0]['id']
                                shop_name = shop_infos[jh_id][0]['name']
                            else:
                                shop_id = None  # 商品id
                                shop_name = None  # 商品名称
                            qianchuanFirstOrderCnt = msg_infos[jh_id]['metrics']['qianchuanFirstOrderCnt'][
                                'value']  # 首单新客人数
                            qianchuanFirstOrderConvertCost = float(
                                msg_infos[jh_id]['metrics']['qianchuanFirstOrderConvertCost'][
                                    'value']) / 100000  # 首单新客转化成本
                            qianchuanFirstOrderDirectPayOrderRoi = \
                                msg_infos[jh_id]['metrics']['qianchuanFirstOrderDirectPayOrderRoi'][
                                    'value']  # 首单新客直接支付roi
                            qianchuanFirstOrderLtv30 = float(
                                msg_infos[jh_id]['metrics']['qianchuanFirstOrderLtv30']['value']) / 100000  # 新客30天累计
                            qianchuanFirstOrderDirectPayGmv = float(
                                msg_infos[jh_id]['metrics']['qianchuanFirstOrderDirectPayGmv'][
                                    'value']) / 100000  # 首单新客直接成交金额
                            qianchuanFirstOrderRate = float(
                                msg_infos[jh_id]['metrics']['qianchuanFirstOrderRate']['value']) / 100  # 首单新客订单占比
                            qianchuanFirstOrderRoi30 = msg_infos[jh_id]['metrics']['qianchuanFirstOrderRoi30'][
                                'value']  # 首单直接占比
                            b = [statCost, showCnt, djl,
                                 qczsfy, clickCnt, convertCnt, zhl, convertCost, allOrderCreateRoi7Days,
                                 allOrderPayRoi7Days,
                                 payOrderCount, payOrderAmount, zfroi,
                                 createOrderCount, createOrderAmount, xdroi, prepayOrderCount, pt, prepayOrderAmount,
                                 indirectOrderCreateCount7Days, indirectOrderCreateGmv7Days, indirectOrderPayCount7Days,
                                 indirectOrderPayGmv7Days, None, None, dyFollow,
                                 lubanLiveEnterCnt, liveWatchOneMinuteCount, liveFansClubJoinCnt,
                                 lubanLiveSlidecartClickCnt,
                                 lubanLiveClickProductCnt, lubanLiveCommentCnt, lubanLiveShareCnt, lubanLiveGiftCnt,
                                 lubanLiveGiftAmount, dyShare, dyComment, dyLike, totalPlay, playDuration3S,
                                 play25FeedBreak,
                                 play50FeedBreak, play75FeedBreak, playOver, bfwcl, qianchuanFirstOrderCnt,
                                 qianchuanFirstOrderRate, qianchuanFirstOrderConvertCost,
                                 qianchuanFirstOrderDirectPayGmv, qianchuanFirstOrderDirectPayOrderRoi,
                                 qianchuanFirstOrderLtv30, qianchuanFirstOrderRoi30]
                            result = 0
                            for i in b:
                                if i:
                                    result = 1
                                    continue
                            if result:
                                info = (
                                    start_day, user_id, jh_id, jh_name, marGoal, campaignType, dy_id, dy_name, '非托管计划',
                                    shop_id,
                                    shop_name, promWay, smartBidType, externalAction, externalAction, pt, statCost,
                                    showCnt,
                                    djl,
                                    qczsfy, clickCnt, convertCnt, zhl, convertCost, allOrderCreateRoi7Days,
                                    allOrderPayRoi7Days,
                                    payOrderCount, payOrderAmount, zfroi,
                                    createOrderCount, createOrderAmount, xdroi, prepayOrderCount, prepayOrderAmount,
                                    indirectOrderCreateCount7Days, indirectOrderCreateGmv7Days,
                                    indirectOrderPayCount7Days,
                                    indirectOrderPayGmv7Days, None, None, dyFollow,
                                    lubanLiveEnterCnt, liveWatchOneMinuteCount, liveFansClubJoinCnt,
                                    lubanLiveSlidecartClickCnt,
                                    lubanLiveClickProductCnt, lubanLiveCommentCnt, lubanLiveShareCnt, lubanLiveGiftCnt,
                                    lubanLiveGiftAmount, dyShare, dyComment, dyLike, totalPlay, playDuration3S,
                                    play25FeedBreak,
                                    play50FeedBreak, play75FeedBreak, playOver, bfwcl, qianchuanFirstOrderCnt,
                                    qianchuanFirstOrderRate, qianchuanFirstOrderConvertCost,
                                    qianchuanFirstOrderDirectPayGmv, qianchuanFirstOrderDirectPayOrderRoi,
                                    qianchuanFirstOrderLtv30, qianchuanFirstOrderRoi30)
                                # print(info)
                                values.append(info)
                            else:
                                print(jh_id)
                        time.sleep(0.5)
                    page += 1
            # check_statcosts = self.check_statCosts(start_day)
            # print(statCosts, check_statcosts)
            # if abs(statCosts-check_statcosts) < 5:
            self._sql_server.save_message('贝德美.DDGF.巨量千川_基础报表_计划', values)
            # else:
            #     raise '数据不对'
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)

    def check_statCosts(self, start_day):
        url = 'https://business.oceanengine.com/platform/api/v1/bp/statistics/promote/ecp/bidding/advertiser/stats_list/?_signature=WjtBAQAAAAAC-fEbFy2Mw1o7QRAADk6'
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-length': '487',
            'content-type': 'application/json;charset=UTF-8',
            'cookie': jlzh_cookie,
            'origin': 'https://business.oceanengine.com',
            'pragma': 'no-cache',
            'referer': 'https://business.oceanengine.com/site/promotion?',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'x-csrftoken': 'wZf5X38_j1qkLb7DuuIprlqP',
            'x-sessionid': '5ca3bdfb-441a-42e3-9d4f-289f6aa5eda7'
        }
        data = {"start_time": f"{start_day} 00:00:00", "end_time": f"{get_after_day(start_day)} 00:00:00", "page": 1,
                "limit": 10,
                "order_type": 1, "order_field": "stat_cost",
                "stats_fields": ["stat_cost", "show_cnt", "ctr", "conversion_rate", "cpm_platform", "click_cnt",
                                 "convert_cnt", "conversion_cost"],
                "cascade_fields": ["advertiser_remark", "advertiser_status", "advertiser_budget", "quota_info",
                                   "ecp_advertiser_bidding_balance", "ecp_advertiser_bidding_valid_balance",
                                   "account_tag", "advertiser_role", "group_id"], "filter": {"advertiser": {}}}
        response = requests.post(url=url, headers=headers, json=data)
        print(response.text)
        response = response.json()
        stat_cost = float(response['data']['total_metrics']['stat_cost'])
        # print(stat_cost)
        # url = 'https://business.oceanengine.com/platform/api/v1/bp/statistics/promote/ecp/brand/advertiser/stats_list/?_signature=WjtBAQAAAAAC-fEbFy0gQlo7QRAADk6'
        # data = {"start_time": f"{start_day} 00:00:00", "end_time": f"{get_after_day(start_day)} 00:00:00", "page": 1, "limit": 10,
        #         "order_type": 1, "order_field": "stat_cost",
        #         "stats_fields": ["stat_cost", "show_cnt", "ctr", "conversion_rate", "brand_pay_order_count",
        #                          "brand_prepay_and_pay_order_roi", "stat_brand_pay_order_amount", "valid_play",
        #                          "average_play_time_per_play"],
        #         "cascade_fields": ["advertiser_remark", "advertiser_status", "ecp_advertiser_brand_balance",
        #                            "ecp_advertiser_brand_valid_balance", "account_tag", "advertiser_role", "group_id"],
        #         "filter": {"advertiser": {}}}
        # response = requests.post(url=url, headers=headers, json=data).json()
        # stat_cost += float(response['data']['total_metrics']['stat_cost'])
        # print(stat_cost)
        return stat_cost

    def report_requests(self, user_id, data, cookie):
        '''
        计划报表的请求函数
        :param user_id: 账户id
        :param data: requests data信息
        :param cookie:
        :return:
        '''
        # url = f'https://qianchuan.jinritemai.com/ad/ecom/marketing/api/v2/report/getDataReportList?aavid={user_id}&gfversion=1.0.0.4153'
        while True:
            url = f'https://qianchuan.jinritemai.com/ad/marketing/data/api/v1/report/list?aavid={user_id}&gfversion=1.0.0.8149'
            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Content-Length': '1048',
                'Content-Type': 'application/json;charset=UTF-8',
                'Cookie': cookie,
                'Host': 'qianchuan.jinritemai.com',
                'Origin': 'https://qianchuan.jinritemai.com',
                'Pragma': 'no-cache',
                'Referer': 'https://qianchuan.jinritemai.com/report/live?aavid=1696543798927432',
                'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': "Windows",
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
                'X-CSRFToken': [a.split('=')[1] for a in cookie.split('; ') if a.split('=')[0] == 'csrftoken'][0]
            }
            response = requests.post(url=url, headers=headers, json=data)
            print(response.text, 111111111111111111111111111111111111111111111)
            if response.text:
                break
            else:
                time.sleep(3)
        return response.json()


    # 抖音创意报表
    def create_idea_report_main(self, cookie, start_day, end_day):
        if not start_day:
            start_day = self._sql_server.get_start_day('贝德美.DDGF.巨量千川_基础报表_创意', '日期', '')
            if start_day == get_before_day(get_today()):
                print('今天数据已经抓取完毕')
                return 0
            start_day = get_after_day(start_day)
        if not end_day:
            end_day = get_before_day(get_today())
        user_ids = self._get_all_user_info(cookie)
        print(user_ids)
        while True:
            values = []
            for user_id in user_ids:
                res = {'直播带货': 1, '短视频/图文带货': 1}
                page = 1
                while True:
                    if res['直播带货'] == 0 and res['短视频/图文带货'] == 0:
                        break
                    # 直播-计划data 视频-计划data
                    datas = {
                        '直播带货': {"orderBy": [{"type": 2, "field": "stat_cost"}], "rangeFilter": {},
                                 "adFilter": {"pricingCategory": 2, "app": 0, "marGoal": 2, "externalAction": [],
                                              "optimizeGoal": []}, "creativeFilter": {"app": 0, "marGoal": 2},
                                 "listType": 3, "startTime": f"{start_day}", "endTime": f"{start_day}",
                                 "pageParams": {"page": page, "pageSize": 50},
                                 "metrics": ["ad_name", "image_mode", "stat_cost", "pay_order_count",
                                             "pay_order_amount", "prepay_and_pay_order_roi", "show_cnt", "click_cnt",
                                             "ctr", "cpm", "creative_type", "campaign_type", "convert_rate",
                                             "convert_cost", "convert_cnt", "create_order_count", "create_order_roi",
                                             "prepay_order_amount", "prepay_order_count", "create_order_amount",
                                             "luban_live_enter_cnt", "live_fans_club_join_cnt",
                                             "luban_live_click_product_cnt", "luban_live_share_cnt",
                                             "luban_live_gift_amount", "dy_comment", "total_play", "dy_like",
                                             "dy_share", "luban_live_gift_cnt", "luban_live_comment_cnt",
                                             "luban_live_slidecart_click_cnt", "live_watch_one_minute_count",
                                             "dy_follow", "play_25_feed_break", "play_75_feed_break", "play_over_rate",
                                             "play_over", "play_50_feed_break", "play_duration_3s", "app",
                                             "qianchuan_first_order_cnt", "qianchuan_first_order_rate",
                                             "qianchuan_first_order_convert_cost",
                                             "qianchuan_first_order_direct_pay_gmv",
                                             "qianchuan_first_order_direct_pay_order_roi",
                                             "qianchuan_first_order_ltv30", "qianchuan_first_order_roi30",
                                             "create_order_coupon_amount", "pay_order_coupon_amount",
                                             "indirect_order_create_count_7days", "indirect_order_create_gmv_7days",
                                             "indirect_order_pay_count_7days", "indirect_order_pay_gmv_7days",
                                             "indirect_order_prepay_gmv_7days", "indirect_order_prepay_count_7days",
                                             "all_order_create_roi_7days", "all_order_pay_roi_7days"],
                                 "timeDimension": "stat_time_day", "aavid": f"{user_id}"},
                        '短视频/图文带货': {"orderBy": [{"type": 2, "field": "stat_cost"}], "rangeFilter": {},
                                     "adFilter": {"pricingCategory": 2, "app": 0, "marGoal": 1, "externalAction": [],
                                                  "optimizeGoal": []}, "creativeFilter": {"app": 0, "marGoal": 1},
                                     "listType": 3, "startTime": f"{start_day}", "endTime": f"{start_day}",
                                     "pageParams": {"page": page, "pageSize": 50},
                                     "metrics": ["ad_name", "image_mode", "stat_cost", "pay_order_count",
                                                 "pay_order_amount", "prepay_and_pay_order_roi", "show_cnt",
                                                 "click_cnt", "ctr", "cpm", "luban_live_enter_cnt",
                                                 "live_fans_club_join_cnt", "dy_follow", "live_watch_one_minute_count",
                                                 "luban_live_slidecart_click_cnt", "luban_live_comment_cnt",
                                                 "luban_live_gift_cnt", "dy_share", "dy_like", "play_duration_3s",
                                                 "play_50_feed_break", "play_over_rate", "play_75_feed_break",
                                                 "play_over", "total_play", "play_25_feed_break", "dy_comment",
                                                 "luban_live_share_cnt", "luban_live_click_product_cnt",
                                                 "luban_live_gift_amount", "prepay_order_amount", "create_order_roi",
                                                 "create_order_count", "prepay_order_count", "create_order_amount",
                                                 "convert_cost", "convert_rate", "convert_cnt", "creative_type",
                                                 "campaign_type", "app", "all_order_create_roi_7days",
                                                 "all_order_pay_roi_7days", "create_order_coupon_amount",
                                                 "pay_order_coupon_amount", "indirect_order_create_count_7days",
                                                 "indirect_order_create_gmv_7days", "indirect_order_pay_count_7days",
                                                 "indirect_order_pay_gmv_7days", "indirect_order_prepay_gmv_7days",
                                                 "indirect_order_prepay_count_7days", "qianchuan_first_order_cnt",
                                                 "qianchuan_first_order_rate", "qianchuan_first_order_direct_pay_gmv",
                                                 "qianchuan_first_order_convert_cost",
                                                 "qianchuan_first_order_direct_pay_order_roi",
                                                 "qianchuan_first_order_ltv30", "qianchuan_first_order_roi30"],
                                     "timeDimension": "stat_time_day", "aavid": f"{user_id}"}
                    }
                    for data in datas:
                        if not res[data]:
                            continue
                        response = self.report_requests(user_id, datas[data], cookie)
                        if not response['data']['objStatsMap']:
                            res[data] = 0
                            continue
                        video_infos = response['data']['creativeInfos']
                        objStatsMap = response['data']['objStatsMap']
                        for video_info in video_infos:
                            try:
                                video_id = video_info['videoMaterial'][0]['videoId']
                                item_id = video_info['videoMaterial'][0]['awemeItemId']
                            except:
                                video_id = None
                                item_id = None
                            if video_id:
                                imageMode = '竖版视频'  # 素材样式
                            else:
                                imageMode = '直播间画面'  # 素材样式
                            cy_id = video_info['id']  # 创意id
                            creativeName = video_info['creativeName']  # 创意名称
                            campaignType = self.campaignTypes[video_info['campaignType']]  # 广告类型
                            adName = video_info['adName']  # 所属计划
                            adId = video_info['adId']  # 所属计划id
                            app = video_info['app']
                            pt = self.app_info[app]  # 平台
                            ideaType = self.ideaTypes[1]  # 创意类型
                            statCost = float(objStatsMap[cy_id]['metrics']['statCost']['value']) / 100000  # 消耗
                            showCnt = float(objStatsMap[cy_id]['metrics']['showCnt']['value'])  # 展示次数
                            clickCnt = float(objStatsMap[cy_id]['metrics']['clickCnt']['value'])  # 点击次数
                            convertCnt = float(objStatsMap[cy_id]['metrics']['convertCnt']['value'])  # 转化数
                            convertCost = float(objStatsMap[cy_id]['metrics']['convertCost']['value']) / 100000  # 转化成本
                            payOrderCount = float(objStatsMap[cy_id]['metrics']['payOrderCount']['value'])  # 成交订单数
                            payOrderAmount = float(
                                objStatsMap[cy_id]['metrics']['payOrderAmount']['value']) / 100000  # 支付金额
                            createOrderCount = float(
                                objStatsMap[cy_id]['metrics']['createOrderCount']['value'])  # 下单订单数
                            createOrderAmount = float(
                                objStatsMap[cy_id]['metrics']['createOrderAmount']['value']) / 100000  # 下单订单金额
                            prepayOrderCount = float(
                                objStatsMap[cy_id]['metrics']['prepayOrderCount']['value'])  # 预售订单数
                            prepayOrderAmount = float(
                                objStatsMap[cy_id]['metrics']['prepayOrderAmount']['value']) / 100000  # 预售订单金额
                            dyFollow = float(objStatsMap[cy_id]['metrics']['dyFollow']['value'])  # 新增粉丝数
                            lubanLiveEnterCnt = float(
                                objStatsMap[cy_id]['metrics']['lubanLiveEnterCnt']['value'])  # 直播间观看人次
                            liveWatchOneMinuteCount = float(
                                objStatsMap[cy_id]['metrics']['liveWatchOneMinuteCount']['value'])  # 直播间超过1分钟观看人次
                            liveFansClubJoinCnt = float(
                                objStatsMap[cy_id]['metrics']['liveFansClubJoinCnt']['value'])  # 直播间新加团人次
                            lubanLiveSlidecartClickCnt = float(
                                objStatsMap[cy_id]['metrics']['lubanLiveSlidecartClickCnt']['value'])  # 直播间查看购物车次数
                            lubanLiveClickProductCnt = float(
                                objStatsMap[cy_id]['metrics']['lubanLiveClickProductCnt']['value'])  # 直播间商品点击次数
                            lubanLiveShareCnt = float(
                                objStatsMap[cy_id]['metrics']['lubanLiveShareCnt']['value'])  # 直播间分享次数
                            lubanLiveGiftCnt = float(
                                objStatsMap[cy_id]['metrics']['lubanLiveGiftCnt']['value'])  # 直播间打赏次数
                            lubanLiveGiftAmount = float(
                                objStatsMap[cy_id]['metrics']['lubanLiveGiftAmount']['value'])  # 直播间音浪
                            dyShare = float(objStatsMap[cy_id]['metrics']['dyShare']['value'])  # 分享次数
                            lubanLiveCommentCnt = float(
                                objStatsMap[cy_id]['metrics']['lubanLiveCommentCnt']['value'])  # 直播间评论次数
                            dyComment = float(objStatsMap[cy_id]['metrics']['dyComment']['value'])  # 评论次数
                            dyLike = float(objStatsMap[cy_id]['metrics']['dyLike']['value'])  # 点赞次数
                            totalPlay = float(objStatsMap[cy_id]['metrics']['totalPlay']['value'])  # 播放数
                            playDuration3S = float(objStatsMap[cy_id]['metrics']['playDuration3S']['value'])  # 3秒播放数
                            play25FeedBreak = float(
                                objStatsMap[cy_id]['metrics']['play25FeedBreak']['value'])  # 25%进度播放数
                            play50FeedBreak = float(
                                objStatsMap[cy_id]['metrics']['play50FeedBreak']['value'])  # 50%进度播放数
                            play75FeedBreak = float(
                                objStatsMap[cy_id]['metrics']['play75FeedBreak']['value'])  # 75%进度播放数
                            playOver = float(objStatsMap[cy_id]['metrics']['playOver']['value'])  # 播放完成数
                            bfwcl = int((playOver / totalPlay) * 1000000) / 10000 if totalPlay != 0 else 0
                            djl = int((clickCnt / showCnt) * 100000) / 1000 if showCnt != 0 else 0
                            qczsfy = int((statCost / showCnt) * 100000) / 100 if showCnt != 0 else 0
                            zhl = int((convertCnt / clickCnt) * 10000) / 100 if clickCnt != 0 else 0
                            zfroi = int((payOrderAmount / statCost) * 100) / 100 if statCost != 0 else 0
                            xdroi = int((createOrderAmount / statCost) * 100) / 100 if statCost != 0 else 0
                            qianchuanFirstOrderCnt = objStatsMap[cy_id]['metrics']['qianchuanFirstOrderCnt'][
                                'value']  # 首单新客人数
                            qianchuanFirstOrderConvertCost = float(
                                objStatsMap[cy_id]['metrics']['qianchuanFirstOrderConvertCost'][
                                    'value']) / 100000  # 首单新客转化成本
                            qianchuanFirstOrderDirectPayOrderRoi = \
                                objStatsMap[cy_id]['metrics']['qianchuanFirstOrderDirectPayOrderRoi'][
                                    'value']  # 首单新客直接支付roi
                            qianchuanFirstOrderLtv30 = float(
                                objStatsMap[cy_id]['metrics']['qianchuanFirstOrderLtv30']['value']) / 100000  # 新客30天累计
                            qianchuanFirstOrderDirectPayGmv = float(
                                objStatsMap[cy_id]['metrics']['qianchuanFirstOrderDirectPayGmv'][
                                    'value']) / 100000  # 首单新客直接成交金额
                            qianchuanFirstOrderRate = float(
                                objStatsMap[cy_id]['metrics']['qianchuanFirstOrderRate']['value']) / 100  # 首单新客订单占比
                            qianchuanFirstOrderRoi30 = objStatsMap[cy_id]['metrics']['qianchuanFirstOrderRoi30'][
                                'value']  # 首单直接占比
                            info = (
                                start_day, user_id, data, item_id, video_id, cy_id, creativeName, campaignType, adName,
                                adId,
                                imageMode,
                                ideaType, pt, statCost,
                                showCnt, djl, qczsfy, clickCnt, convertCnt, zhl, convertCost, payOrderCount,
                                payOrderAmount, zfroi,
                                createOrderCount, createOrderAmount, xdroi, prepayOrderCount, prepayOrderAmount,
                                dyFollow,
                                lubanLiveEnterCnt, liveWatchOneMinuteCount, liveFansClubJoinCnt,
                                lubanLiveSlidecartClickCnt,
                                lubanLiveClickProductCnt, lubanLiveCommentCnt, lubanLiveShareCnt, lubanLiveGiftCnt,
                                lubanLiveGiftAmount,
                                dyShare, dyComment, dyLike, totalPlay, playDuration3S, play25FeedBreak, play50FeedBreak,
                                play75FeedBreak,
                                playOver, bfwcl, qianchuanFirstOrderCnt,
                                 qianchuanFirstOrderRate, qianchuanFirstOrderConvertCost,
                                 qianchuanFirstOrderDirectPayGmv, qianchuanFirstOrderDirectPayOrderRoi,
                                 qianchuanFirstOrderLtv30, qianchuanFirstOrderRoi30)
                            values.append(info)
                            print(info)
                        time.sleep(2)
                    page += 1
            self._sql_server.save_message('贝德美.DDGF.巨量千川_基础报表_创意', values)
            if start_day == end_day:
                break
            start_day = get_after_day(start_day)

    # 云图趋势分析
    def yuntu_trend_analysis(self, start_day, end_day, cookie):
        '''

        :return:
        '''
        categoryIds = [21255, 21256, 21257]
        if not start_day:
            start_day = self._sql_server.get_start_day('贝德美.DDGF.行业洞察_品牌市场份额_类目', '日期', '')
            if start_day == get_before_day(get_today()):
                print('今天数据已经抓取完毕')
                return 0
            start_day = get_after_day(start_day)
        if not end_day:
            end_day = get_before_day(get_today())
        try:
            with open(r'C:\Users\lianqinglongfei\Desktop\DyItemSpider\抖音\抖音云图\云图signature.js', 'r',
                      encoding='utf8') as r:
                b = r.read()
            execjs.compile(b).call('yuntu_trend_analysis', end_day, end_day,
                                   cookie)
            print('爬取完毕')
        except:
            print('爬取完毕')
        for categoryId in categoryIds:
            response = self.get_yuntu_msg(categoryId)
            print(response)
            datas = demjson.decode(response)['data']
            for data_key in datas:
                for data in datas[data_key]:
                    sql = f"select * from 贝德美.DDGF.行业洞察_品牌市场份额_类目 where 日期='{data['date']}' and 类目ID='{categoryId}'"
                    res = self._sql_server.check_message(sql, 0)
                    if res:
                        continue
                    gmvRatio = data['gmvRatio']  # 本品牌gvm
                    purchaseUidRatio = data['purchaseUidRatio']  # 本品牌占成交数占比
                    value = (data['date'], categoryId, gmvRatio, float(purchaseUidRatio))
                    self._sql_server.save_message('贝德美.DDGF.行业洞察_品牌市场份额_类目', [value])
            # time.sleep(5)

    def get_yuntu_msg(self, categoryId):
        with open(r'C:\Users\lianqinglongfei\Desktop\DyItemSpider\抖音\{}.txt'.format(categoryId), 'r',
                  encoding='utf-8') as r:
            datas = r.read()
        r.close()
        return datas

    # 星图达人价格
    # def
    #     url = 'https://www.xingtu.cn/h/api/gateway/handler_get/?platform_source=1&order_by=score&sort_type=2&search_scene=1&display_scene=1&limit=20&page=1&regular_filter=%7B%22current_tab%22:3,%22marketing_target%22:2,%22task_category%22:1%7D&attribute_filter=%7B%7D&author_pack_filter=%7B%7D&service_name=go_search.AdStarGoSearchService&service_method=SearchForStarAuthors&sign_strict=1&sign=6a574654a9323f9667d0c78c853cf152'


if __name__ == '__main__':
    # https://business.oceanengine.com/site/promotion?#/ecp/bidding/account
    jlzh_cookie = 'csrftoken=kpdHBDC_ju6HRGqY3jHVSvAH; gr_user_id=f1d2612f-352f-4a5b-b1c7-edc519055b40; grwng_uid=c37b68df-ef11-4d78-babf-ce4970f9689d; passport_csrf_token=73a82def6b3213d1ee103ae5ad894ade; passport_csrf_token_default=73a82def6b3213d1ee103ae5ad894ade; ttwid=1%7Cym8DI5mlhkCXIpJryh1wQA0iW84Y2h0TQbuHZT-UTiE%7C1662516172%7Ce6b4a6948af56d2e40edcdee61788eeaf9573cf0c05cae85c6c79d9648782775; ttcid=22fe56fa459e4b09b1fa321d295314b532; tt_scid=AkaHc7q5emk941AScsJbBHX3QZuugJQzvnfdklTmz.QMuPLyLG0Gsx4.Y6KQ4lxYdd0a; s_v_web_id=verify_l7qz7ltc_ywVaRaSt_ikbr_423o_9YJI_Efry8Jqu7FRk; _tea_utm_cache_2018=undefined; d_ticket=13f2c17c2d4f359fb9bc248b0bf6adf58ea4e; n_mh=Ea7ohvZmpq2GgYEw5hDBKPPhomLW-8LmjUonzOlwQuQ; sso_auth_status=42c117ef104f03cf465ed11702046ca8; sso_auth_status_ss=42c117ef104f03cf465ed11702046ca8; sso_uid_tt=8ef2ee5672066355c757d1661d23624a; sso_uid_tt_ss=8ef2ee5672066355c757d1661d23624a; toutiao_sso_user=be1f531ec1a0a92cf39f6b9c8ce7e433; toutiao_sso_user_ss=be1f531ec1a0a92cf39f6b9c8ce7e433; sid_ucp_sso_v1=1.0.0-KDkzNjY0ZDc3MmVlNzM4ZmE1MTA5MTA1ZmFkMmQ3ZDJhMjA2NDhhNDYKHwiU_cCF0IzOBhD099-YBhj6CiAMMIikwIoGOAJA8QcaAmxmIiBiZTFmNTMxZWMxYTBhOTJjZjM5ZjZiOWM4Y2U3ZTQzMw; ssid_ucp_sso_v1=1.0.0-KDkzNjY0ZDc3MmVlNzM4ZmE1MTA5MTA1ZmFkMmQ3ZDJhMjA2NDhhNDYKHwiU_cCF0IzOBhD099-YBhj6CiAMMIikwIoGOAJA8QcaAmxmIiBiZTFmNTMxZWMxYTBhOTJjZjM5ZjZiOWM4Y2U3ZTQzMw; msToken=b7TSvGe1zD28N7Q32V7P88VjB4ksMZg1oraS_Xj342pe7MhTKbXbxIh1UuYCkD6dNXeOYRjFG45rHIu4nhR6F-jc6XLgpaCNABrBk06ojyhF; odin_tt=1760e9b39f927218cd37f6ac5c47ef1e31f6b726d2e7d4bdf5592e0e95d3a6b3c76df1abcdf9d7eb9df18ae7b75b46e9f7f720e9ede33a3c75c63afbda27dbda; passport_auth_status=ffbf5e1461d308dc91cbfe729568e022%2C0d3e3ca5401dc2b2593ce0ab9b0a924e; passport_auth_status_ss=ffbf5e1461d308dc91cbfe729568e022%2C0d3e3ca5401dc2b2593ce0ab9b0a924e; sid_guard=498c58d37c0bbde0cc6446e1478888df%7C1662516212%7C5184000%7CSun%2C+06-Nov-2022+02%3A03%3A32+GMT; uid_tt=dd88e9f3d1a1cc60257647ba9432407e; uid_tt_ss=dd88e9f3d1a1cc60257647ba9432407e; sid_tt=498c58d37c0bbde0cc6446e1478888df; sessionid=498c58d37c0bbde0cc6446e1478888df; sessionid_ss=498c58d37c0bbde0cc6446e1478888df; sid_ucp_v1=1.0.0-KDRjNmM0NWIxZTkxNjQ4NjgzNWVkMDQ3ODM4OGNkOTAwN2E5NWVjYWIKGQiU_cCF0IzOBhD099-YBhj6CiAMOAJA8QcaAmxmIiA0OThjNThkMzdjMGJiZGUwY2M2NDQ2ZTE0Nzg4ODhkZg; ssid_ucp_v1=1.0.0-KDRjNmM0NWIxZTkxNjQ4NjgzNWVkMDQ3ODM4OGNkOTAwN2E5NWVjYWIKGQiU_cCF0IzOBhD099-YBhj6CiAMOAJA8QcaAmxmIiA0OThjNThkMzdjMGJiZGUwY2M2NDQ2ZTE0Nzg4ODhkZg; gftoken=NDk4YzU4ZDM3Y3wxNjYyNTE2MjEyNzZ8fDAGBgYGBgY; trace_log_adv_id=undefined; trace_log_user_id=3721181151641236'
    tk = TikTok()
    # https://qianchuan.jinritemai.com/data-report/bidding/live?aavid=1696543798927432
    cookie = 'BUYIN_SASID=SID2_3569868405764979738; passport_csrf_token=99733c8d819a59aca0ca5a5d122bbd85; passport_csrf_token_default=99733c8d819a59aca0ca5a5d122bbd85; ttwid=1%7C1-rC236pOlUYpqagy9o9eeSuBd_g3b0quVy0Pd5YEZg%7C1662349518%7C9e09a710b862c7ed4f202b48702a2bcb5a1f067eb5c738c484120ab8f4793fe3; d_ticket=8e4cbcf62da9790b53fded5bbb86814b0470b; n_mh=Ea7ohvZmpq2GgYEw5hDBKPPhomLW-8LmjUonzOlwQuQ; sso_auth_status=4b11158324a25369748f53d9392dea41; sso_auth_status_ss=4b11158324a25369748f53d9392dea41; sso_uid_tt=218ca897e29de567b549a5ecf24d9c08; sso_uid_tt_ss=218ca897e29de567b549a5ecf24d9c08; toutiao_sso_user=c403b6ed5bdf2a36bd0ecf00212622a6; toutiao_sso_user_ss=c403b6ed5bdf2a36bd0ecf00212622a6; sid_ucp_sso_v1=1.0.0-KDVkZjk4MDhlYjg5ZTg1OTU1N2I5MDBlMWY5MTBiN2MzYjFlODFhMDUKHwiU_cCF0IzOBhDr4dWYBhiwISAMMIikwIoGOAJA8QcaAmxmIiBjNDAzYjZlZDViZGYyYTM2YmQwZWNmMDAyMTI2MjJhNg; ssid_ucp_sso_v1=1.0.0-KDVkZjk4MDhlYjg5ZTg1OTU1N2I5MDBlMWY5MTBiN2MzYjFlODFhMDUKHwiU_cCF0IzOBhDr4dWYBhiwISAMMIikwIoGOAJA8QcaAmxmIiBjNDAzYjZlZDViZGYyYTM2YmQwZWNmMDAyMTI2MjJhNg; odin_tt=c0b3163b20ea12722725dae2980b9a61ae21753f8493063b44b95fe6d06e6691d2043093de7509beeeab95fe5ac812c43855ed585813c9f9b573e03575c5194e; passport_auth_status=5d6b80dda82c4317fc65da198073209a%2Cc4b67a6b9d755192189660b23da8ecf3; passport_auth_status_ss=5d6b80dda82c4317fc65da198073209a%2Cc4b67a6b9d755192189660b23da8ecf3; ucas_sso_c0=CkEKBTEuMC4wEJ-IkLaom9yKYxjmJiDAkvCB34zAByiwITCU_cCF0IzOBkDt4dWYBkjtlZKbBlCEvN7w9bD4p2FYbxIUrd0wVH7BbE2quX1NV-5RFG8lG6A; ucas_sso_c0_ss=CkEKBTEuMC4wEJ-IkLaom9yKYxjmJiDAkvCB34zAByiwITCU_cCF0IzOBkDt4dWYBkjtlZKbBlCEvN7w9bD4p2FYbxIUrd0wVH7BbE2quX1NV-5RFG8lG6A; ucas_c0=CkEKBTEuMC4wEIeIisz2m9yKYxjmJiDAkvCB34zAByiwITCU_cCF0IzOBkDt4dWYBkjtlZKbBlCEvN7w9bD4p2FYbxIU0nqkgCTTj4XtyCGPJWMt38LFGPM; ucas_c0_ss=CkEKBTEuMC4wEIeIisz2m9yKYxjmJiDAkvCB34zAByiwITCU_cCF0IzOBkDt4dWYBkjtlZKbBlCEvN7w9bD4p2FYbxIU0nqkgCTTj4XtyCGPJWMt38LFGPM; sid_guard=4ac7ab47bc3b3ab9c4a1c535ad13a7e2%7C1662349549%7C5184000%7CFri%2C+04-Nov-2022+03%3A45%3A49+GMT; uid_tt=fbc47ba41d689781f58498fc104e7a0f; uid_tt_ss=fbc47ba41d689781f58498fc104e7a0f; sid_tt=4ac7ab47bc3b3ab9c4a1c535ad13a7e2; sessionid=4ac7ab47bc3b3ab9c4a1c535ad13a7e2; sessionid_ss=4ac7ab47bc3b3ab9c4a1c535ad13a7e2; sid_ucp_v1=1.0.0-KDEyODliYjY5Y2MxYjFlNjczYjM0ZmIyYmI1ODM5ODI2ZGUxMDJlZDEKFwiU_cCF0IzOBhDt4dWYBhiwITgCQPEHGgJsZiIgNGFjN2FiNDdiYzNiM2FiOWM0YTFjNTM1YWQxM2E3ZTI; ssid_ucp_v1=1.0.0-KDEyODliYjY5Y2MxYjFlNjczYjM0ZmIyYmI1ODM5ODI2ZGUxMDJlZDEKFwiU_cCF0IzOBhDt4dWYBhiwITgCQPEHGgJsZiIgNGFjN2FiNDdiYzNiM2FiOWM0YTFjNTM1YWQxM2E3ZTI; PHPSESSID=2f8bf9c86a11a80c9284af137e541b0d; PHPSESSID_SS=2f8bf9c86a11a80c9284af137e541b0d; qc_tt_tag=0; ttcid=8273e9e8deb44976a6410594dab0ef2724; csrf_session_id=aff671027f78aa34ee9fbe3eec54e817; csrftoken=jsFzZGdt-WqUGQM64hUB6lu4sjkkb70E3Bcc; x-jupiter-uuid=16623499980446382; tt_scid=th8H77lsCfHzbUebKjPAQsAHtqY4Vq.vN8YGYQFzFz8s4bwnzgOthP18UqFZQ3ql651b; msToken=xijdWh_CVywDBGvWQsw1mEOligZ-XkS-kNa1lFjyrDSeRpgf4YoaQ5mvFoMM8AI_bUtAbyQqF2FOhp8fFBVndNzj0X173IRFZtxDHUsttYSw4BYEQ4W7kGzmxjJktT4=; msToken=EiZ_Z55HtRe9__PNBKQArkqHm42xTWKd8zwtjau36t-1qsgH8stPyRQdpOeYbxMx3A4MH4vgKSnrDXQqbBRdkbk7rRMNVzWfRgaE8GHQDjeTfD5hTqgJ'
    #  贝德美.DDGF.巨量千川_基础报表_计划
    tk.plan_report_form_main(cookie, '', '')
    # 贝德美.DDGF.巨量千川_基础报表_创意
    tk.create_idea_report_main(cookie, '', '')
    # 贝德美.DDGF.行业洞察_品牌市场份额_类目
    cookie = 'MONITOR_WEB_ID=d06f3fc5-ee9f-47e7-9159-53467d3c4624; ttcid=0f498bc8b9514439958949c244090bc215; tt_scid=hZJpz02r48TKtjqN3YRAQQAdmNM9pOv0lP8FnkNG4xpvOU-FZEAJoUyaSSBLVa5u8986; loginType=email; passport_csrf_token=cc7e4995e7565560745538bde553ffbf; passport_csrf_token_default=cc7e4995e7565560745538bde553ffbf; s_v_web_id=verify_l7zkjqum_ySBEUu7d_WJ9w_4e7m_8nyE_LbPTC51CEM5Y; n_mh=9-mIeuD4wZnlYrrOvfzG3MuT6aQmCUtmr8FxV8Kl8xY; sso_uid_tt=9052c06c37c2f62dea82a593962dd103; sso_uid_tt_ss=9052c06c37c2f62dea82a593962dd103; toutiao_sso_user=682bb9e4739bcfed14ee09a8483a4771; toutiao_sso_user_ss=682bb9e4739bcfed14ee09a8483a4771; sid_ucp_sso_v1=1.0.0-KGUxNWI3MmE3OThiYjI0OWUyMTkzMjQzZTVkZjdhM2JkMDQxZTUwNTkKFwjLkfC-1PSVBxDs0v-YBhjkDjgBQOsHGgJsZiIgNjgyYmI5ZTQ3MzliY2ZlZDE0ZWUwOWE4NDgzYTQ3NzE; ssid_ucp_sso_v1=1.0.0-KGUxNWI3MmE3OThiYjI0OWUyMTkzMjQzZTVkZjdhM2JkMDQxZTUwNTkKFwjLkfC-1PSVBxDs0v-YBhjkDjgBQOsHGgJsZiIgNjgyYmI5ZTQ3MzliY2ZlZDE0ZWUwOWE4NDgzYTQ3NzE; sid_guard=4d492b6b126990e8f5fe2735c932794f%7C1663035756%7C5184000%7CSat%2C+12-Nov-2022+02%3A22%3A36+GMT; uid_tt=395ea1802d31e8368ff8039826fc9482; uid_tt_ss=395ea1802d31e8368ff8039826fc9482; sid_tt=4d492b6b126990e8f5fe2735c932794f; sessionid=4d492b6b126990e8f5fe2735c932794f; sessionid_ss=4d492b6b126990e8f5fe2735c932794f; sid_ucp_v1=1.0.0-KGI2OWVjMDAzOTc5YjNiZjc5MzVmOGFmYmMyNDg4ZjUxODljM2M3MWYKFwjLkfC-1PSVBxDs0v-YBhjkDjgBQOsHGgJsZiIgNGQ0OTJiNmIxMjY5OTBlOGY1ZmUyNzM1YzkzMjc5NGY; ssid_ucp_v1=1.0.0-KGI2OWVjMDAzOTc5YjNiZjc5MzVmOGFmYmMyNDg4ZjUxODljM2M3MWYKFwjLkfC-1PSVBxDs0v-YBhjkDjgBQOsHGgJsZiIgNGQ0OTJiNmIxMjY5OTBlOGY1ZmUyNzM1YzkzMjc5NGY; msToken=JNhEHAHXc2ru6qN00c9I3FX9cvro_k-49K4j_t1VpP-Q95Dm1UQ5iPrrqteIP7Ep6Do12rckc9iHl1hHcy8598oytHqlz-KlXNqGIzVQJrWDWC3PrHje; msToken=82C0HUQ9pYrXk--FcfMAkY6rvjuj4NTS-0ICRf3RWsNvg3u7Sa7eERPaosZAybQQmIbWqKBiuDPqDiV5yZ7r1YaVXdx-nreutJ1rM2zBhUfJtlyoiYWC1bPXRFXujA=='
    tk.yuntu_trend_analysis('', '', cookie)
