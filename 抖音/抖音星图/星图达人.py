import json
import time

import requests, execjs
from CurrencyModule import *
import demjson

values = [
    ['名称', '粉丝', '带货视频数', '带货商品数', '平均销售额', '带货商品价格', '小店购物车点击量', '小店购物车点击率', '口碑', '预期cpm', 'gpm', '预期播放量', '个人作品互动率', '个人作品完播率', '粉丝增长量', '粉丝增长率',
     '星图指数', '1-20秒报价', '20-60秒报价', '60秒报价', '链接']]

try:
    pages = 201
    for page in range(1, pages):
        print(page)
        # url = f'https://www.xingtu.cn/h/api/gateway/handler_get/?platform_source=1&order_by=score&sort_type=2&search_scene=1&display_scene=1&limit=20&page={page}&regular_filter=%7B%22current_tab%22:3,%22marketing_target%22:1,%22task_category%22:1,%22use_recommend%22:true%7D&attribute_filter=%7B%7D&author_pack_filter=%7B%7D&service_name=go_search.AdStarGoSearchService&service_method=SearchForStarAuthors&sign_strict=1'
        url = f'https://www.xingtu.cn/h/api/gateway/handler_get/?platform_source=1&order_by=score&sort_type=2&search_scene=1&display_scene=1&limit=20&page={page}&regular_filter=%7B%22current_tab%22:3,%22marketing_target%22:2,%22task_category%22:1%7D&attribute_filter=%7B%22tag%22:%22[55]%22%7D&author_pack_filter=%7B%7D&service_name=go_search.AdStarGoSearchService&service_method=SearchForStarAuthors&sign_strict=1'

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': 'gfpart_1.0.1.3914_220078=0; csrf_session_id=20d1974d53dcafb9260661e17e54ba2a; csrftoken=ngWh3YmVTCd0Bu0Slwrv75MmwSemGOza; tt_webid=7137983864757208590; ttcid=42996287766a4726a23b683fb059f0f235; MONITOR_WEB_ID=df2e4f65-9605-4da8-8ae6-2d93df064d72; _tea_utm_cache_2018=undefined; passport_csrf_token=0d22cef8cdd37e920d940b829d08dd23; passport_csrf_token_default=0d22cef8cdd37e920d940b829d08dd23; gfpart_1.0.1.3969_220078=0; gfpart_1.0.1.3985_220078=0; tt_scid=Ty2oFT.JGvUzQ8j9EHqYFBtE8RzN-PArKL2l4FdlV8haBLDy4cZWimp1wI84EydP4772; s_v_web_id=verify_l7ogyj5x_1PEePs7u_s7AB_4g47_8sJB_OCiaFvsUWGwZ; sid_guard=50c6830a23f1bcc1e77bfd6984491847%7C1662364600%7C5184000%7CFri%2C+04-Nov-2022+07%3A56%3A40+GMT; uid_tt=f600804f2b67a814f60a4c1a71060495; uid_tt_ss=f600804f2b67a814f60a4c1a71060495; sid_tt=50c6830a23f1bcc1e77bfd6984491847; sessionid=50c6830a23f1bcc1e77bfd6984491847; sessionid_ss=50c6830a23f1bcc1e77bfd6984491847; sid_ucp_v1=1.0.0-KDlkOGFhODcyZmIwNTE0YjNmMzg2YmQ0ODFlMjk4ZDQ3ZTZhZWRlMzcKFQjejYG3mAMQuNfWmAYY-hM4AUDrBxoCbGYiIDUwYzY4MzBhMjNmMWJjYzFlNzdiZmQ2OTg0NDkxODQ3; ssid_ucp_v1=1.0.0-KDlkOGFhODcyZmIwNTE0YjNmMzg2YmQ0ODFlMjk4ZDQ3ZTZhZWRlMzcKFQjejYG3mAMQuNfWmAYY-hM4AUDrBxoCbGYiIDUwYzY4MzBhMjNmMWJjYzFlNzdiZmQ2OTg0NDkxODQ3; star_sessionid=efec34e46cf04cda69351b5dbef9a88a; gftoken=NTBjNjgzMGEyM3wxNjYyMzY0NjAyMDZ8fDAGBgYGBgY',
            'pragma': 'no-cache',
            'referer': 'https://www.xingtu.cn/ad/creator/market',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'x-csrftoken': 'ngWh3YmVTCd0Bu0Slwrv75MmwSemGOza',
            'x-login-source': '1',
            'x-secsdk-csrf-token': '0001000000012f5563282bb2df5abdda58bcdf53c9bf0ec63095ee75a88d86c4dee74896b5061711ee5eec4b2802',
            'x-star-service-method': 'SearchForStarAuthors',
            'x-star-service-name': 'go_search.AdStarGoSearchService'
        }

        with open(r'C:\Users\lianqinglongfei\Desktop\DyItemSpider\抖音\抖音星图\sign.js', 'r', errors='ignore') as r:
            b = r.read()
        signature = execjs.compile(b).call('get_sign', page)
        # print(signature)
        url = url + f'&sign={signature}'
        response = requests.get(url=url, headers=headers)
        print(response.text)
        response = response.json()
        datas = response['data']['authors']
        if not datas:
            break
        for data in datas:
            try:
                nick_name = json.loads(data['attribute_datas']['nick_name'])  # nick_name
            except:
                nick_name = ''
            try:
                follower = data['attribute_datas']['follower']  # 粉丝
            except:
                follower = ''
            try:
                author_avatar_frame_icon = data['attribute_datas']['author_avatar_frame_icon']  # 带货视频数
            except:
                author_avatar_frame_icon = ''
            try:
                ecom_video_product_num_30d = data['attribute_datas']['ecom_video_product_num_30d'].replace('"',
                                                                                                           '')  # 带货商品数
            except:
                ecom_video_product_num_30d = ''
            try:
                avg_sale_amount_range = json.loads(data['attribute_datas']['avg_sale_amount_range'])  # 平均销售额
            except:
                avg_sale_amount_range = ''
            try:
                ecom_main_price_30days = json.loads(data['attribute_datas']['ecom_main_price_30days'])  # 带货商品价格
            except:
                ecom_main_price_30days = ''
            try:
                ecom_video_mid_click_pv_30d_range = json.loads(
                    data['attribute_datas']['ecom_video_mid_click_pv_30d_range'])  # 小店购物车点击量
            except:
                ecom_video_mid_click_pv_30d_range = ''
            try:
                ecom_video_ctr_30d_range = json.loads(data['attribute_datas']['ecom_video_ctr_30d_range'])  # 小店购物车点击率
            except:
                ecom_video_ctr_30d_range = ''
            try:
                ecom_score = json.loads(data['attribute_datas']['ecom_score'])  # 口碑
            except:
                ecom_score = ''
            try:
                prospective_20_60_cpm = data['attribute_datas']['prospective_20_60_cpm']  # 预期cpm
            except:
                prospective_20_60_cpm = ''
            try:
                ecom_gpm_30days_range = json.loads(data['attribute_datas']['ecom_gpm_30days_range'])  # gpm
            except:
                ecom_gpm_30days_range = ''
            try:
                expected_play_num = data['attribute_datas']['expected_play_num']  # 预期播放量
            except:
                expected_play_num = ''
            try:
                interact_rate_within_30d = data['attribute_datas']['interact_rate_within_30d']  # 个人作品互动率
            except:
                interact_rate_within_30d = ''
            try:
                play_over_rate_within_30d = data['attribute_datas']['play_over_rate_within_30d']  # 个人作品完播率
            except:
                play_over_rate_within_30d = ''
            try:
                fans_increment_within_15d = data['attribute_datas']['fans_increment_within_15d']  # 粉丝增长量
            except:
                fans_increment_within_15d = ''
            try:
                fans_increment_rate_within_15d = float(
                    data['attribute_datas']['fans_increment_rate_within_15d']) / 100  # 粉丝增长率
            except:
                fans_increment_rate_within_15d = ''
            try:
                star_index = data['attribute_datas']['star_index']  # 星图指数
            except:
                star_index = ''
            try:
                price_1_20 = data['attribute_datas']['price_1_20']  # 1-20秒报价
            except:
                price_1_20 = ''
            try:
                price_20_60 = data['attribute_datas']['price_20_60']  # 20-60秒报价
            except:
                price_20_60 = ''
            try:
                price_60 = data['attribute_datas']['price_60']  # 60秒报价
            except:
                price_60 = ''
            try:
                star_id = f'https://www.xingtu.cn/ad/creator/author/douyin/{data["star_id"]}/1?search_session_id=7140170262716350478&video_type=2'
            except:
                star_id = ''
            info = [nick_name, follower, author_avatar_frame_icon, ecom_video_product_num_30d, avg_sale_amount_range,
                    ecom_main_price_30days, ecom_video_mid_click_pv_30d_range, ecom_video_ctr_30d_range, ecom_score,
                    prospective_20_60_cpm, expected_play_num, ecom_gpm_30days_range, interact_rate_within_30d,
                    play_over_rate_within_30d, fans_increment_within_15d, fans_increment_rate_within_15d, star_index,
                    price_1_20, price_20_60, price_60, star_id]
            value = []
            for i in info:
                if i == '-':
                    i = ''
                value.append(i)
            values.append(value)
            print(value)
        time.sleep(5)
    write_excel_xlsx('./星图报价.xlsx', 'data', values)
except Exception as e:
    print(e)
    write_excel_xlsx('./星图报价.xlsx', 'data', values)
