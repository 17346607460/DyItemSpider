import requests
from selenium import webdriver


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
    driver.execute_script(open(r"C:\Users\lianqinglongfei\Desktop\DyItemSpider\web\web60\web60.js", encoding="utf8").read())
    return driver


def get_token(browser, num):
    msg = browser.execute_script("return window.l('{}')".format(num))
    return msg


browser = init_browser()
number = 0
for i in range(1, 101):
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-length': '6',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': 'Hm_lvt_337e99a01a907a08d00bed4a1a52e35d=1660720700; iloveu=be6b8be9c57945ee16dffa04ca76adb3c3ffbc35; yuanrenxue34=f4hqxnDzc2; sessionid=afft6j6j5dxsis4vhauqzo5jbuj8elkw; Hm_lpvt_337e99a01a907a08d00bed4a1a52e35d=1661337100',
        'origin': 'https://www.python-spider.com',
        'pragma': 'no-cache',
        'referer': 'https://www.python-spider.com/challenge/60',
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    data = {
        'page': i
    }
    token = get_token(browser, i)
    print(token)
    url = f'https://www.python-spider.com/api/challenge60/{token}'
    response = requests.post(url=url, headers=headers, data=data).json()
    datas = response['data']
    for data in datas:
        number += int(data['value'].replace(r'\r', ''))
    print(number)