# -*- coding:utf-8 -*-
# @Author: clark
# @Time: 2019-11-01 19:09
# @File: 2、exchange_alexa.py
# @project demand:交易所网站历史Alexa流量数据
# api 文档 https://docs.aws.amazon.com/AlexaWebInfoService/latest/ApiReference_TrafficHistoryAction.html
import csv
import time

from myawis import *
import os
from decimal import Decimal


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
        data_soup = self.awis_obj.traffichistory(domain=top_domain, myrange=my_range, start=start_time)
        return data_soup

    def parse_data(self, data_soup, exchange_name, top_domain):
        '''
        解析数据
        :return:
        '''
        data_list = data_soup.find_all(name="Data")
        for data_row in data_list:
            item = dict()
            item['exchange_name'] = exchange_name
            item['website'] = top_domain
            item['date'] = data_row.Date.string
            item['timestamp'] = self.make_timestamp(data_row.Date.string, "%Y-%m-%d") + 28800
            item['alexa_pageviews_permillion'] = Decimal(
                data_row.find(name='PageViews').find(name='PerMillion').string) if data_row.find(
                name='PageViews').find(name='PerMillion').string else None
            item['alexa_pageviews_peruser'] = Decimal(
                data_row.find(name='PageViews').find(name='PerUser').string) if data_row.find(
                name='PageViews').find(name='PerUser').string else None
            item['alexa_rank'] = int(data_row.find(name='Rank').string) if data_row.find(
                name='Rank').string else None
            item['alexa_reach_permillion'] = Decimal(
                data_row.find(name="Reach").find(name="PerMillion").string) if data_row.find(
                name="Reach").find(name="PerMillion").string else None
            yield item

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

    @staticmethod
    def make_timestamp(time_raw, time_format):
        """
        注意：time_raw 如果是0时区的时间，则需对结果时间戳 +28800; 如果是+8时区时间，则无需额外操作。
        :param time_raw:
        :param time_format:
        :return:
        """
        timestamp = int(time.mktime(time.strptime(time_raw, time_format)) - time.altzone) - 28800
        return timestamp

    @staticmethod
    def write_csv(file_location, item):
        '''
        用于将scrapy的item，循环写成csv
        :param file_location:
        :param item:
        :return:
        '''
        if not os.path.exists(file_location) or not os.path.getsize(file_location):
            with open(file_location, 'a+', encoding='utf-8') as csv_file:
                # with open(file_location, 'a+', newline='',encoding='utf-8') as csv_file:
                headers = list(item.keys())
                writer = csv.DictWriter(csv_file, fieldnames=headers)
                writer.writeheader()
                writer.writerow(item)
        else:
            with open(file_location, 'r', encoding='utf-8') as csv_file:
                reader = csv.reader(csv_file)
                headers = next(reader)
            with open(file_location, 'a+', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=headers)
                writer.writerow(item)


if __name__ == '__main__':
    alexa = ExchangeAlexa()
    exchange_list = [
        {"top_domain": "binance.com", "exchange_name": "币安"},
        {"top_domain": "coinbase.com", "exchange_name": "CoinBase"},
        {"top_domain": "hbg.com", "exchange_name": "火币"},
        {"top_domain": "okex.com", "exchange_name": "Okex"},
        {"top_domain": "bitmex.com", "exchange_name": "bitmex"},
        {"top_domain": "mxc.com", "exchange_name": "抹茶"},
    ]
    for exchange in exchange_list:
        data_soup = alexa.traffic_history(top_domain=exchange['top_domain'], my_range=31, start_time=20191001)
        for item in alexa.parse_data(data_soup=data_soup,
                                     exchange_name=exchange['exchange_name'],
                                     top_domain=exchange['top_domain']):
            print(item)
            alexa.write_csv('exchange_alexa.csv', item)
