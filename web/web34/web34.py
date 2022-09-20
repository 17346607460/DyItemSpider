import execjs
import requests
from lxml import etree

session = requests.session()

url = 'https://www.python-spider.com/challenge/34'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'Hm_lvt_337e99a01a907a08d00bed4a1a52e35d=1660720700; sessionid=we0ne7owxecbfcgolbcj05f2zyi3ppdx; Hm_lpvt_337e99a01a907a08d00bed4a1a52e35d=1661243477; yuanrenxue34=DU6x2oHdla;',
    'Host': 'www.python-spider.com',
    'Pragma': 'no-cache',
    'Referer': 'https://www.python-spider.com/challenge/34',
    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': 'Windows',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
}

response = session.get(url=url, headers=headers, verify=False)
yrx34 = dict(response.cookies)['yuanrenxue34']
rnns = str(response.text.split(r'In2s\"=""*/=')[1].split('\n')[0]).replace('"', '')
rind = response.text.split(r'*//**//**/')[1].split('//FDi5u')[0]
with open(r'/web/web34/web34_1.js', 'r', errors='ignore') as r:
    b = r.read()
iloveu = execjs.compile(b).call('get_iloveu', rind, rnns, yrx34)
headers['Cookie'] = headers['Cookie'] + '' + iloveu
response = session.get(url=url, headers=headers, verify=False).text
# print(response)
html = etree.HTML(response)
tds = html.xpath('//td//text()')
value = 0
for td in tds:
    value += int(td.replace('\n', '').replace(' ', ''))
    print(int(td.replace('\n', '').replace(' ', '')))
print(value)
