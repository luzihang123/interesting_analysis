# -*- coding:utf-8 -*-
# @Author: clark
# @Time: 2020-02-11 19:28
# @File: insert_data.py
# @project demand:插入数据
from collections import Counter

from sqlalchemy import func

from create_table import CBNdataTables
from create_table import Session
import time

from utils import make_md5
import logging


class HandleCbnData(object):
    def __init__(self):
        # 实例化session信息
        self.mysql_session = Session()
        # self.date = time.strftime("%Y-%m-%d",time.localtime())
        self.date = '2020-02-10'

    # 数据的存储方法
    def insert_item(self, item):
        # 存储的数据结构
        logging.info(item)
        hash_value = make_md5(f"{item.get('province')}"
                              f"{item.get('city')}"
                              f"{item.get('district')}"
                              f"{item.get('address')}"
                              f"{item.get('longitude')}"
                              f"{item.get('latitude')}"
                              )
        data = CBNdataTables(
            # 省份
            province=item.get('province'),
            # 城市
            city=item.get('city'),
            # 行政区
            district=item.get('district'),
            # 地址
            address=item.get('address'),
            # 经度
            longitude=item.get('longitude'),
            # 纬度
            latitude=item.get('latitude'),
            # 确诊数量
            count=item.get('count'),
            # 去重hash值
            hash_value=hash_value,
        )

        # 在存储数据之前，先来查询一下表里此地理位置是否有这条疫情信息
        query_result = self.mysql_session.query(CBNdataTables).filter(
            CBNdataTables.hash_value == hash_value, CBNdataTables.count == item['count']).first()
        # 是否存在 地理位置相同，确诊数量更新的情况
        judge_update = self.mysql_session.query(CBNdataTables).filter(CBNdataTables.hash_value == hash_value,
                                                                      CBNdataTables.count != item['count']).first()
        # 疫情已存在
        if query_result:
            logging.info(f'该疫情信息已存在{item}')
        # 更新or新增确诊
        else:
            # 更新
            if judge_update:
                self.mysql_session.query(CBNdataTables).filter(CBNdataTables.hash_value == hash_value,
                                                               CBNdataTables.count != item['count']).update(
                    {'count': item['count'], 'update_time': time.localtime()}
                )
                self.mysql_session.commit()
                logging.info(f"更新疫情信息{item}")
            # 新增
            else:
                self.mysql_session.add(data)
                self.mysql_session.commit()
                logging.info(f'新增疫情信息{item}')


cbn_mysql = HandleCbnData()
