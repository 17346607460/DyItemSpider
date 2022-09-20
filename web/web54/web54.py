import requests
import base64

s = "6964KBYY54Eo8TZSVdsupHij+BWlI5owUQ2Pw9cqBSyw2pyJV4sS+n6k4n6IFu9wtIM,1606802560116"
# "Njk2NEtCWVk1NEVvOFRaU1Zkc3VwSGlqK0JXbEk1b3dVUTJQdzljcUJTeXcycHlKVjRzUytuNms0bjZJRnU5d3RJTSwxNjA2ODAyNTYwMTE2"

count = 0
for page in range(1, 101):
    url = 'https://www.python-spider.com/api/challenge54'
    headers = {
        'Host': 'www.python-spider.com',
        'Connection': 'keep-alive',
        'Content-Length': '21',
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
        'Referer': 'https://www.python-spider.com/challenge/54',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'Hm_lvt_337e99a01a907a08d00bed4a1a52e35d=1661408990; m=pua; sessionid=bnhbfupxy6fpf6adl6l27b85mxypysq7; iloveu=56166552d0c9bde9c1190c1bdd206296fba1ebbd; yuanrenxue34=N2Fza5Cs3d; Hm_lpvt_337e99a01a907a08d00bed4a1a52e35d=1662112394'
    }
    n = base64.b64encode(f'{page}'.encode())
    data = {
        'page': page,
        'token': f'{n.decode()}'
    }
    print(data)
    response = requests.post(url=url, headers=headers, data=data).json()
    print(response)
    for info in response['data']:
        count += int(info['value'].replace('\r', ''))
    print(count)