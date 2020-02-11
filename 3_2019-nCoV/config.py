# -*- coding:utf-8 -*-
# @Author: clark
# @Time: 2020-02-11 18:46
# @File: config.py
# @project demand:配置文件
import os

MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_USER_NAME = os.getenv("MYSQL_USER_NAME", 'root')
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", '12345678')
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", 'interesting_analysis')
