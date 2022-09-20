import time
import random
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import base64, os
from PIL import Image
import numpy as np



# https://customer.xiaohongshu.com/login?service=https://ark.xiaohongshu.com/ 小红书后台账号
xhs_user = "15606713079"
xhs_password = "beidemei2022"


class ChromeOption(object):
    def __init__(self):
        options = Options()
        # options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"')
        options.add_argument('User-Agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"')
        # options.add_argument("--disable-javascript")  # 禁止加载js
        # options.add_argument("--window-size=1366,768")  # 设置窗口大小
        options.add_argument("--start-maximized")       # 最大化
        # options.add_argument("--incognito")  # 隐身模式，无痕模式
        options.add_argument("--disable-infobars")  # 禁用浏览器正在被自动化程序控制的提示
        options.add_argument('lang=zh_CN.UTF-8')
        options.add_argument("--disable-blink-features=AutomationControlled")
        # options.add_argument('--disable-gpu')  # 禁用 gpu
        options.add_argument('--disable-infobars')  # 除去“正受到自动测试软件的控制”
        # options.set_headless()  # 无头浏览器
        # options.add_argument('--headless')  # 无头浏览器
        options.add_argument('--no-sandbox')  # 让 driver 在 root 权限下跑
        # options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('blink-settings=imagesEnabled=false')  # 禁止加载图片
        options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 打开开发者模式
        # options.add_argument("--auto-open-devtools-for-tabs")  # 打开 F12
        self.driver = webdriver.Chrome(options=options)

    def __del__(self):
        """ 关闭模拟器 """
        self.driver.close()
        print(111111111111111111111)

    def ks_login(self):
        first_page_url = 'https://s.kwaixiaodian.com/zone-origin/order/list'
        self.driver.get(url=first_page_url)
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[2]/div/div/div/div[2]/div[1]')))
        self.driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div/div/div[2]/div[1]').click()
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[2]/div/div/div/div[2]/div[2]')))
        self.driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div/div/div[2]/div[2]').click()
        self.driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div/div/div[4]/form/div[1]/div/div/span/input').send_keys(xhs_user)
        self.driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div/div/div[4]/form/div[2]/div/div/span/span/input').send_keys(xhs_password)
        self.driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div/div/div[4]/form/div[3]/button').click()
        time.sleep(5)
        cookies = self.driver.get_cookies()
        cookie = ''
        for i in cookies:
            cookie += i['name'] + '=' + i['value'] + '; '
        return cookie[:-2]

    def syt_login(self):
        first_page_url = 'https://kssyt.e.kuaishou.com/welcome'
        self.driver.get(url=first_page_url)
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/section/section/main/div/div/section[1]/div[2]/div[1]/a')))
        self.driver.find_element_by_xpath('/html/body/div/section/section/main/div/div/section[1]/div[2]/div[1]/a').click()
        # WebDriverWait(self.driver, 60).until(
        #     EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[2]/div/div/div/div[2]/div[2]')))
        # self.driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div/div/div[2]/div[2]').click()
        self.driver.find_element_by_xpath('/html/body/section/div/main/div/div/div[2]/div[2]/div[1]/div/div/input').send_keys(xhs_user)
        self.driver.find_element_by_xpath('/html/body/section/div/main/div/div/div[2]/div[2]/div[2]/div/div/input').send_keys(xhs_password)
        self.driver.find_element_by_xpath('/html/body/section/div/main/div/div/div[2]/div[2]/button').click()
        time.sleep(5)
        cookies = self.driver.get_cookies()
        cookie = ''
        for i in cookies:
            cookie += i['name'] + '=' + i['value'] + '; '
        return cookie[:-2]

    def cllp_login(self):
        first_page_url = 'https://luopan.e.kuaishou.com/login?redirectUrl=%2Fhome'
        self.driver.get(url=first_page_url)
        time.sleep(10)
        # WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div[2]/div/form/div[1]/div[1]/div/input')))
        # self.driver.find_element_by_xpath('/html/body/div/section/section/main/div/div/section[1]/div[2]/div[1]/a').click()
        # WebDriverWait(self.driver, 60).until(
        #     EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[2]/div/div/div/div[2]/div[2]')))
        # self.driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div/div/div[2]/div[2]').click()
        self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div/main/div/div/div/div[2]/div/form/div[1]/div[1]/div/input').send_keys(xhs_user)
        self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div/main/div/div/div/div[2]/div/form/div[2]/div/div/input').send_keys(xhs_password)
        self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div/main/div/div/div/div[2]/div/form/div[3]/div/label/span/input').click()
        self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div/main/div/div/div/div[2]/div/form/div[3]/button').click()
        time.sleep(5)
        cookies = self.driver.get_cookies()
        cookie = ''
        for i in cookies:
            cookie += i['name'] + '=' + i['value'] + '; '
        return cookie[:-2]


if __name__ == '__main__':
    chrome = ChromeOption()
    print(chrome.cllp_login())
