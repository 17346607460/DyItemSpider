#!/usr/bin/env python
# -*- coding: utf-8 -*-

import frida
import requests
import time


# 发送接收frida_js信息
def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


js = open('app1.js', 'r', encoding='utf8').read()  # 读取frida脚本

session = frida.get_usb_device(timeout=1000).attach('com.yuanrenxue.challenge')

script = session.create_script(js)
script.on('message', on_message)
script.load()  # 加载frida脚本

if __name__ == '__main__':
    val = 0
    for i in range(1, 101):
        url = 'https://www.python-spider.com/api/app1'
        headers = {
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; Nexus 6P Build/MTC20L) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '61',
            'Host': 'www.python-spider.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'Cache-Control': 'no-cache'
        }
        time_ = int(time.time()*1000)  # 获取世家戳
        s = f'page={i}' + str(time_)
        bArr = [x for x in bytearray(s, 'utf_8')]
        res = script.exports.callsecretfunctionedy(bArr)  # 调用frida_js函数获取加密参数
        print(res)
        data = {
            'page': i,
            'sign': res,
            't': time_
        }
        response = requests.post(url=url, headers=headers, data=data, verify=False).json()
        datas = response['data']
        for info in datas:
            val += int(info['value'].replace('\r', ''))
        time.sleep(0.5)
        print(val)



