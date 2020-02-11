# -*- coding:utf-8 -*-
# @Author: clark
# @Time: 2020-02-11 18:38
# @File: create_table.py
# @project demand:
from sqlalchemy import create_engine, Integer, String, Float, DateTime, DECIMAL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from config import *
import datetime

# 创建数据库的连接
engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER_NAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4")
# 操作数据库，需要我们创建一个session
Session = sessionmaker(bind=engine)
# 声明一个基类
Base = declarative_base()


class CBNdataTables(Base):
    '''
    CBNdata 数据结构
     {
        "province": "云南省",
        "city": "玉溪市",
        "district": "红塔区",
        "address": "云南省玉溪市红塔区北城街道大石板社区秧草塘村",
        "longitude": "102.51207",
        "latitude": "24.46442",
        "count": "2"
    },
    '''
    __tablename__ = 'CBN_data'
    # id,设置为主键和自动增长
    id = Column(Integer, primary_key=True, autoincrement=True, comment="id")
    # 省份
    province = Column(String(length=30), nullable=True, comment="省份")
    # 城市
    city = Column(String(length=30), nullable=True, comment="城市")
    # 行政区
    district = Column(String(length=30), nullable=True, comment="行政区")
    # 地址
    address = Column(String(length=100), nullable=True, comment="地址")
    # 经度
    longitude = Column(DECIMAL(20, 10), nullable=True, comment="经度")
    # 纬度
    latitude = Column(DECIMAL(20, 10), nullable=True, comment="纬度")
    # 确诊数量
    count = Column(String(length=10), nullable=True, comment="确诊数量")
    # 去重hash值:
    hash_value = Column(String(length=50), nullable=False, unique=True, comment="去重hash值")
    # 创建时间
    create_time = Column(DateTime, default=datetime.datetime.now, comment="创建时间")
    # 更新时间
    update_time = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment="更新时间")
    __table_args__ = ({'comment': 'CBNdata疫情地图数据'})  # 添加表注释


if __name__ == '__main__':
    # 创建数据表
    CBNdataTables.metadata.create_all(engine)
