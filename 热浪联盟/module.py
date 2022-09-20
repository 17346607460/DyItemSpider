import time

from CurrencyModule import *
from Setting import *



class HeatWaveAlliance:
    def __init__(self):
        self.sql_server = SqlServerConnect()

    # 贝德美.dbo.热浪联盟_出佣总账_主播
    def heat_wave_alliance_anchor(self, start_day, cookie):
        _csrf = cookie.split('XSRF-TOKEN=')[1].split(';')[0]
        fileKey = self.get_fileKey(_csrf, start_day, cookie, 2)
        time.sleep(10)
        fileurl = self.get_fileurl(_csrf, fileKey, cookie)
        self.get_data(fileurl)
        file_paths = un_zip('1.zip')
        print(file_paths)
        for file_path in file_paths:
            print(file_path)
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0] == '账期':
                        continue
                    # print(row)
                    value = [start_day.replace('-', '')]
                    for i in row:
                        if not i:
                            i = None
                        if '-' == i:
                            i = None
                        if i:
                            if '%' in i:
                                try:
                                    i = round(float(i.replace('%', '')) / 100, 4)
                                except:
                                    i = 0
                        try:
                            i = i.replace('\t', '')
                        except:
                            pass
                        value.append(i)
                    self.sql_server.save_message("贝德美.dbo.热浪联盟_出佣总账_主播", [tuple(value[:-1])])
            os.remove(file_path)

    # 贝德美.dbo.热浪联盟_出佣总账_平台
    def heat_wave_alliance_platform(self, start_day, cookie):
        _csrf = cookie.split('XSRF-TOKEN=')[1].split(';')[0]
        fileKey = self.get_fileKey(_csrf, start_day, cookie, 1)
        time.sleep(10)
        fileurl = self.get_fileurl(_csrf, fileKey, cookie)
        self.get_data(fileurl)
        file_paths = un_zip('1.zip')
        print(file_paths)
        for file_path in file_paths:
            print(file_path)
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0] == '账期':
                        continue
                    # print(row)
                    value = []
                    for i in row:
                        if not i:
                            i = None
                        if '-' == i:
                            i = None
                        if i:
                            if '%' in i:
                                try:
                                    i = round(float(i.replace('%', '')) / 100, 4)
                                except:
                                    i = 0
                        try:
                            i = i.replace('\t', '')
                        except:
                            pass
                        value.append(i)
                    self.sql_server.save_message("贝德美.dbo.热浪联盟_出佣总账_平台", [tuple(value)])
            os.remove(file_path)

    def get_fileKey(self, _csrf, start_day, cookie, settleMode):
        url = f'https://hot.taobao.com/wallet/initDownload.do?_csrf={_csrf}'
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-length': '104',
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': cookie,
            'origin': 'https://hot.taobao.com',
            'referer': 'https://hot.taobao.com/hw/union/console/wallet?activeKey=1',
            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            'x-xsrf-token': _csrf
        }
        data = {
            'settleMode': f'{settleMode}',
            'settleType': 'normal',
            'type': '12',
            'endTime': f'{get_before_day(get_after_month(start_day) + "-01").replace("-", "")} 23:59:59',
            'startTime': f'{(start_day + "-01").replace("-", "")} 00:00:00',
        }
        response = requests.post(url=url, headers=headers, data=data).json()
        return response['data']['fileKey']

    def get_fileurl(self, _csrf, fileKey, cookie):
        url = f'https://hot.taobao.com/file/generateDownloadUrl.do?_csrf={_csrf}&fileKey={fileKey}'
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': cookie,
            'referer': 'https://hot.taobao.com/hw/union/console/wallet?activeKey=1',
            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            'x-xsrf-token': '6132bf62-5919-4efa-b70d-7a88a874a51a'
        }
        response = requests.get(url=url, headers=headers).json()
        return response['data']

    def get_data(self, url):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'tccp.oss-cn-zhangjiakou.aliyuncs.com',
            'Referer': 'https://hot.taobao.com/',
            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
        }
        response = requests.get(url=url, headers=headers).content
        with open('1.zip', 'wb')as w:
            w.write(response)
        w.close()



if __name__ == '__main__':
    hwa = HeatWaveAlliance()
    cookie = 't=ba991419abcabe60cd3884e42a2b30f4; cookie2=1d11a579ddc9331e331a8cbf42b950a2; _samesite_flag_=true; XSRF-TOKEN=6132bf62-5919-4efa-b70d-7a88a874a51a; cancelledSubSites=empty; v=0; unb=2212731641217; _m_h5_tk=a043c580eefebd2b7f87133c789bd2fa_1663125686721; _m_h5_tk_enc=78ac6456b5314a15dad7fba330d22ff1; sgcookie=E100Jf3nYEiSxxSJZn3MWiZNNII6LVKYfblCzQqiMZdnbD%2FfPpwo5AwQQpBMMCyLDyzXeF8ZFl4cbb9mwh9A%2Bkc8Kvfze1FwWP7UkgX0QY0I7og%3D; uc1=cookie21=W5iHLLyFfoaZ&cookie14=UoeyDbouLRXgog%3D%3D; sn=%E8%B4%9D%E5%BE%B7%E7%BE%8E%E6%97%97%E8%88%B0%E5%BA%97%3A%E9%BE%99%E9%A3%9E; csg=496547b7; skt=1f7ebd633c71224b; _cc_=WqG3DMC9EA%3D%3D; _tb_token_=335bd363777bb; cna=nWYbGpuKHDsCAXkEs3F2iXa2; l=eB_anV6cgpC-ROuFBO5Zhurza7793COjCsPzaNbMiInca1zhfU_t4NCE0sxBddtjgt5fxeKPNKfZAdUer-UT5xT2JxtSxSvwrw96RF1..; tfstk=c4G1BNqDYGjs7VxQYRTebtZSqLZRBHb7ldZi5HWZ5I-hoQ_26s5ciJ5zVwSmniF4ky1..; isg=BIWF1LTZSiZSxmzLdz7aQxmOlMG_QjnUe6B0IofvU7zCHrCQTpdIpqW4KELoXlGM'
    hwa.heat_wave_alliance_anchor('2022-08', cookie)
    hwa.heat_wave_alliance_platform('2022-08', cookie)