import time

import requests
from selenium import webdriver

def init_browser():
    """
    启动一个浏览器，提供 js 执行环境
    :return:
    """
    option = webdriver.ChromeOptions()
    # option.add_experimental_option("useAutomationExtension", False)
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # 链接当前浏览器
    # option.add_experimental_option("excludeSwitches", ['enable-automation'])
    option.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(chrome_options=option)
    # driver.get("https://www.python-spider.com/challenge/5")
    # driver.execute_script(open(r"C:\Users\lianqinglongfei\Desktop\DyItemSpider\web\web5\web5rpc.js", encoding="utf8").read())
    return driver

browser = init_browser()
def get_token(browser, num):
    msg = browser.execute_script('''call({})'''.format(num))
    return msg

def get_token1(browser):
    msg = browser.execute_script('''return window.datas''')
    return msg

number = 0
for i in range(1, 101):
    print(get_token(browser, i))
    time.sleep(3)
    values = get_token1(browser)
    print(values)
    for value in values:
        number += int(value['value'].replace(r'\r', ''))
    print(number, i)