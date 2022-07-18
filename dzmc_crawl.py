# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2021/7/21
# @Author: zengxinyue
# @File  : dzmc_crawl.py
import datetime
import re
import pandas as pd
from numpy import random
import requests
import pymysql
from fake_useragent import UserAgent
import json


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
        headers = {'user-agent': UserAgent().random}
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


def get_item_id(url):
    headers = {'Content-Type': 'application/json;charset=UTF-8',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/89.0.4389.128 Safari/537.36',
               'Accept': 'application/json, text/plain, */*',
               'Cookie': 'jfe_pin=cefad5d9; jfe_ts=1629709734.158; jfe_sn=nhXVVloAQB57twoCcQHFLvMnGL0=; Hm_lvt_139c628d'
                         'e301d6f3d54245fc7c8ba583=1629709737; Hm_lpvt_139c628de301d6f3d54245fc7c8ba583=1629711785'
                }
    page_number = 1
    items_id = []
    for i in range(0, 104):
        data = {'businessType': "1", 'cid': 1506, 'cids': [], 'homeType': "10",
                'orderColumn': "saleCount", 'orderType': "desc", 'publishType': "1",
                'queryPage': {'platformId': 20, 'pageSize': 28, 'pageNum': int(page_number)}, 'pageNum': 1, 'pageSize': 28,
                'platformId': 20}
        data1 = json.dumps(data)
        response = requests.post(url,
                                 headers=headers,
                                 data=data1).text
        temp = re.findall('"skuId":(.*?),"cid"', response)
        items_id += temp
        print('page ' + str(page_number))
        page_number += 1
    return items_id


def get_item_url(id):
    return 'https://mkt.zycg.gov.cn/mall-view/product/detail?skuid=' + id


def get_item_name(id):
    url1 = 'https://mkt.zycg.gov.cn/proxy/trade-service/commodity/detail/queryCommodityDetail?platformId=20&skuId=' + id
    response1 = requests.get(url1).text
    sku_name_list = re.findall('"skuName":"(.*?)","sellPrice":', response1)
    'https://mkt.zycg.gov.cn/proxy/trade-service/commodity/detail/queryCommodityDetail?platformId=20&skuId=1022344'
    sku_name = ''.join(sku_name_list)
    return sku_name


def get_item_suppliers(id):
    headers = {'Content-Type': 'application/json;charset=UTF-8',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/89.0.4389.128 Safari/537.36',
               'Accept': 'application/json, text/plain, */*',
               'Cookie': '_zcy_log_client_uuid=66c70590-fbdf-11eb-bd79-4b130334b582; aid=510104; districtCode=319900; '
                         'districtName=%E4%B8%8A%E6%B5%B7%E5%B8%82%E6%9C%AC%E7%BA%A7'
               }

    data = {'blacklistStatus': 0, 'publishType': 1, 'queryPage': {'platformId': 20, 'pageSize': 10, 'pageNum': 1},
            'pageNum': 1, 'pageSize': 10, 'platformId': 20, 'salesArea': "北京市", 'skuId': int(id)}
    data1 = json.dumps(data)
    response2 = requests.post('https://mkt.zycg.gov.cn/proxy/trade-service/mall/search/querySkuAgentListFromEs',
                              headers=headers, data=data1).text
    agent_names = re.findall('"agentName":"(.*?)","agentRank":', response2)
    supply_prices = re.findall('"supplyPrice":"(.*?)","blackListStatus":', response2)
    return {'供应商名称': agent_names, '单价（元)': supply_prices}


def get_item_params(id):
    url2 = 'https://mkt.zycg.gov.cn/proxy/trade-service/item/itemDetailController/queryItemSpecAttributesDetails?pl' \
           'atformId=20&skuId=' + id
    response3 = requests.get(url2).text
    params_name = re.findall('"name":"(.*?)","value":', response3)
    params_value = re.findall('"value":"(.*?)"', response3)
    general = re.findall('"desc":"(.*?)"', response3)
    return {'规格参数项': params_name, '参数值1': params_value, '参数值2': general}


def get_selling_record(id):
    url3 = 'https://mkt.zycg.gov.cn/proxy/trade-service/mall/order/querySkuSaleRecord?pageNum=1&pageSize=10&platfor' \
           'mId=20&skuId=' + id
    response4 = requests.get(url3).text
    organization_names = re.findall('"organizeName":"(.*?)","shopId":', response4)
    shop_names = re.findall('"shopName":"(.*?)","skuNum":', response4)
    sku_nums = re.findall('"skuNum":(.*?),"sellPrice":', response4)
    sell_prices = re.findall('"sellPrice":"(.*?)","orderTime":', response4)
    order_times = re.findall('"orderTime":"(.*?)"', response4)
    return {'采购单位': organization_names, '购买数量': sku_nums, '购买单价(元)': sell_prices, '供应商': shop_names,
            '成交日期': order_times}


def get_item_type(id):
    url4 = 'https://mkt.zycg.gov.cn/proxy/trade-service/item/itemDetailController/queryPlatformCategory?platform' \
           'Id=20&skuId=' + id
    response5 = requests.get(url4).text
    type = re.findall('"key":"(.*?)","value"', response5)
    return type[-1]


if __name__ == "__main__":
    # get a list of items' ids
    ids = get_item_id('https://mkt.zycg.gov.cn/proxy/trade-service/mall/search/searchByParamFromEs')
    # with open('ids.txt', 'w') as f:
    #     for i in range(len(ids)):
    #         f.write(str(ids[i]) + "\r")
    dff = pd.DataFrame()
    count = 0
    err_list = []
    for id in ids:
        count += 1
        try:
            url = get_item_url(id)
            sku_name = get_item_name(id)
            type = get_item_type(id)
            suppliers = get_item_suppliers(id)
            params = get_item_params(id)
            record = get_selling_record(id)
            df1 = pd.DataFrame({'序号': count, '商品链接': url, '商品名称': sku_name, '商品类型': type}, index=[0])
            df2 = pd.DataFrame(suppliers)
            df3 = pd.DataFrame(params)
            df4 = pd.DataFrame(record)
            df = pd.concat([df1, df2, df3, df4], axis=0)
            for i in range(1, df.shape[0]):
                df.iat[i, 0] = count
                df.iat[i, 1] = url
                df.iat[i, 2] = sku_name
                df.iat[i, 3] = type
            dff = dff.append(df)
        except:
            err_list.append(id)
            pass

    if err_list:
        print(err_list)
    dff.to_excel('seeerver.xlsx', index=False)