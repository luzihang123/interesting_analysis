# -*- coding:utf-8 -*-
# @Author: clark
# @Time: 2020-02-13 13:41
# @File: schedule.py
# @project demand:schedule job
from apscheduler.schedulers.blocking import BlockingScheduler
from cbndata import main as cbn_main
import pytz
import time
import os
import logging

tz = pytz.timezone('Asia/Shanghai')
time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 5))
START_DATE = os.getenv('START_DATE', time_str)

# 实例化一个调度器
scheduler = BlockingScheduler()
# 添加任务并设置触发方式为间隔 5 min 一次
logging.info(f"调度器首次启动时间:{time_str}")
scheduler.add_job(cbn_main, 'interval', seconds=60 * 5, start_date=START_DATE, max_instances=2, timezone=tz)
# 开始运行调度器
scheduler.start()
