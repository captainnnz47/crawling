# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2021/7/21
# @Author: zengxinyue
# @File  : nb_server.py
import re
import pandas as pd
from numpy import random
import requests
import pymysql
from fake_useragent import UserAgent
import time


# connect to IP proxy server
def return_ip():
    conn = pymysql.connect(
        host="59.110.219.171",
        user="zgcindex",
        password="zgcprice2019",
        database="zdzs_proxy",
        charset="utf8",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )
    cur = conn.cursor()
    cur.execute('select * from proxy where status = 0')
    ip_list = cur.fetchall()
    return [x['ip_port'] for x in ip_list]


# get url using proxy server, random headers and specified cookies
def get_url(url, ip=1, headers=None):
    if headers is None:
        headers = {}
    if len(headers) > 0:
        headers = headers
    else:
        headers = {'user-agent': UserAgent().random,
                   'cookie': '_zcy_log_client_uuid=a6c0b7e0-f9a5-11eb-b27a-f579b3bce48f; aid=330102; tax=; platform_'
                             'code=zcy; wsid=1000489373#1629193610221; uid=10008331419; user_type=0601; tenant_code=0'
                             '01000; institution_id=1000500000; UM_distinctid=17b5381ae296-0f9a0b61b5c9fc-4343363-1440'
                             '00-17b5381ae2a228; SESSION=NTQyNjRiYjEtYTdmYS00YzdhLWE3ZDktODc5OTViNDhmMDU2; CNZZDATA125'
                             '9303436=1977974229-1629190157-%7C1629253112; districtCode=330299; districtName=%E5%AE%81'
                             '%E6%B3%A2%E5%B8%82%E6%9C%AC%E7%BA%A7; acw_tc=76b20ff016292553153838599e5a7fccb2da287dec3'
                             '8e8c7e02a8da2ac7c25; goodsId=268036; itemId=544534459800001; sellerId=100043491'}
    if ip == 1:
        ip_num = 0
        ip_list = []
        while ip_num == 0:
            ip_list = return_ip()
            if len(ip_list) >= 1:
                ip_num = 1

        ip = ip_list[random.randint(0, len(ip_list) - 1)]
        proxies = {
            "http": "http://{}".format(ip),
            "https": "http://{}".format(ip),
        }
        r = requests.get(url, verify=False, headers=headers, proxies=proxies, timeout=5)
    else:
        r = requests.get(url, verify=False, headers=headers, timeout=5)
    return r


def get_product_accessories_info(url, ip=0, err_num=0):
    try:
        err_num = err_num
        # get url content
        response = get_url(url, ip=ip).text
        # print(response)
        category = re.findall('<td style="word-break: break-all">(.*?)</td>', response)
        temp = re.findall('<tr data-all="{&quot;id&quot;(.*?)&quot;source&quot;:0}">', response, re.M)
        if not temp:
            return {}
        name = []
        brand = []
        mode = []
        market_price = []
        contract_price = []
        for item in temp:
            temp_name = re.findall('&quot;partName&quot;:&quot;(.*?)&quot;,&quot;brand&quot;:&quot;', item)
            names = ''.join(temp_name)
            name.append(names)
            temp_brand = re.findall('&quot;,&quot;brand&quot;:&quot;(.*?)&quot;,&quot;categoryId&quot;', item)
            brands = ''.join(temp_brand)
            brand.append(brands)
            temp_mode = re.findall('&quot;mode&quot;:&quot;(.*?)&quot;,&quot;unit&quot;', item)
            modes = ''.join(temp_mode)
            mode.append(modes)
            temp_market_price = re.findall('&quot;marketPrice&quot;:(.*?),&quot;agreementPrice&quot;:', item)
            market_prices = ''.join(temp_market_price)
            market_price.append(market_prices)
            temp_contract_price = re.findall('&quot;agreementPrice&quot;:(.*?),&quot;discountRate&quot;', item)
            contract_prices = ''.join(temp_contract_price)
            contract_price.append(contract_prices)
        return {'配件名称': name, '配件类别': category, '品牌': brand, '型号': mode, '市场价（元)': market_price,
                '协议单价(元)': contract_price}
    except:
        s = requests.session()
        s.keep_alive = False
        err_num += 1
        # maximum three-time requesting
        if err_num <= 5:
            time.sleep(1)
            res = get_product_info(url, ip=1, err_num=err_num)
        return res


def get_product_info(url, ip=1, err_num=0):
    try:
        err_num = err_num
        # get url content
        response = get_url(url, ip=ip).text
        # print(response)
        product_name = re.findall('&quot;name&quot;:&quot;(.*?)&quot;,&quot;mainImage&quot;', response)
        if not product_name:
            name = []
        else:
            name = product_name[0]
        product_price = re.findall('&quot;agreementPrice&quot;:&quot;(.*?)&quot;,&quot;projectId&quot;', response)
        if not product_price:
            price = []
        else:
            price = product_price[0]
        return [name, price]
    except:
        s = requests.session()
        s.keep_alive = False
        err_num += 1
        # maximum three-time requesting
        if err_num <= 5:
            time.sleep(1)
            res = get_product_info(url, ip=1, err_num=err_num)
        return res


if __name__ == "__main__":
    df_data = pd.read_excel(io='./Book1.xlsx')
    urls = df_data.values.tolist()
    dff = pd.DataFrame()
    err_url_list = []
    count = 0
    ac = []
    bc = []
    for url in urls:
        try:
            count += 1
            temp_url = str(url)[2:-2]
            basic_info = get_product_info(temp_url)
            accessories_info = get_product_accessories_info(temp_url)
            print(count, ':')
            if basic_info:
                df1 = pd.DataFrame({'产品链接': temp_url, '产品名称': basic_info[0], '产品价格': basic_info[1]}, index=[0])
            else:
                df1 = pd.DataFrame()
            df2 = pd.DataFrame(accessories_info)
            df = pd.concat([df1, df2], axis=0)
            dff = dff.append(df)
        except:
            err_url_list.append(str(url)[2:-2])
            pass
    print(err_url_list)
    dff.to_excel('result.xlsx', index=False)