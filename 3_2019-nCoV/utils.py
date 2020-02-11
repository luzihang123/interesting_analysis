# -*- coding:utf-8 -*-
# @Author: clark
# @Time: 2020-02-11 19:35
# @File: utils.py
# @project demand:
from hashlib import md5


def make_md5(text):
    '''
    计算md5指纹
    :param text:
    :return:
    '''
    if text:
        return md5(text.encode('utf-8')).hexdigest()
