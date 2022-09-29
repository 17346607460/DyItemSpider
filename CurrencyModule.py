import datetime, traceback
import zipfile
from time import strftime
import time
import hmac, os
import hashlib
import base64
from urllib.parse import quote_plus

import demjson
import openpyxl
import requests, json


def get_number_day(start_time):
    timeArray = time.localtime(start_time)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


def get_after_day(start_time):
    '''
    params:
        start_time: 传入时间
    return:
        返回传入时间 + 1天
    '''
    try:
        try:
            start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d")
        except:
            start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        start_time = str((start_time + datetime.timedelta(days=+1))).split(' ')[0]
        return start_time
    except:
        error_message(0)


def get_today():
    return strftime('%Y-%m-%d')


def get_today_hour():
    return strftime('%H:%M:%S')

def get_hour_day():
    return strftime('%Y-%m-%d %H:%M:%S')


def get_month(data_info=1):
    '''

    :param data_info: 1 返回2021-11， 0 返回 202111
    :return:
    '''
    if data_info:
        month = strftime('%Y-%m-%d').split('-')[0] + '-' + strftime('%Y-%m-%d').split('-')[1]
    else:
        month = strftime('%Y-%m-%d').split('-')[0] + strftime('%Y-%m-%d').split('-')[1]
    return month


def get_after_month(date):
    date = date.replace('-', '')
    year = int(date[:-2])
    month = int(date[-2:])
    if month == 12:
        month = 1
        year += 1
    else:
        month += 1
    if month < 10:
        month = '0' + str(month)
    return str(year) + '-' + str(month)


def get_before_day(start_time):
    '''
    params:
        start_time: 传入时间
    return:
        返回传入时间 + 1天
    '''
    try:
        try:
            start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d")
        except:
            start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        start_time = str((start_time + datetime.timedelta(days=-1))).split(' ')[0]
        return start_time
    except:
        error_message(0)


def error_message(exit_type, fifter=0):
    '''
    报错信息设置
    :param exit_type: 是否退出程序 0：退出
    :return:
    '''
    error_info = traceback.format_exc().split('Traceback (most recent call last):')[-1].strip().split('\n')
    if fifter:
        if fifter in error_info[-1]:
            printColor(f' 跳过错误: -- {fifter}', color='32')
            return 0
        else:
            printColor(f' 无筛选条件: -- {fifter}', color='32')
            return 0
    printColor(f' 报错时间：-- {time.strftime("%Y-%m-%d %H:%M:%S")}\n 位置信息：-- {error_info[0]}\n 报错信息：-- {error_info[-1]}', color='31')
    if not exit_type:
        printColor(' 手动退出程序', color='31')
        exit()


def get_month_day(month):
    try:
        year = int(month.split('-')[0])
        month = int(month.split('-')[-1]) + 1
        if month == 13:
            month = 1
            year = year + 1
        month_day = get_before_day(str(year) + '-' + str(month) + '-01').split('-')[-1]
        return month_day
    except:
        error_message(0)


def get_time_number(start_day):
    try:
        result = int(time.mktime(time.strptime(start_day, "%Y-%m-%d")))
        return result
    except:
        result = int(time.mktime(time.strptime(start_day, "%Y-%m-%d %H:%M:%S")))
        return result


def change_number_today(timeStamp):
    try:
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return otherStyleTime
    except:
        error_message(0)


def get_day_before_today(day, number):
    start_time = datetime.datetime.strptime(day, "%Y-%m-%d")
    start_time = str((start_time + datetime.timedelta(days=-number))).split(' ')[0]
    print(start_time)
    return start_time


def get_before_month(start_month):
    # if '-' not in start_month:
    #     print(start_month[:-2])
    #     print(start_month[-2:])
    # print(start_month)
    start_month = (start_month + '-01').replace('-', '')
    start_month = datetime.datetime.strptime(start_month, "%Y%m%d").replace(day=1)
    start_month = get_before_day(str(start_month).split(' ')[0])
    res = start_month.split('-')[0] + '-' + start_month.split('-')[1]
    print(res)
    return res


def change_str_to_dict(infos):
    headers = {}
    for info in infos.split('\n'):
        try:
            if info.split(':')[0].strip() != 'accept-encoding' and info.split(':')[0].strip():
                headers[info.split(':')[0].strip()] = info.split(':')[1].strip()
        except:
            headers[info.split(':')[0]] = ''
    return headers


def erro_dingding(erro_text):
    # timestamp = round(time.time() * 1000)
    timestamp = time.time() * 1000
    secret = 'SEC09ec04d69c22f18f01fd9bda1638d68bca17f63000d9b52a62760cf3e0ee745e'
    # secret_enc = b'this is secret'
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = quote_plus(base64.b64encode(hmac_code))
    printColor(sign, color='31')

    # url = 'https://oapi.dingtalk.com/robot/send?access_token=3e5b6393c25f3cfdc15dc697fb83cc95ec848df4bc7143d392dd39a16e0d6d2b'
    url = 'https://oapi.dingtalk.com/robot/send?access_token=583b60654c16266f9b03a688e27c44ff473a457ff2ef44c475826ca3f14c0d0f'
    headers = {
        'Content-Type': 'application/json;charset=utf-8'
    }
    data_info = {"msgtype": "text", "text": {"content": "{}".format(erro_text)},
                 "at": {"atMobiles": [], "isAtAll": False}}
    value = json.dumps(data_info)
    res = requests.post(url, json=data_info)
    print(res.text)


def write_excel_xlsx(path, sheet_name, value):
    index = len(value)
    workbook = openpyxl.Workbook()  # 新建工作簿（默认有一个sheet？）
    sheet = workbook.active  # 获得当前活跃的工作页，默认为第一个工作页
    sheet.title = sheet_name  # 给sheet页的title赋值
    for i in range(0, index):
        for j in range(0, len(value[i])):
            sheet.cell(row=i + 1, column=j + 1, value=str(value[i][j]))  # 行，列，值 这里是从1开始计数的
    workbook.save(path)  # 一定要保存
    print("xlsx格式表格写入数据成功！")


def un_zip(file_name):
    """unzip zip file"""
    zip_file = zipfile.ZipFile(file_name)
    '''
    if os.path.isdir(file_name.split(".")[0]):  
        pass  
    else:  
        os.mkdir(file_name.split(".")[0])
    '''
    for names in zip_file.namelist():
        # zip_file.extract(names)  # 加入到某个文件夹中
        zip_file.extract(names, file_name.split(".")[0])
    zip_file.close()
    # file_names = os.listdir(r'C:\Users\lianqinglongfei\Desktop\DyItemSpider\热浪联盟\{}'.format(file_name.replace(".zip", "")))
    file_names = os.listdir(r'C:\Users\lianqinglongfei\Desktop\DyItemSpider\直通车\{}'.format(file_name.replace(".zip", "")))
    file_paths = []
    for fil in file_names:
        # file_path = os.path.join(r'C:\Users\lianqinglongfei\Desktop\DyItemSpider\热浪联盟', file_name.replace(".zip", ""))
        file_path = os.path.join(r'C:\Users\lianqinglongfei\Desktop\DyItemSpider\直通车', file_name.replace(".zip", ""))
        # print(file_path)
        for c in os.listdir(file_path):
            # n_path = os.path.join(file_path, c)
            file_paths.append(os.path.join(file_path, c))
            # for d in os.listdir(n_path):
            #     file_paths.append(os.path.join(n_path, d))
    return file_paths

# un_zip("test.zip").


def save_page(page_list):
    print(page_list)
    with open(r'F:\lqlf\日常程序\plug_in_unit\page.txt', 'w') as w:
        w.write(json.dumps(page_list))
    w.close()


def read_page():
    with open(r'F:\lqlf\日常程序\plug_in_unit\page.txt', 'r') as r:
        page_list = demjson.decode(r.read())
    r.close()
    return page_list


def printColor(msg, color='32'):
    '''

    :param msg: 需要输出的信息
    :param color: 输出信息的颜色 30（黑色）、31（红色）、32（绿色）、 33（黄色）、34（蓝色）、35（洋 红）、36（青色）、37（白色）0（默认\）、1（高亮）、22（非粗体）、4（下划线）、24（非下划线）、 5（闪烁）、25（非闪烁）、7（反显）、27（非反显）
    :return:
    '''
    # erro_dingding(msg)
    print(f'\033[0;{color}m {time.strftime("%Y-%m-%d %H:%M:%S")} {msg}\033[0m')


if __name__ == '__main__':
    start_day = 1661097600
    print(get_number_day(start_day))

# def get_after_month(start_month):
#     print(start_month)
#     start_month = (start_month + '-01').replace('-', '')
#     start_month = datetime.datetime.strptime(start_month, "%Y%m%d").replace(day=-1)
#     print(start_month)
# start_month = get_before_day(str(start_month).split(' ')[0])
# return start_month.split('-')[0] + '-' + start_month.split('-')[1]


# if __name__ == '__main__':
#     start_day = '2022-02'
#     print(get_before_day(get_after_month(start_day.replace("-", "")) + "-01"))
