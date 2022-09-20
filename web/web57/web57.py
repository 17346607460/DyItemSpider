import execjs
import requests


num = 0
for i in range(1,101):
    url = 'https://www.python-spider.com/api/challenge57'
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-length': '6',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': 'Hm_lvt_337e99a01a907a08d00bed4a1a52e35d=1660720700; sessionid=we0ne7owxecbfcgolbcj05f2zyi3ppdx; iloveu=be6b8be9c57945ee16dffa04ca76adb3c3ffbc35; yuanrenxue34=f4hqxnDzc2; Hm_lpvt_337e99a01a907a08d00bed4a1a52e35d=1661248695',
        'origin': 'https://www.python-spider.com',
        'pragma': 'no-cache',
        'referer': 'https://www.python-spider.com/challenge/57',
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
    response = requests.post(url=url, headers=headers, data=data).json()
    print(response)
    with open(r'C:\Users\lianqinglongfei\Desktop\DyItemSpider\web\web57\web57.js', 'r', errors='ignore') as r:
        b = r.read()
    values = execjs.compile(b).call('get_values', response)
    for value in values:
        num += int(value['value'].replace('\r', ''))
print(num)