# -*- coding:utf-8 -*-
# @Author: clark
# @Time: 2020-02-11 18:05
# @File: cbndata.py
# @project demand:
import logging
import requests
import time
from pprint import pprint

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://z.cbndata.com/2019-nCoV/index.html',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
}
params = (
    ('timestamp', str(int(time.time() * 1000))),
)

i = 0
while True:
    response = requests.get(f'https://assets.cbndata.org/2019-nCoV/{i}/data.json', headers=headers, params=params)
    if response.json().get("data"):
        i += 1
        print(len(response.json()['data']))
        pprint(response.json()['data'][0])
        time.sleep(0.5)
        continue
    break
