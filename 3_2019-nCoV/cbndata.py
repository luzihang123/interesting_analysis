# -*- coding:utf-8 -*-
# @Author: clark
# @Time: 2020-02-11 18:05
# @File: cbndata.py
# @project demand:
import logging
from json import JSONDecodeError

import requests
import time

from insert_data import cbn_mysql
import json

logging.basicConfig(level=logging.INFO, datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class HandleCbndata(object):
    def __init__(self):
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://z.cbndata.com/2019-nCoV/index.html',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        }

        self.params = (
            ('timestamp', str(int(time.time() * 1000))),
        )
        self.api_url = "https://assets.cbndata.org/2019-nCoV/{}/data.json"

    def handle_request(self, url):
        '''
        发请求
        '''
        response = requests.get(url,
                                headers=self.headers,
                                params=self.params
                                )
        return response.text

    def handle_cbndata(self):
        '''
        处理数据
        '''
        i = 0
        while True:
            cbn_response = self.handle_request(url=self.api_url.format(i))
            try:
                json_data = json.loads(cbn_response)
                if json_data.get("data"):
                    i += 1
                    for item in json_data['data']:
                        # 插入数据库
                        cbn_mysql.insert_item(dict(item))
                    time.sleep(0.5)
                    continue
                break
            # 数据遍历完，返回值不是json
            except JSONDecodeError as e:
                logging.info(f"JSONDecodeError:{e},返回非json数据:{cbn_response}")
                break
            # 捕获其他异常
            except Exception as e:
                logging.error(f"异常:{e}")
                break


def main():
    cbn = HandleCbndata()
    cbn.handle_cbndata()


if __name__ == '__main__':
    main()
