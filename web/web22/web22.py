import random
import requests


url = 'https://www.python-spider.com/api/challenge22'
headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-length': '6',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'cookie': 'Hm_lvt_337e99a01a907a08d00bed4a1a52e35d=1663047488; sessionid=7ob42ha5l0tcdooceclp7olimcgii254; Hm_lpvt_337e99a01a907a08d00bed4a1a52e35d=1663135409; __yr_token__=b301cDDIFe2otWCxOUx1aYRM/KAx/DwxjCHU8GCNVNyxdGX0FT1cSTShdKAkkTCEeXx1qFHFMMSkhFmo9EB8JcgVzaB8bG0NRFyhDa1s6SQYoRCUkfH1ETAMTWAZYF3ZrXAZPABUMG3kJWQNBYRY=',
    'origin': 'https://www.python-spider.com',
    'pragma': 'no-cache',
    'referer': 'https://www.python-spider.com/challenge/22',
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
    'page': 2
}
print(requests.post(url=url, headers=headers, data=data).json())
