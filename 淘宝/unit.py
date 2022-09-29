import time
from selenium import webdriver
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import json, requests


def init_browser():
    """
    启动一个浏览器，提供 js 执行环境
    :return:
    """
    option = webdriver.ChromeOptions()
    option.add_experimental_option("useAutomationExtension", False)
    option.add_experimental_option("excludeSwitches", ['enable-automation'])
    option.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(chrome_options=option)
    driver.get("https://www.baidu.com")
    driver.execute_script(open(r"F:\lqlf\日常程序\plug_in_unit\pdd32.js", encoding="utf16").read())
    return driver


def get_token(browser):
    msg = browser.execute_script("return window.Me()")
    return msg


def get_signature(browser, url):
    time.sleep(1)
    signature = browser.execute_script(f"return window.byted_acrawler.sign({{'url':'{url}'}})")
    # browser.close()
    return signature


def init_browser_dy():
    """
    启动一个浏览器，提供 js 执行环境
    :return:
    """
    option = webdriver.ChromeOptions()
    option.add_experimental_option("useAutomationExtension", False)
    option.add_experimental_option("excludeSwitches", ['enable-automation'])
    option.add_argument("--disable-blink-features=AutomationControlled")
    # option.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=option)

    # driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    #     "source": """
    #     Object.defineProperty(navigator, 'webdriver', {
    #         get: () => undefined
    #     })
    #     """
    # })
    driver.get("https://compass.jinritemai.com/login")
    return driver


def decrypt(text):
    # print('text:',text)
    # key = 'sycmsycmsycmsycm'.encode('utf-8')
    # iv = b'mcysmcysmcysmcys'
    key = 'w28Cz694s63kBYk4'.encode('utf-8')# 密码
    iv = b'4kYBk36s496zC82w'# 偏移量
    mode = AES.MODE_CBC
    cryptos = AES.new(key, mode, iv)
    plain_text = cryptos.decrypt(a2b_hex(text))
    # print(bytes.decode(plain_text))
    res = bytes.decode(plain_text).rstrip('\0').replace('：', ':').replace('null', '0').replace("true",'\"true\"').replace("false", '\"false\"')
    # print(res)
    # .replace('\t','').replace(' ', '')
    # 取出最后一位字符
    try:
        last = res[-1]
        if last != ']' and last != '}':  # 如说last不等于 ] 和 } ,说明有填充，则替换掉
            res = res.replace(last, '')
    except IndexError:  # 报错则说明是空串， 返回false
        return False

    try:
        first = res[0]          # 判断字符串是字典还是列表
    except IndexError:         # 报此错说明是个空串
        return res

    first = res[0]
    if first == '[':
        # print(type(res))
        data = eval(res.replace('babe"true"','babetrue'))
        return data
    elif first == '{':
        data = json.loads(res.replace('babe"true"','babetrue'), strict=False)
        # data = res
        return data
    return res


def get_change(x):
    if x == 0 or x == None:
        return 0
    url = 'https://tool.musicheng.com/exponent/calcult'
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-length': '213',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': '_ga=GA1.2.46511641.1610349553; _gid=GA1.2.2057611704.1610349553; Hm_lvt_23c29ef18f57ef3419152a651c437547=1610349553; _gat_gtag_UA_129654797_1=1; Hm_lpvt_23c29ef18f57ef3419152a651c437547=1610416707',
        'origin': 'https://tool.musicheng.com',
        'pragma': 'no-cache',
        'referer': 'https://tool.musicheng.com/exponent',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    data = {
        'token': 'badAxn8UY9gsq2U36BoynQ7UbDoMASv9mHQ14B2pAg8bGW2NbQYH%2b7NJ2CuyFlm0ZNn%2bJqGPrIeGM7O8GZ4NBkmCYcLoWbFQkJY0ZNY2H6NVB37l7GxUOGDINLf5L9T4L31vtPviRcI%3d',
        'sin': 'wx6872bcacd43026c8',
        'ver': 'v2',
        'search[]': '%.0f' %float(x),
        'type': '1',
    }
    while 1:
        try:
            res = requests.post(url,headers=headers,data=data)
            # print(res.text)
            extData = json.loads(res.text)['data'][0]
            break
        except:
            print('指数断线')
            time.sleep(3)
    return '%.0f' %float(extData)


def get_pay(x):
    if x == 0 or x == None:
        return 0
    url = 'https://tool.musicheng.com/exponent/calcult'
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-length': '213',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': '_ga=GA1.2.46511641.1610349553; _gid=GA1.2.2057611704.1610349553; Hm_lvt_23c29ef18f57ef3419152a651c437547=1610349553; _gat_gtag_UA_129654797_1=1; Hm_lpvt_23c29ef18f57ef3419152a651c437547=1610416707',
        'origin': 'https://tool.musicheng.com',
        'pragma': 'no-cache',
        'referer': 'https://tool.musicheng.com/exponent',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    data = {
        'token': 'badAxn8UY9gsq2U36BoynQ7UbDoMASv9mHQ14B2pAg8bGW2NbQYH%2b7NJ2CuyFlm0ZNn%2bJqGPrIeGM7O8GZ4NBkmCYcLoWbFQkJY0ZNY2H6NVB37l7GxUOGDINLf5L9T4L31vtPviRcI%3d',
        'sin': 'wx6872bcacd43026c8',
        'ver': 'v2',
        'search[]': '%.0f' %x,
        'type': '6',
    }
    while 1:
        try:
            res = requests.post(url, headers=headers, data=data)
            # print(res.text)
            extData = float(json.loads(res.text)['data'][0].replace('%',''))/100
            break
        except:
            print('指数断线')
            time.sleep(3)
    return '%.4f' %extData

# if __name__ == '__main__':
#     print(decrypt(''))