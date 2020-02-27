# -*- coding:utf-8 -*-
# @Author: clark
# @Time: 2020-02-27 15:24
# @File: create_table.py
# @project demand:建表，模型类
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


class KlineDayTables(Base):
    '''
    日线行情
    '''
    __tablename__ = 'kline_day'
    # 交易日
    state_dt = Column(DateTime, primary_key=True, nullable=False, comment="交易日")
    # 股票代码
    stock_code = Column(String(length=255), primary_key=True, nullable=False, comment="股票代码")
    # 开盘价
    open = Column(DECIMAL(20, 2), default=None, comment="开盘价")
    # 收盘价
    close = Column(DECIMAL(20, 2), default=None, comment="收盘价")
    # 最高价
    high = Column(DECIMAL(20, 2), default=None, comment="最高价")
    # 最低价
    low = Column(DECIMAL(20, 2), default=None, comment="最低价")
    # 成交量
    vol = Column(DECIMAL(30, 2), default=None, comment="成交量")
    # 成交额
    amount = Column(DECIMAL(30, 2), default=None, comment="成交额")
    # 前日收盘价
    pre_close = Column(DECIMAL(20, 2), default=None, comment="前日收盘价")
    # 涨跌额
    amt_change = Column(DECIMAL(20, 2), default=None, comment="涨跌额")
    # 涨跌幅
    pct_change = Column(DECIMAL(20, 2), default=None, comment="涨跌幅")

    # 创建时间
    create_time = Column(DateTime, default=datetime.datetime.now, comment="创建时间")
    # 更新时间
    update_time = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment="更新时间")
    __table_args__ = ({'comment': 'A股日线行情'})  # 添加表注释


if __name__ == '__main__':
    # 创建数据表
    KlineDayTables.metadata.create_all(engine)
