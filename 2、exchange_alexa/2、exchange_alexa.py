# -*- coding:utf-8 -*-
# @Author: clark
# @Time: 2019-11-01 19:09
# @File: 2、exchange_alexa.py
# @project demand:交易所网站历史Alexa流量数据
# api 文档 https://docs.aws.amazon.com/AlexaWebInfoService/latest/ApiReference_TrafficHistoryAction.html

from myawis import *
import os


class ExchangeAlexa(object):
    def __init__(self):
        # 获取 Alexa Web Information Service 对象,从环境变量获取秘钥
        # 文档：https://docs.aws.amazon.com/AlexaWebInfoService/latest/MakingRequestsChapter.html
        self.awis_obj = CallAwis(os.getenv('Access_Key_ID'), os.getenv('Secret_Access_Key'))

    def traffic_history(self, top_domain, my_range, start_time):
        '''
        获取历史流量数据
        :param domain:
        :param total_history_days:
        :param first_start_int:
        :return:
        '''
        _data = self.awis_obj.traffichistory(domain=top_domain, myrange=my_range, start=start_time)
        return _data

    def parse(self):
        '''
        解析数据
        :return:
        '''
        pass

    def get_start_int_list(self):
        '''
        计算每一次请求的start，间隔默认31天（self.my_range）
        :return:
        '''
        pass

    def get_first_start_int(self):
        '''
        指定爬虫开始时的第一个start 时间， 默认今天的日期,格式int。之后一直递减。
        :return:
        '''
        pass


if __name__ == '__main__':
    alwxa = ExchangeAlexa()
    data_raw = alwxa.traffic_history(top_domain='cctv.com', my_range=31, start_time=20190801)
    print(data_raw)
