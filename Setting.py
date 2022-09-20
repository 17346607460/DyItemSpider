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



# import aiohttp,asyncio
# import time
# async def get_html(session,url):
#     print('发送请求：',url)
#     async with session.get(url,verify_ssl=False)as response:
#         content=await response.content.read()
#         print('得到结果',url,len(content))
#         filename=url.rsplit('/')[-1]
#         print('正在下载',filename)
#         with open(filename,'wb') as file_object:
#             file_object.write(content)
#             print(filename,'下载成功')
# async def main():
#     async with aiohttp.ClientSession() as session:
#         start_time=time.time()
#         url_list=[
#             'https://images.cnblogs.com/cnblogs_com/blueberry-mint/1877253/o_201106093544wallpaper1.jpg',
#             'https://images.cnblogs.com/cnblogs_com/blueberry-mint/1877253/o_201106093557wallpaper2.jpg',
#             'https://images.cnblogs.com/cnblogs_com/blueberry-mint/1877253/o_201106093613wallpaper3.jpg',
#         ]
#
#         tasks=[loop.create_task(get_html(session,url))for url in url_list]
#         await asyncio.wait(tasks)
#         end_time=time.time()
#         print('is cost',round(end_time-start_time),'s')
#
# loop=asyncio.get_event_loop()
# loop.run_until_complete(main())


# wO5Yxl5j