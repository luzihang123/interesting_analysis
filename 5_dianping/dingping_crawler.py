# -*- coding:utf-8 -*-
# @Author: clark
# @Time: 2020-11-19 15:41
# @File: dingping_crawler.py
# @project demand:大众点评爬虫
'''

'''
# !/usr/bin/env python
# encoding: utf-8

import requests
import re
import csv
from urllib.parse import quote, unquote
from fontTools.ttLib import TTFont
from lxml import etree

kw = "大虾"
page = 3
data_url = "https://www.dianping.com/search/keyword/166/0_{}/p{}".format(quote(kw), page)
css_url = "https://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/fd7c8f441ff6bd0a2ccf4b4af81ec2f5.css"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    # 这里使用的是登录成功后的cookie值，完成翻页
    "cookie": "_hc.v=7ff743b7-eed7-b595-a51d-77dab3a759f9.1597040385; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1597040385; _lxsdk_cuid=1714304d906c8-0bd58ff3884e5b-396d7f06-1fa400-1714304d90626; _lxsdk=1714304d906c8-0bd58ff3884e5b-396d7f06-1fa400-1714304d90626; s_ViewType=10; ua=%E5%90%AF%E8%88%AA8; ctu=34fb7d109b3aa6800a3dc60f917ca960a230a3c6dd7469a4c9bcdfff3af52c25; cy=1; cye=shanghai; fspop=test; Hm_lvt_4c4fc10949f0d691f3a2cc4ca5065397=1605693819; Hm_lpvt_4c4fc10949f0d691f3a2cc4ca5065397=1605769140; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1603677445,1605693800,1605752161,1605771582; lgtoken=0c8e86b12-2200-4daa-91c9-593344e7be32; ll=7fd06e815b796be3df069dec7836c3df; dplet=0c500d140436701766916ce197e32305; dper=d191f60dcb2c07e6588a391eac0fe88745eb9696cc15eb1a2528dd5935d958ce3cb78691414027f67f7f70e9c725151810f45d5eb437ce17c3f11feac48b0c6884c8a3611b2462365936a60b5b01f2119d6868a85f6f211e7477b3723712504b; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1605773976; _lxsdk_s=175df4c77a3-a00-753-3b2%7C%7C118"
}


def read_word_string():
    with open("word_string.txt", "r", encoding="utf-8") as file:
        return file.read()


def parse_url(url):
    """解析url得到字节"""
    response = requests.get(url=url, headers=headers)
    return response.content


def parse_html(html):
    """使用xpath解析html，返回xpath对象"""
    etree_obj = etree.HTML(html)
    return etree_obj


def save_woff():
    """保存woff文件"""
    content = parse_url(css_url).decode("utf-8")
    woff_url_list = re.findall(
        r'url\("(//s3plus\.meituan\.net/v1/mss_73a511b8f91f43d0bdae92584ea6330b/font/\w+?\.woff)"\)', content)
    woff_url_list = map(lambda x: "https:" + x, woff_url_list)
    for woff_url in woff_url_list:
        content = parse_url(woff_url)
        filepath = woff_url.split("/")[-1]
        with open(filepath, "wb") as file:
            file.write(content)
    print("保存成功！")


def get_word(name, key):
    """读取指定的woff得到字体"""
    word = None
    if name == "tagName":
        woff_name = "732b648f.woff"
    elif name == "shopNum":
        woff_name = "27505d98.woff"
    elif name == "address":
        woff_name = "72f0c501.woff"
    tag = TTFont(woff_name)
    order_list = tag.getGlyphOrder()
    index = order_list.index(key)
    word = word_string[index - 2]

    return word


def get_data():
    """获取数据"""
    html = parse_url(data_url).decode("utf-8")
    html = re.sub(r"&#x(\w+?);", r"*\1*", html)  # 替换特殊字符，避免解析css加密数据获取后是unicode字符串
    xpath_obj = parse_html(html)
    li_list = xpath_obj.xpath('//*[@id="shop-all-list"]/ul/li')

    for li in li_list:
        item = {}
        item["shop_url"] = li.xpath("./div[1]/a/@href")[0]  # 店铺的url
        item["shop_img_url"] = li.xpath("./div[1]/a/img/@src")[0]  # 店铺图片的url
        item["shop_name"] = li.xpath("./div[1]/a/img/@title")[0]  # 店铺名称

        star_class = li.xpath('.//*[@class="star_icon"]/span[1]/@class')[0]
        item["shop_star"] = star_class.split(" ")[1].split("_")[-1]  # 店铺评分

        class_name = li.xpath('./div[2]/div[2]/a[1]/b/svgmtsi/@class')
        if class_name:  # 有加密
            class_name = class_name[0]
            item["shop_comment_num"] = "".join(
                [get_word(class_name, "uni" + i.strip("*")) if (i.startswith("*") and i.endswith("*")) else i for i in
                 li.xpath('./div[2]/div[2]/a[1]/b//text()')])
        else:  # 没有加密
            item["shop_comment_num"] = "".join(li.xpath('./div[2]/div[2]/a[1]/b//text()'))  # 评论数

        class_name = li.xpath('./div[2]/div[2]/a[2]/b/svgmtsi/@class')
        if class_name:  # 有加密
            class_name = class_name[0]
            item["shop_avg_money"] = "".join(
                [get_word(class_name, "uni" + i.strip("*")) if (i.startswith("*") and i.endswith("*")) else i for i in
                 li.xpath('./div[2]/div[2]/a[2]/b//text()')])
        else:  # 没有加密
            item["shop_avg_money"] = "".join(li.xpath('./div[2]/div[2]/a[2]/b//text()'))  # 人均消费

        class_name = li.xpath('./div[2]/div[3]/a[1]/span/svgmtsi/@class')
        if class_name:
            class_name = class_name[0]
            item["shop_type"] = "".join(
                [get_word(class_name, "uni" + i.strip("*")) if (i.startswith("*") and i.endswith("*")) else i for i in
                 li.xpath('./div[2]/div[3]/a[1]/span//text()')])
        else:
            item["shop_type"] = "".join(li.xpath('./div[2]/div[3]/a[1]/span//text()'))

        class_name = li.xpath('./div[2]/div[3]/a[2]/span/svgmtsi/@class')
        if class_name:
            class_name = class_name[0]
            item["shop_address1"] = "".join(
                [get_word(class_name, "uni" + i.strip("*")) if (i.startswith("*") and i.endswith("*")) else i for i in
                 li.xpath('./div[2]/div[3]/a[2]/span//text()')])  # 区域地址
        else:
            item["shop_address1"] = "".join(li.xpath('./div[2]/div[3]/a[2]/span//text()'))

        class_name = li.xpath('./div[2]/div[3]/span[1]/svgmtsi/@class')
        if class_name:
            class_name = class_name[0]
            item["shop_address2"] = "".join(
                [get_word(class_name, "uni" + i.strip("*")) if (i.startswith("*") and i.endswith("*")) else i for i in
                 li.xpath('./div[2]/div[3]/span[1]//text()')])
        else:
            item["shop_address2"] = "".join(li.xpath('./div[2]/div[3]/span[1]//text()'))  # 详细地址
        print(item)
        save(item)


def save(item):
    """将数据保存到csv中"""
    with open("./大众点评-{}.csv".format(kw), "a", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(item.values())


if __name__ == '__main__':
    # save_woff()
    word_string = read_word_string()
    get_data()
