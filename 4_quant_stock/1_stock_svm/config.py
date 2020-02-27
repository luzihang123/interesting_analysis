# -*- coding:utf-8 -*-
# @Author: clark
# @Time: 2020-02-27 15:25
# @File: config.py
# @project demand:配置

import os

# tushare pro 专业版token
TUSHARE_TOKEN = os.getenv("TUSHARE_TOKEN", "")

MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_USER_NAME = os.getenv("MYSQL_USER_NAME", 'root')
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", '12345678')
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", 'stock')
