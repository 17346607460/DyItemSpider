import csv
import json
import traceback

import aiohttp
import pymssql
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from CurrencyModule import *
import pymysql
import redis
import time


# 数据库处理操作
# 连接数据库
class SqlServerConnect:
    def __init__(self):
        self.connect = pymssql.connect(
            '121.4.129.10',
            'chenchao',
            'lqlf6228998.',
            # '119.45.130.51',
            # 'longfei',
            # 'longfei2021'
        )  # 服务器名,账户,密码
        self.cursor = self.connect.cursor()

    def __del__(self):
        self.connect.close()
        self.cursor.close()
        print('数据库资源已关闭')

    def save_message(self, table, values, fifter=''):
        '''
        存储函数
        :param table: 表名
        :param values: 存入的数据
        :return: 返回0，1
        '''
        printColor(f'表名：{table}  数据：{values}')
        if not values:
            return 0
        try:
            if len(values) < 1:
                sql = f'insert into {table} values {values}'
                self.cursor.execute(sql)
                self.connect.commit()
            else:
                num = len(values[0])
                number = '(' + ('%s,' * num)[:-1] + ')'
                sql = f'insert into {table} values {number}'
                self.cursor.executemany(sql, values)
                self.connect.commit()
            return 1
        except:
            error_message(1, fifter=fifter)
            return 0

    def check_message(self, sql, result_type):
        '''
        查询语句
        :param sql: sql语句
        :param save_type: 返回的数据类型 0：一条， 1：多条, 2:不返回值
        :return: 返回查询结果
        '''
        try:
            print(sql)
            self.cursor.execute(sql)
            if result_type == 2:
                self.connect.commit()
                return 0
            return self.cursor.fetchall() if result_type else self.cursor.fetchone()
        except:
            error_message(0)
            return 0

    def get_start_day(self, table, word, filter, boolf='='):
        '''
        获取开始抓取的时间
        :param table: 数据库表名
        :return: 日期
        '''
        try:
            text = ''
            if filter:
                for key in filter:
                    if text == '':
                        text += f""" where {key} {boolf} '{filter[key]}'"""
                    else:
                        text += f""" and {key} {boolf} '{filter[key]}'"""
            sql = f"select max({word}) from {table}{text}"
            printColor(f'sql语句: {sql}')
            self.cursor.execute(sql)
            try:
                start_time = str(self.cursor.fetchone()[0])
                if word == '订单结算时间':
                    start_time = start_time.split(' ')[0]
            except:
                start_time = get_before_day(get_today())
            return start_time
        except:
            error_message(0)
            return 0

    def delete_change_week(self, table):
        sql = f'delete from {table} where 转化周期 < 30'
        self.cursor.execute(sql)
        self.connect.commit()

    def select_shop_id(self):
        '''

        :return:
        '''
        result = self.check_message("select 商品id from 贝德美.dbo.vw_t_cmpt_we_prdc_base_info ", 1)
        id_list = [i[0] for i in result]
        return id_list

    def delete_day(self, table, number):
        '''
        params:
            start_time: 传入时间
        return:
            返回传入时间 + 1天
        '''
        start_time = datetime.datetime.strptime(get_today(), "%Y-%m-%d")
        start_time = str((start_time + datetime.timedelta(days=-number))).split(' ')[0]
        sql = f"""select * from {table} where 直播开始时间 > '{start_time}'"""
        if self.check_message(sql, 1):
            sql = f"""delete from {table} where 直播开始时间 > '{start_time}'"""
            self.cursor.execute(sql)
            self.connect.commit()
            print('删除成功')
        else:
            print('无需要删除的数据')

    def delete_directional_click_effect_id_info(self):
        sql = "delete FROM [dbo].[超级推荐_商品推广_定向_点击效果_ID] where 转化周期<30 and 日期>= CONVERT(date,DATEADD(day, -90, getdate()),102)"
        self.cursor.execute(sql)
        self.connect.commit()

    def get_day_to_start(self, start_day, end_day, table, date, filter):
        if not start_day:
            start_day = self.get_start_day(table, date, filter)
            if start_day == get_before_day(get_today()):
                print('今天数据已经抓取完毕')
                return start_day, end_day, 0
            start_day = get_after_day(start_day)
        if not end_day:
            end_day = get_before_day(get_today())
        return start_day, end_day, 1

    def start_run_function(self, table):
        start_time = get_before_month(get_month()).replace("-", '')
        sql = f'select 月份 from {table} group by 月份'
        infos = []
        for item in self.check_message(sql, 1):
            infos.append(item[0])
        print(infos)
        if start_time in infos:
            return 0
        else:
            return start_time


class SqlServerReadConnect:
    def __init__(self):
        self.connect = pymssql.connect(
            '121.4.129.10',
            'read',
            'mtg+4%d',
            # '119.45.130.51',
            # 'longfei',
            # 'longfei2021'
        )  # 服务器名,账户,密码
        self.cursor = self.connect.cursor()

    def __del__(self):
        self.connect.close()
        self.cursor.close()
        print('数据库资源已关闭')

    def check_task(self):
        '''
        获取爬虫进度表的信息
        :return:
        '''
        sql = "select CONVERT(nvarchar(255), 数据库) 数据库, CONVERT(nvarchar(255), 表) 表, 截止日期 from 红色小象_数据交互.dbo.vw_爬虫进度表 where 取数频率='每日'"
        datas = self.implement_sql(sql, 1)
        for data in datas:
            table = data[0] + '.' + data[1]
            date = data[-1]
            RedisConnect().save_queue('sqlserverdb', {'table': table, 'date': date})

    def implement_sql(self, sql, result_type):
        '''
        查询语句
        :param sql: sql语句
        :param save_type: 返回的数据类型 0：一条， 1：多条, 2:不返回值
        :return: 返回查询结果
        '''
        try:
            print(sql)
            self.cursor.execute(sql)
            if result_type == 2:
                self.connect.commit()
                return 0
            return self.cursor.fetchall() if result_type else self.cursor.fetchone()
        except:
            error_message(0)
            return 0


class RedisConnect:
    def __init__(self):
        self.connect = redis.Redis(host='127.0.0.1', port=6379, db=0)

    def save_key_value(self, key, value):
        try:
            self.connect.set(key, value)
            printColor(f'{time.strftime("%Y-%m-%d %H:%M:%S")} {key, value}已存入redis', color='37')
        except Exception as e:
            printColor(f'{time.strftime("%Y-%m-%d %H:%M:%S")} {key, value}存入redis失败 报错信息: {e}', color='31')

    def save_queue(self, key, value):
        try:
            value['status'] = 1
            self.connect.rpush(key, json.dumps(value))
            printColor(f'{time.strftime("%Y-%m-%d %H:%M:%S")} {value}已存入{key}', color='32')
        except Exception as e:
            printColor(f'{value}存入{key}失败 报错信息: {e}', color='31')
            exit()

    def read_queue(self, key):
        return self.connect.lrange(key, 1, -1)

    def clear_db(self, key):
        self.connect.delete(key)


class MysqlConnect:

    def __init__(self):
        self.connect = pymysql.connect(
            host='118.31.104.96',
            user='root',
            password='7720051',
            database='funds',
            # charset='utf-8',
            port=3306
        )
        self.cursor = self.connect.cursor()

    def save_message(self, table, values):
        '''
        存储函数
        :param table: 表名
        :param values: 存入的数据
        :return: 返回0，1
        '''
        try:
            print(values)
            if len(values) <= 1:
                sql = f'insert into {table}(fund_name, fund_id, short_name) values {values[0]}'
                print(sql)
                self.cursor.execute(sql)
                self.connect.commit()
            else:
                num = len(values[0])
                number = '(' + ('%s,' * num)[:-1] + ')'
                sql = f'insert into {table}(fund_name, fund_id, short_name) values {number}'
                print(sql)
                self.cursor.executemany(sql, values)
                self.connect.commit()
            return 1
        except:
            error_message(0)
            return 0

    def save_5_years_info(self, table, values):
        try:
            print(values)
            if len(values) <= 1:
                sql = f'insert into {table}(fund_id, profit, profit_time, profit_type) values {values[0]}'
                print(sql)
                self.cursor.execute(sql)
                self.connect.commit()
            else:
                num = len(values[0])
                number = '(' + ('%s,' * num)[:-1] + ')'
                sql = f'insert into {table}(fund_id, profit, profit_time, profit_type) values {number}'
                print(sql)
                self.cursor.executemany(sql, values)
                self.connect.commit()
            return 1
        except:
            error_message(0)
            return 0


    def check_message(self, sql, result_type):
        '''
        查询语句
        :param sql: sql语句
        :param save_type: 返回的数据类型 0：一条， 1：多条
        :return: 返回查询结果
        '''
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall() if result_type else self.cursor.fetchone()
        except:
            error_message(0)
            return 0


def get_Access_Token(auth_code, app_id, secret):
    header = {'Content-Type': 'application/json'}
    url_access_token = 'https://ad.oceanengine.com/open_api/oauth2/access_token/'
    data = {
        "app_id": app_id,
        "secret": secret,
        "grant_type": "auth_code",
        "auth_code": auth_code

    }

    response = requests.post(url_access_token, headers=header, json=data)
    response_data = response.json()
    return response_data


def get_drsp_token(app_id, secret):
    sql = f"select GetTime, access_token, refresh_token from 贝德美.DDGF.t_Marketing_API_base_info where APP_ID='{app_id}'"
    result = SqlServerConnect().check_message(sql, 0)
    print(result)
    diff_day = int((get_time_number(str(get_hour_day())) - get_time_number(str(result[0]))) / (60 * 60 * 24))
    print(diff_day)
    if diff_day >= 30:
        auth_code = input('Refresh_Token已超过30天，请重新授权，输入回调地址中的auth_code：')
        response_data = get_Access_Token(auth_code, app_id, secret)
        access_token = response_data['data']['access_token']
        refresh_token = response_data['data']['refresh_token']
    else:
        response_data = get_Refresh_Token(result[-1], app_id, secret)
        access_token = response_data['data']['access_token']
        refresh_token = response_data['data']['refresh_token']
    sql = f"update 贝德美.DDGF.t_Marketing_API_base_info set GetTime='{get_hour_day()}', access_token='{access_token}', refresh_token='{refresh_token}' where APP_ID='{app_id}'"
    print(sql)
    SqlServerConnect().check_message(sql, 2)
    print(access_token, refresh_token)
    return access_token


def get_Refresh_Token(refresh_token, app_id, secret):
    # print('refresh_token', refresh_token)
    url_refresh_token = "https://ad.oceanengine.com/open_api/oauth2/refresh_token/"
    header = {'Content-Type': 'application/json'}
    data = {
        "app_id": app_id,
        "secret": secret,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token

    }
    response = requests.post(url_refresh_token, headers=header, json=data)
    response_data = response.json()
    print("response_data", response_data)
    return response_data


#  https://e.bilibili.com/site/home  785695062@qq.com  bdm20228017.
bilibili_cookie = 'B_SESSDATA=8499bd98%2C1670313190%2C20131%2A99; bili_b_jct=9a844a3d3cf45e02c15ba2297bb8d062; B_DedeUserID=16136751; B_DedeUserID__ckMd5=0e1ea1f2d03bdee2; B_sid=pr3nsx32'

#  https://sycm.taobao.com/custom/login.htm?_target=http://sycm.taobao.com/portal/home.htm?activeKey=taobaoUpper&dateRange=2021-09-27%7C2021-09-27&dateType=day&spm=a217wi.openworkbeachtb_web   贝德美旗舰店:龙飞  lqlf6228998
dbo_cookie = 't=ba991419abcabe60cd3884e42a2b30f4; thw=cn; cookie2=1f9299af1907012d87ad1bdc6b31c185; _tb_token_=531317e3585e1; _samesite_flag_=true; cancelledSubSites=empty; XSRF-TOKEN=e409111c-aff5-47d8-be3a-c2fb174800f9; _m_h5_tk=a97ffda303ba6d7d5a53df5970385b96_1663921110319; _m_h5_tk_enc=3d9cf74de914c3ea17c8e80a0de0672c; xlly_s=1; JSESSIONID=2FA0345477181BF906A14B7ADA51A6FE; tfstk=cM7OBx1ZgJ2M38OdaGEH3x6iiQPhZk2vdf9mkZAGcAluXK3AisblyuG3fI9yBWC..; sgcookie=E100PItObykaEux3HbJWKWt31AceUNZ75JJk5Xq3iBCZW4l6HDJIEHFnyqEBzBdwd8tSgW2C757d2z%2BNtF123MfOCRFavz%2BnqwShJsaSPCLPrl4%3D; uc1=cookie21=WqG3DMC9Eman&cookie14=UoeyChPsKGtolQ%3D%3D; unb=2212731641217; sn=%E8%B4%9D%E5%BE%B7%E7%BE%8E%E6%97%97%E8%88%B0%E5%BA%97%3A%E9%BE%99%E9%A3%9E; csg=3565b28e; skt=8faa92701f68a3c7; _cc_=UIHiLt3xSw%3D%3D'

#  https://sycm.taobao.com/portal/home.htm?activeKey=operator&dateRange=2022-09-21%7C2022-09-21&dateType=day  bodormebaby旗舰店:龙飞  lqlf6228998
BODORME_cookie = 't=da03a3a2ff72f7a25e393fbd232e1134; cookie2=121ead4360c93f87765c152c6653fe17; _tb_token_=389583a0e66ae; _samesite_flag_=true; __wpkreporterwid_=08eb790e-219c-4364-1c94-8cee8705e366; _m_h5_tk=e9ccdf0f241068825cafdc08487d0be3_1664397348721; _m_h5_tk_enc=508440ce92b2c8658f5fbb62ce6fc57c; xlly_s=1; cancelledSubSites=empty; sgcookie=E1004YdA4gZ1SC96nojEbR%2BU49gLVDMM4%2FFaHAFcnwkrs5JQAzKBcA7XbwNGpsRstLeEumwefS7NUcpw%2BHvnJP7L7l1oNi%2Fp%2FyTHcigIIdPCwKw%3D; unb=2211227458136; uc1=pas=0&cookie14=UoeyChYV972dmw%3D%3D&existShop=false&cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D&cookie21=Vq8l%2BKCLiw%3D%3D; uc3=lg2=WqG3DMC9VAQiUQ%3D%3D&id2=UUpgR1CZuQznIbZW7g%3D%3D&nk2=EF2TYQY0F0dH5%2F4%3D&vt3=F8dCv4Sm6nRa7GDKn8s%3D; csg=7b3bdba6; lgc=scm27891300; cookie17=UUpgR1CZuQznIbZW7g%3D%3D; dnk=scm27891300; skt=c0d17ee7916d20bc; existShop=MTY2NDQxODExMw%3D%3D; uc4=id4=0%40U2gqyO3pcEiZXLDSGE5mx%2FK2FQbrmZ14&nk4=0%40EoTGjVAUdXJN3jYc2LCfdK9jjoQEpQ%3D%3D; tracknick=scm27891300; _cc_=UIHiLt3xSw%3D%3D; _l_g_=Ug%3D%3D; sg=069; _nk_=scm27891300; cookie1=AV1z4DhgRbgAIDoG84bMNy0IaVRkH3WLBGTVZtNEzNo%3D; cna=jWCxGw8o4HwCAXPG25PMGsWZ; JSESSIONID=5AC2D9B0D8F42C188ABE4EE994CCEEE4; l=eBE4J76mTrlCl6A8oOfwourza77OSIRAguPzaNbMiOCP96Av54ihW6uSyI_JC3GVh6JvR3lMfBR8BeYBqI0k4AsqK6Po_fkmn; tfstk=cn8fBvDU--2jah3gotGr3UT0nE-1ZXVC1m6DGY8HuERtT_Rfi8zFdxlHjRQN6_1..; isg=BMHBbnc5RiXOXqoO4UuvOB2d0A3b7jXgKYB0RyMWvUgnCuHcaz5FsO8M7H5MAs0Y'

#  https://unidesk.taobao.com/login.html  淘宝扫码登录
ud_cookie = 't=da03a3a2ff72f7a25e393fbd232e1134; cookie2=121ead4360c93f87765c152c6653fe17; _tb_token_=389583a0e66ae; _samesite_flag_=true; XSRF-TOKEN=a358f125-cb92-461a-ba49-23c782f29cad; cancelledSubSites=empty; v=0; _m_h5_tk=e9ccdf0f241068825cafdc08487d0be3_1664397348721; _m_h5_tk_enc=508440ce92b2c8658f5fbb62ce6fc57c; cna=jWCxGw8o4HwCAXPG25PMGsWZ; xlly_s=1; sgcookie=E100gCn0WqT3Wgxu3LdgUPFoE6Okp9jPqPK2f24wg95KR1Y%2BCxMlIpNS25d29V1u%2B3oc3BFmIHktyeWKz8SUfi7jcMUUDk8QMZkspxE1N94ouhYIZHQ6WcqwRCDlhYRE78WI; unb=2911123925; uc1=cookie16=URm48syIJ1yk0MX2J7mAAEhTuw%3D%3D&cookie15=W5iHLLyFOGW7aA%3D%3D&cookie14=UoeyChYV%2Bq2j%2FQ%3D%3D&cookie21=VFC%2FuZ9aiKCaj7AzMHh1&pas=0&existShop=false; uc3=vt3=F8dCv4Sm61lriHgHT%2Bg%3D&nk2=2HadJau3DBvYAZBwqDA%3D&lg2=UtASsssmOIJ0bQ%3D%3D&id2=UUGjM7Vaabayaw%3D%3D; csg=1553dfed; lgc=%5Cu5212%5Cu8239%5Cu4E0D%5Cu7528%5Cu6D465273; cookie17=UUGjM7Vaabayaw%3D%3D; dnk=%5Cu5212%5Cu8239%5Cu4E0D%5Cu7528%5Cu6D465273; skt=096914ec5ca1d2af; existShop=MTY2NDQxNTk1OQ%3D%3D; uc4=id4=0%40U2OU%2FCTNRsEE%2FBzQre%2FdEWAqGk6F&nk4=0%402kOEDA6snKdq9Xf8ZbZe7jVRAjWg4OLA1g%3D%3D; tracknick=%5Cu5212%5Cu8239%5Cu4E0D%5Cu7528%5Cu6D465273; _cc_=Vq8l%2BKCLiw%3D%3D; _l_g_=Ug%3D%3D; sg=359; _nk_=%5Cu5212%5Cu8239%5Cu4E0D%5Cu7528%5Cu6D465273; cookie1=BxY4nPx7lTc5Cr9xWOOwFyTAZ4s3p5pkw9q782BJR%2BA%3D; ud_cloud_uid=adb3081e0045318d5a17ffb66b112126; l=eBE4J76mTrlClrM6BOfwlurza77OAIRAguPzaNbMiOCP995k55DdW6uJ9-8DCnGVh67HR3lMfBR8BeYBqIqgqt0p9gW-XDHmn; tfstk=cKEdBtjmg1f3K5fobDQiaURZZ0eRZH5-1pGk2uxekvlCwjxRinq0Dp9GRYGq9OC..; isg=BDEx590V9vRHnVr-8XsfaA3NQL3LHqWQOXDkFxNGHvgXOlGMW20RYaRcXM5c8j3I'

#  https://diantoushi.com/index.html#exponent   15158036889  beidemei2021  店透视
dts_cookie = 'Hm_lvt_623a6e6c9e21142aa93edc3fffb24a30=1663579827; token=80265f3e-7127-4e7a-af6b-5d3f450d00b5; Hm_lpvt_623a6e6c9e21142aa93edc3fffb24a30=1663583486'

#  https://sycm.taobao.com/portal/home.htm?activeKey=taobaoUpper&dateRange=2022-09-25%7C2022-09-25&dateType=day  dyyyz99:练庆龙飞  lqlf6228998 红色小象
hsxx_cookie = 't=da03a3a2ff72f7a25e393fbd232e1134; cookie2=121ead4360c93f87765c152c6653fe17; _tb_token_=389583a0e66ae; _samesite_flag_=true; ucn=center; xlly_s=1; sgcookie=E100oauEO%2FL3lldFWhgTcQ4KOMGAiyUJiEKagEkaCijPLMEfHqj0n37xEavgoh0JfO2Mbwc3I4s5Tand5jF3z3MMRuQGFfe0%2BmGBAHtaIe6zJLY%3D; unb=2212628883848; sn=dyyyz99%3A%E7%BB%83%E5%BA%86%E9%BE%99%E9%A3%9E; uc1=cookie21=U%2BGCWk%2F7oPIg&cookie14=UoeyChADUAWFkQ%3D%3D; csg=bad34586; cancelledSubSites=empty; skt=7fd8fc342143f837; _cc_=U%2BGCWk%2F7og%3D%3D; v=0; cna=jWCxGw8o4HwCAXPG25PMGsWZ; _m_h5_tk=e0959b6191b0faa02aa17c4cc443eb4a_1664275018829; _m_h5_tk_enc=6bcd31bde2e223d717c83cfe0d77bb52; l=fBE4J76mTrlClHhyKOfZourza77TJIRAguPzaNbMi95P_TCD5TvcW6uVBOTkCnGVF6lBR3lMfBR8BeYBqCvdvMKTi1p8krHmnmOk-Wf..; tfstk=c1khB0iQDXPIUKJ-52wBUc0xNGehZOXzoYksQH3VQlCrt2kNi0fNgRaJjyYX8_1..; isg=BNvb_hezPFBz4EA8z8UlSmv7aj9FsO-ynyYe1c0Y91r7rPuOVYUTA1MmRgwijEeq'

# https://subway.simba.taobao.com/#!/home/index-new  贝德美旗舰店:龙飞  lqlf6228998 直通车cookie
bdm_ztc_cookie = 't=ba991419abcabe60cd3884e42a2b30f4; __wpkreporterwid_=8fa9f0f4-e1f9-4a14-05f9-1ce8b82ece5a; thw=cn; cookie2=1f9299af1907012d87ad1bdc6b31c185; _tb_token_=531317e3585e1; _samesite_flag_=true; _m_h5_tk=82c4e3c4b03a3506a3709fa99d1a8d2b_1664185432453; _m_h5_tk_enc=25cc6dc28487c2240d8689f9153ef899; unb=2212731641217; sn=%E8%B4%9D%E5%BE%B7%E7%BE%8E%E6%97%97%E8%88%B0%E5%BA%97%3A%E9%BE%99%E9%A3%9E; cancelledSubSites=empty; v=0; sgcookie=E1007v3wd4OpOoll%2Be1qFCdmQYeQI3%2BMWDtIfQaEzIqMTeUEb8ExUjYqBalVGm5ZUkANJZTXie13dIFyY%2FvOqXFlmHRlw7JmmQ%2BMOJTvU1%2BMlS4%3D; uc1=cookie14=UoeyChACxXTc%2Fg%3D%3D&cookie21=U%2BGCWk%2F7oPIg; csg=6811490b; skt=ffdefa33c2df5692; _cc_=Vq8l%2BKCLiw%3D%3D; cna=nWYbGpuKHDsCAXkEs3F2iXa2; xlly_s=1; JSESSIONID=185831310D92E7528FB78A4DDFCCF4A0; tfstk=cOsdBvXEU5V34yNkbHUMagTRIbSdZkVJ1vOo2gvWTsW_HCiRi_jcDrMgRLO29RC..; l=eBSlN7-VTNKFSRf8BOfwourza77OSIRAguPzaNbMiOCPOX5e5NghW6u4Gp8wC3GVh6LkR3z1UrspBeYBqIfQ2hv1MexHfhMmn; isg=BMbGrpb92eN_iI0jfHWpX2CDF7xIJwrh2IRgzrDvsunEs2bNGLda8axFi-9_GwL5'

# https://subway.simba.taobao.com/#!/home/index-new  bodormebaby旗舰店:龙飞  lqlf6228998  贝德美.BODORME.直通车_账户报表
BODORME_ztc_cookie = 't=da03a3a2ff72f7a25e393fbd232e1134; cookie2=121ead4360c93f87765c152c6653fe17; _tb_token_=389583a0e66ae; _samesite_flag_=true; __wpkreporterwid_=08eb790e-219c-4364-1c94-8cee8705e366; _m_h5_tk=b252fc270ad1e7eb9d7a08e9eef0e39b_1664182270369; _m_h5_tk_enc=de13984e540da0eac8107afe55482399; sgcookie=E1009lT2bDTmq82F8O5O00mozKGLBpx04Mzh%2FV51VFeX8vD1FfYqaTeqLEVITM%2BQoIyCFVn4hM9Tugmj66TCqQyI7YUkVhIKaL1m%2Fj1zKSQls3A%3D; unb=2213334203009; sn=bodormebaby%E6%97%97%E8%88%B0%E5%BA%97%3A%E9%BE%99%E9%A3%9E; uc1=cookie14=UoeyChACx83nog%3D%3D&cookie21=V32FPkk%2FhSg%2F; csg=282ee02b; cancelledSubSites=empty; skt=96c6a802d4d5edae; _cc_=V32FPkk%2Fhw%3D%3D; cna=jWCxGw8o4HwCAXPG25PMGsWZ; v=0; xlly_s=1; JSESSIONID=CAA5AC325878BBC92F4402323A84192F; l=eBE4J76mTrlClG-fAOfwourza77OSIRAguPzaNbMiOCP91Qv5iTNW6u44JdJC3GVh6BWR3lMfBR8BeYBqIxuKp9PMexHfhMmn; tfstk=c3ZlBu2SBzuWu2sLG7i5Y-S0A_fPZStEskrb0TFGhxox02ZViXY27mGdnbf1ae1..; isg=BF9fJzAkQCTpmUQgk1Fpfs-X7rPpxLNmu_oa6fGs-45VgH8C-ZRDtt1WQhD-GIve'

# https://subway.simba.taobao.com/#!/home/index-new  TMCS账号进入
tmcs_ztc_cookie = 't=da03a3a2ff72f7a25e393fbd232e1134; cookie2=121ead4360c93f87765c152c6653fe17; _tb_token_=389583a0e66ae; _samesite_flag_=true; __wpkreporterwid_=08eb790e-219c-4364-1c94-8cee8705e366; _m_h5_tk=e9ccdf0f241068825cafdc08487d0be3_1664397348721; _m_h5_tk_enc=508440ce92b2c8658f5fbb62ce6fc57c; xlly_s=1; cancelledSubSites=empty; sgcookie=E1004YdA4gZ1SC96nojEbR%2BU49gLVDMM4%2FFaHAFcnwkrs5JQAzKBcA7XbwNGpsRstLeEumwefS7NUcpw%2BHvnJP7L7l1oNi%2Fp%2FyTHcigIIdPCwKw%3D; unb=2211227458136; uc1=pas=0&cookie14=UoeyChYV972dmw%3D%3D&existShop=false&cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D&cookie21=Vq8l%2BKCLiw%3D%3D; uc3=lg2=WqG3DMC9VAQiUQ%3D%3D&id2=UUpgR1CZuQznIbZW7g%3D%3D&nk2=EF2TYQY0F0dH5%2F4%3D&vt3=F8dCv4Sm6nRa7GDKn8s%3D; csg=7b3bdba6; lgc=scm27891300; cookie17=UUpgR1CZuQznIbZW7g%3D%3D; dnk=scm27891300; skt=c0d17ee7916d20bc; existShop=MTY2NDQxODExMw%3D%3D; uc4=id4=0%40U2gqyO3pcEiZXLDSGE5mx%2FK2FQbrmZ14&nk4=0%40EoTGjVAUdXJN3jYc2LCfdK9jjoQEpQ%3D%3D; tracknick=scm27891300; _cc_=UIHiLt3xSw%3D%3D; _l_g_=Ug%3D%3D; sg=069; _nk_=scm27891300; cookie1=AV1z4DhgRbgAIDoG84bMNy0IaVRkH3WLBGTVZtNEzNo%3D; cna=jWCxGw8o4HwCAXPG25PMGsWZ; JSESSIONID=5AC2D9B0D8F42C188ABE4EE994CCEEE4; l=eBE4J76mTrlCl6A8oOfwourza77OSIRAguPzaNbMiOCP96Av54ihW6uSyI_JC3GVh6JvR3lMfBR8BeYBqI0k4AsqK6Po_fkmn; tfstk=cn8fBvDU--2jah3gotGr3UT0nE-1ZXVC1m6DGY8HuERtT_Rfi8zFdxlHjRQN6_1..; isg=BMHBbnc5RiXOXqoO4UuvOB2d0A3b7jXgKYB0RyMWvUgnCuHcaz5FsO8M7H5MAs0Y'

# https://web.txcs.tmall.com/?frameUrl=https%3A%2F%2Fweb.txcs.tmall.com%2Fpages%2Fchaoshi%2Fcommon_tj_index#43037.708964  TMCS账号进入
tmcs_cookie = 'cna=jWCxGw8o4HwCAXPG25PMGsWZ; cancelledSubSites=empty; t=da03a3a2ff72f7a25e393fbd232e1134; cookie2=121ead4360c93f87765c152c6653fe17; login=true; SCMLOCALE=zh-cn; SCMSESSID=121ead4360c93f87765c152c6653fe17@HAVANA; SCMBIZTYPE=6000; X-XSRF-TOKEN=f56bbed8-b629-42f5-bfc2-fea86d0fcdb3; ascp_web_canary=0; dnk=scm27891300; tracknick=scm27891300; lid=scm27891300; lgc=scm27891300; _tb_token_=389583a0e66ae; uc1=cookie21=Vq8l%2BKCLiw%3D%3D&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&cookie14=UoeyChPv%2B%2FoznQ%3D%3D&cookie15=UIHiLt3xD8xYTw%3D%3D&pas=0&existShop=false; uc3=vt3=F8dCv4UzALsxoRN6aG0%3D&lg2=UIHiLt3xD8xYTw%3D%3D&id2=UUpgR1CZuQznIbZW7g%3D%3D&nk2=EF2TYQY0F0dH5%2F4%3D; uc4=nk4=0%40EoTGjVAUdXJN3jYc2LCfdKoQD6%2BA%2Bw%3D%3D&id4=0%40U2gqyO3pcEiZXLDSGE5mx%2FK2EKk03sFZ; sgcookie=E100PaBGO7rYkO4oT3d7FZrj6wyCkQjYC3ThHC9NL%2Fp6yY0fnfnME7xhIfQWp9eWDh6juAEQwQF6jAB8BUpgv8yT5HrfWrs2PF1lPGp3iJypQm0%3D; csg=99b54d36; xlly_s=1; l=eBMd4zWcTrlTD6ehKOfwourza77OSIRAguPzaNbMiOCP9e5v5Oq1W6u4xoLJC3GVh6DXR3lMfBR8BeYBqQAonxvObA13OWMmn; tfstk=c9dGBmY1ydW6pjhvAh1sgekrFiTcZRNVqIRBTVKoB0LGvwOFiG2UU6sx-GmSb-1..; isg=BG9vPUWpUNQQdVTwBuBcTuoA_oN5FMM2K4pqmYH8C17l0I_SieRThm2GUsBuqJuu'

# https://subway.simba.taobao.com/#!/home/index-new  bodormebaby旗舰店:龙飞  lqlf6228998
tbk_cookie = 't=6711df92ba85c36afe639a438682e232; cna=nWYbGpuKHDsCAXkEs3F2iXa2; new-entrance-guide=true; cookie2=16d1d66e7db5a00e8c432bb85e5ca446; v=0; _tb_token_=51ee57e3bfee9; rurl=aHR0cDovL2FkLmFsaW1hbWEuY29tL3BvcnRhbC92Mi9kYXNoYm9hcmQuaHRtP3NwbT1hMjFhbi4xMTUzMjkzMS5Qb3J0YWxMYXlvdXQuX3BvcnRhbF92Ml9kYXNoYm9hcmQuNGI0ZjYxZGJRcVNNMVo%3D; alimamapwag=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEwNS4wLjAuMCBTYWZhcmkvNTM3LjM2; cookie32=303ec5c4dd8647c00cb35935f52fef4b; alimamapw=F3tSFSQDFiZRQHYFHXVWRiJSF3pVFSN0FiYgQHQFHXRQRiQjOwlWVFIBUlNTVVcCDw9XAAdSUQpU%0AA1VVAlNVAwEGXFMH; cookie31=Mzk4MzcwMDU1LCVFOCVCNCU5RCVFNSVCRSVCNyVFNyVCRSU4RSVFNiU5NyU5NyVFOCU4OCVCMCVFNSVCQSU5Nyxib2Rvcm1lQGNvc2Vhc3QuY29tLFRC; taokeisb2c=; taokeIsBoutiqueSeller=eQ%3D%3D; xlly_s=1; login=U%2BGCWk%2F75gdr5Q%3D%3D; isg=BICAf5GI93EF4InUKqAwEzZOUQ5SCWTTAgLmXPoRTBsudSCfohk0Y1ZHjd21Xhyr; tfstk=ck7hB3b1XM-IjUzRC9TQz1LlTBzAwguyna717WBXLgxE7VfcscoVALFMK-wEV; l=eBL6dPl4gpC2gJDzBOfanurza77OSIRYYuPzaNbMiOCPO9fB5JKfW6uVGZL6C3GVh6RyR3z1UrspBeYBqQAonxvOuIujsfDmn'

BODORME_tbk_cookie = 't=614a575cbddcc3cdc1577b258be2e79f; cookie2=1100978c320dfe4894d3c9188ecf598e; v=0; _tb_token_=f5954dfe57e57; cna=jWCxGw8o4HwCAXPG25PMGsWZ; alimamapwag=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzk0LjAuNDYwNi41NCBTYWZhcmkvNTM3LjM2; cookie32=e0fafcac5305db527e84d55da7921752; alimamapw=AwxQW0BYXVFTVxgVJwJGfXVHIycRdQAQegYXcCAVUAQCVF8PAA5VPQIAXAcEVFYHVFZWDw9QAgUE%0AVwECCwBQBFYBAgBSXFMA; cookie31=MjQxNTEwMDE0MCxib2Rvcm1lYmFieSVFNiU5NyU5NyVFOCU4OCVCMCVFNSVCQSU5NyU0MGFsaW1hbWEsMjIxMzI4NjU4Nzk3OUBhbGltYW1hLmNvbSxUQg%3D%3D; taokeisb2c=; taokeIsBoutiqueSeller=eQ%3D%3D; rurl=aHR0cDovL2FkLmFsaW1hbWEuY29tL3BvcnRhbC92Mi9kYXNoYm9hcmQuaHRtP3NwbT1hMjFhbi4xMTUzMjkzMS5Qb3J0YWxMYXlvdXQuX3BvcnRhbF92Ml9kYXNoYm9hcmQuNGI0ZjYxZGJRcVNNMVo%3D; xlly_s=1; login=UtASsssmOIJ0bQ%3D%3D; isg=BHNzJs3ZFC-iddhloTpZCioIAnedqAdqt97mLSUQzxLJJJPGrXiXutG23lTKn19i; tfstk=c9x1BJGzq5V_0vi0j1ME_H_E3eIAwt25hV1MCX-lPrOPA_108u5S_YY0MiWAd; l=eBMyJDRITre7yb-kBOfanurza77OSIRYYuPzaNbMiOCPO9fB505hW6uS4TL6C3GVh6vvR3lMfBRJBeYBqQAonxvOuIujsfDmn'

# wO5Yxl5j