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



# https://jzt.jd.com/gw/ 精准通账号密码
jzt_user = "贝德美官方旗舰店"
jzt_password = "Beidemei@2021."


# https://ppzh.jd.com/brand/homePage/index.html
ppzh_user = 'gru33616540'
ppzh_password = 'bdm123456'

ppzh_user1 = '杭州赫尔罗母婴'
ppzh_password1 = 'bdm123456'

# https://shop.jd.com/
sz_user = '贝德美-练庆龙飞'
sz_password = 'lqlf6228998'


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

    def jzt_login(self):
        first_page_url = "https://jzt.jd.com/gw/"
        self.driver.get(url=first_page_url)
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[1]/div/div/div/div[7]/div/a[2]')))
        self.driver.find_element_by_xpath('/html/body/div/div/div[1]/div/div/div/div[7]/div/a[2]').click()
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div/div[2]/div/iframe")))
        iframe = self.driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div[2]/div/iframe")
        # print(iframe)
        self.driver.switch_to.frame(iframe)
        self.driver.find_element_by_xpath('/html/body/form/div/div/div/div[1]/div/input').send_keys(jzt_user)
        self.driver.find_element_by_xpath('/html/body/form/div/div/div/div[2]/div/input').send_keys(jzt_password)
        self.driver.find_element_by_xpath('//*[@id="paipaiLoginSubmit"]').click()
        while True:
            time.sleep(1)
            img_data = self.driver.find_element_by_xpath('/html/body/div/div/div/div/div[1]/div[2]/div[1]/img').get_attribute('src').split(',')[1]
            imgdata = base64.b64decode(img_data)
            file = open('jd.png', 'wb')
            file.write(imgdata)
            file.close()
            im = Image.open("jd.png")
            image_data = np.array(im)
            image_msg = image_data[0][0].tolist()
            move_px = (int(self.get_image_path(image_msg, image_data))-1)*(281/360)
            print(move_px)
            # time.sleep(2)
            module = self.driver.find_element_by_xpath('//*[@id="JDJRV-wrap-paipaiLoginSubmit"]/div/div/div/div[2]/div[3]')
            y = module.location.get('y')
            print(y)
            x = (1920-281)/2
            y = (969-109.27)/2 + y + 50
            pyautogui.moveTo(x, y, duration=0.1)
            pyautogui.mouseDown()
            y += random.randint(9, 19)
            move1 = x + move_px * 1.1
            pyautogui.moveTo(move1, y+1, duration=0.3)
            move1 -= move_px * 0.1
            pyautogui.moveTo(move1, y-1, duration=0.6)
            time.sleep(0.1)
            pyautogui.mouseUp()
            time.sleep(3)
            try:
                title = self.driver.find_element_by_xpath('/html/body/div/div/div[1]/div/div/div/div[7]/div/span[1]').text
                print(title)
                if title == '贝德美官方旗舰店':
                    break
            except:
                pass
        cookies = self.driver.get_cookies()
        cookie = ''
        for i in cookies:
            cookie += i['name'] + '=' + i['value'] + '; '
        return cookie[:-2]

    def get_image_path(self, image_msg, ddd):
        dir_path = r"F:\Dy-Items\Daily_Task\日常\京东\京东滑块"
        files_path = os.listdir(dir_path)
        move_pxs = []
        for file_path in files_path:
            path = os.path.join(dir_path, file_path)
            image_info = Image.open(path)
            image_data = np.array(image_info)
            if image_msg == image_data[0][0].tolist():
                print(path)
                for index1, sss in enumerate(image_data):
                    for index, image in enumerate(image_data[index1]):
                        if list(image) != list(ddd[index1][index]):
                            print((index1, index), image.tolist(), ddd[index1][index].tolist())
                            move_pxs.append(index)
        return min(move_pxs)

    def jdsz_login(self):
        first_page_url = 'https://ppzh.jd.com/brand/homePage/index.html'
        self.driver.get(url=first_page_url)
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[1]/div/div/div[2]/a[5]')))
        self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div/div/div[2]/a[5]').click()
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/iframe")))
        iframe = self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/iframe")
        print(iframe)
        self.driver.switch_to.frame(iframe)
        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/a').click()
        self.driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[3]/div/form/div[1]/input').send_keys(ppzh_user)
        self.driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[3]/div/form/div[2]/input').send_keys(ppzh_password)
        self.driver.find_element_by_xpath('//html/body/div[2]/div[3]/div[3]/div/form/div[5]/div/a').click()
        while True:
            time.sleep(1)
            img_data = self.driver.find_element_by_xpath('/html/body/div/div/div/div/div[1]/div[2]/div[1]/img').get_attribute('src').split(',')[1]
            imgdata = base64.b64decode(img_data)
            file = open('jd.png', 'wb')
            file.write(imgdata)
            file.close()
            im = Image.open("jd.png")
            image_data = np.array(im)
            image_msg = image_data[0][0].tolist()
            move_px = int(self.get_image_path(image_msg, image_data))*(281/360)
            print(move_px)
            # time.sleep(2)
            module = self.driver.find_element_by_xpath('/html/body/div[2]')
            y = module.location.get('y')
            print(y)
            x = (1920-281)/2
            y = (969-109.27)/2 + y + 110
            pyautogui.moveTo(x, y, duration=0.1)
            pyautogui.mouseDown()
            y += random.randint(9, 19)
            move1 = x + move_px * 1.1
            pyautogui.moveTo(move1, y+1, duration=0.3)
            move1 -= move_px * 0.1
            pyautogui.moveTo(move1, y-1, duration=0.6)
            time.sleep(0.1)
            pyautogui.mouseUp()
            time.sleep(5)
            try:
                title = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[1]/div[2]/div/div[3]/div/span[2]').text
                print(title)
                # if title == 'gru33616540':
                break
            except:
                pass
        cookies = self.driver.get_cookies()
        cookie = ''
        for i in cookies:
            cookie += i['name'] + '=' + i['value'] + '; '
        return cookie[:-2]

    def jdsz_login1(self):
        first_page_url = 'https://ppzh.jd.com/brand/homePage/index.html'
        self.driver.get(url=first_page_url)
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[1]/div/div/div[2]/a[5]')))
        self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div/div/div[2]/a[5]').click()
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/iframe")))
        iframe = self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/iframe")
        print(iframe)
        self.driver.switch_to.frame(iframe)
        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/a').click()
        self.driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[3]/div/form/div[1]/input').send_keys(ppzh_user1)
        self.driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[3]/div/form/div[2]/input').send_keys(ppzh_password1)
        self.driver.find_element_by_xpath('//html/body/div[2]/div[3]/div[3]/div/form/div[5]/div/a').click()
        while True:
            time.sleep(1)
            img_data = self.driver.find_element_by_xpath('/html/body/div/div/div/div/div[1]/div[2]/div[1]/img').get_attribute('src').split(',')[1]
            imgdata = base64.b64decode(img_data)
            file = open('jd.png', 'wb')
            file.write(imgdata)
            file.close()
            im = Image.open("jd.png")
            image_data = np.array(im)
            image_msg = image_data[0][0].tolist()
            move_px = int(self.get_image_path(image_msg, image_data))*(281/360)
            print(move_px)
            # time.sleep(2)
            module = self.driver.find_element_by_xpath('/html/body/div[2]')
            y = module.location.get('y')
            print(y)
            x = (1920-281)/2
            y = (969-109.27)/2 + y + 110
            pyautogui.moveTo(x, y, duration=0.1)
            pyautogui.mouseDown()
            y += random.randint(9, 19)
            move1 = x + move_px * 1.1
            pyautogui.moveTo(move1, y+1, duration=0.3)
            move1 -= move_px * 0.1
            pyautogui.moveTo(move1, y-1, duration=0.6)
            time.sleep(0.1)
            pyautogui.mouseUp()
            time.sleep(5)
            try:
                title = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[1]/div[2]/div/div[3]/div/span[2]').text
                print(title)
                # if title == '杭州赫尔罗母婴':
                break
            except:
                pass
        cookies = self.driver.get_cookies()
        cookie = ''
        for i in cookies:
            cookie += i['name'] + '=' + i['value'] + '; '
        return cookie[:-2]

    def jm_login(self):
        first_page_url = 'https://shop.jd.com/'
        self.driver.get(url=first_page_url)
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[1]/div[2]')))
        self.driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div[2]').click()
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[2]/div[2]/iframe[1]')))
        iframe = self.driver.find_element_by_xpath("/html/body/div/div/div/div[2]/div[2]/iframe[1]")
        print(iframe)
        self.driver.switch_to.frame(iframe)
        # self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/a').click()
        self.driver.find_element_by_xpath('/html/body/form/div/div/div/div[1]/div/input').send_keys(sz_user)
        self.driver.find_element_by_xpath('/html/body/form/div/div/div/div[2]/div/input').send_keys(sz_password)
        self.driver.find_element_by_xpath('/html/body/form/div/div/div/div[5]/input').click()
        while True:
            time.sleep(1)
            img_data = self.driver.find_element_by_xpath('/html/body/div/div/div/div/div[1]/div[2]/div[1]/img').get_attribute('src').split(',')[1]
            imgdata = base64.b64decode(img_data)
            file = open('jd.png', 'wb')
            file.write(imgdata)
            file.close()
            im = Image.open("jd.png")
            image_data = np.array(im)
            image_msg = image_data[0][0].tolist()
            move_px = int(self.get_image_path(image_msg, image_data))*(281/360)
            print(move_px)
            x = 1210
            y = (969-109.27)/2 + 20
            pyautogui.moveTo(x, y, duration=0.1)
            pyautogui.mouseDown()
            y += random.randint(9, 19)
            move1 = x + move_px * 1.1
            pyautogui.moveTo(move1, y+1, duration=0.3)
            move1 -= move_px * 0.1
            pyautogui.moveTo(move1, y-1, duration=0.6)
            time.sleep(0.1)
            pyautogui.mouseUp()
            time.sleep(3)
            try:
                title = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[2]/div[3]/span').text
                print(title)
                if title == '贝德美-练庆龙飞':
                    break
            except:
                pass
        cookies = self.driver.get_cookies()
        cookie = ''
        for i in cookies:
            cookie += i['name'] + '=' + i['value'] + '; '
        return cookie[:-2]


if __name__ == '__main__':
    chrome = ChromeOption()
    # print(chrome.jzt_login())
    # print(chrome.jm_login())
