import execjs, json
import requests

number = 0
for page in range(1, 101):
    url = 'https://www.python-spider.com/api/challenge21'
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-length': '6',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': 'Hm_lvt_337e99a01a907a08d00bed4a1a52e35d=1661408990; m=pua; sessionid=bnhbfupxy6fpf6adl6l27b85mxypysq7; iloveu=56166552d0c9bde9c1190c1bdd206296fba1ebbd; yuanrenxue34=N2Fza5Cs3d; Hm_lpvt_337e99a01a907a08d00bed4a1a52e35d=1662112907',
        'origin': 'https://www.python-spider.com',
        'pragma': 'no-cache',
        'referer': 'https://www.python-spider.com/challenge/55',
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    with open(r'C:\Users\lianqinglongfei\Desktop\DyItemSpider\web\web21\web21.js', 'r', errors='ignore') as r:
        b = r.read()
    signature = execjs.compile(b).call('get_msg')
    sign = signature[0]
    write_time = signature[1]
    data = {
        'page': page,
        's': sign,
        't': write_time
    }
    response = requests.post(url=url, headers=headers,data=data).json()
    print(response)
    for data in response['data']:
        number += int(data['value'].replace(r'\r', ''))
    print(number)