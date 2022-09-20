import time

import requests


session = requests.session()
num = 0
for i in range(1, 101):
    url = 'https://www.python-spider.com/api/challenge59'
    session.headers.clear()
    session.headers.update({
        'Host': 'www.python-spider.com',
        'Connection': 'keep-alive',
        'Content-Length': '6',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
        'sec-ch-ua-platform': 'Windows',
        'Origin': 'https://www.python-spider.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.python-spider.com/challenge/59',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'Hm_lvt_337e99a01a907a08d00bed4a1a52e35d=1660720700; iloveu=be6b8be9c57945ee16dffa04ca76adb3c3ffbc35; yuanrenxue34=f4hqxnDzc2; sessionid=afft6j6j5dxsis4vhauqzo5jbuj8elkw; Hm_lpvt_337e99a01a907a08d00bed4a1a52e35d=1661332438'
    })
    data = {
        'page': str(i)
    }
    response = session.post(url=url, data=data).json()
    print(response)
    values = response['data']
    print(len(values))
    for value in values:
        num += int(value['value'].replace('\r', '').replace('5733', '5734'))
    print(i)
    print(num)

# 237549  5
# 1408275  29
# 2270549  46
# 4079573  82
