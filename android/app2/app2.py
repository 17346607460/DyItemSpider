import frida
import requests
import time


# 发送接收frida_js信息
def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


js = open('app2.js', 'r', encoding='utf8').read()  # 读取frida脚本

session = frida.get_usb_device(timeout=1000).attach('com.yuanrenxue.challenge')

script = session.create_script(js)
script.on('message', on_message)
script.load()  # 加载frida脚本

if __name__ == '__main__':
    time_ = int(time.time() * 1000)  # 获取世家戳
    s = '1:' + str(time_)
    bArr = [x for x in bytearray(s, 'utf_8')]
    res = script.exports.callsecretfunctionedy(bArr)  # 调用frida_js函数获取加密参数
    print(res)