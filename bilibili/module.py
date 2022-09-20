import requests
from Setting import *


class Bilibili:
    def __init__(self):
        self._sql_server = SqlServerConnect()

    # 三连推广效果总览
    def overview_of_promotion_effect_of_sanlian_main(self, start_day, end_day, cookie):
        if not start_day:
            start_day = self._sql_server.get_start_day('贝德美.dbo.bilibili_三连推广效果', '日期', '')
            if start_day == get_before_day(get_today()):
                print('今天数据已经抓取完毕')
                return 0
            start_day = start_day
        if not end_day:
            end_day = get_before_day(get_today())
        response = self.overview_of_promotion_effect_of_sanlian_request(start_day, end_day, cookie)
        datas = response['result']['rtb_data']
        values = {}
        dates = datas['xaxis']
        for index, date in enumerate(dates):
            values[date.split(' ')[0]] = []
            costs = datas['cost']  # 花费
            show_count = datas['show_count']  # 展示量
            click_count = datas['click_count']  # 点击量
            fans_increase_count = datas['fans_increase_count']  # 张粉数
            values[date.split(' ')[0]].append((date.split(' ')[0], 975433, '贝德美旗舰店-带货起飞', costs[index], show_count[index], click_count[index], fans_increase_count[index]))
        for value in values:
            self._sql_server.save_message('贝德美.dbo.bilibili_三连推广效果', values[value])

    def overview_of_promotion_effect_of_sanlian_request(self, start_day, end_day, cookie):
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


if __name__ == '__main__':
    bl = Bilibili()
    cookie = 'B_SESSDATA=8499bd98%2C1670313190%2C20131%2A99; bili_b_jct=9a844a3d3cf45e02c15ba2297bb8d062; B_DedeUserID=16136751; B_DedeUserID__ckMd5=0e1ea1f2d03bdee2; B_sid=pr3nsx32'
    bl.overview_of_promotion_effect_of_sanlian_main('', '', cookie)