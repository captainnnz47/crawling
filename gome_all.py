#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: z
"""
import pandas as pd
import requests
import re
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/62.0.3202.62 Safari/537.36',
            'cookies': 'uid=Cjo0mGE1tldqKHfGF7UUAg==; cartnum=0_0-1_0; compare=; route=f9006be0eff9a077c15a34575456df4'
                       'e; ctx=app-shangcheng|ver-v7.0.0|plt-pc|cmpid-; _index_ad=0; sensorsdata2015jssdkcross=%7B%22d'
                       'istinct_id%22%3A%2217bb9d048eac2c-0fc9c7ac4833218-a7d193d-2073600-17bb9d048eb63c%22%2C%22first'
                       '_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%'
                       'E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC'
                       '_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_'
                       'id%22%3A%2217bb9d048eac2c-0fc9c7ac4833218-a7d193d-2073600-17bb9d048eb63c%22%7D; atgregion=7101'
                       '0400%7C%E5%9B%9B%E5%B7%9D%E7%9C%81%E6%88%90%E9%83%BD%E5%B8%82%E6%AD%A6%E4%BE%AF%E5%8C%BA%E6%A1'
                       '%82%E6%BA%AA%E8%A1%97%E9%81%93%7C71010000%7C71000000%7C710104018; DSESSIONID=4a672cf678e54d05'
                       'b870189ed475b3f1; _idusin=86490498356; gradeId=-1; s_cc=true; gpv_pn=no%20value; gpv_p22=no%20'
                       'value; s_sq=gome-prd%3D%2526pid%253Dhttps%25253A%25252F%25252Flist.gome.com.cn%25252Fcat100001'
                       '03-00-0-48-0-0-0-0-1-0-0-1-0-0-0-0-0-0.html%25253Fintcmp%25253Dlist-9000000600-11%2526oid%253D'
                       'https%25253A%25252F%25252Fitem.gome.com.cn%25252F9140081673-1122822116.html%25253Fintcmp%25253'
                       'Dlist-9000000700-1_1_1%252526search_id%25253DCATPL%2525401I2%2526ot%253DA; proid120517atg=%5B%2'
                       '2G001-fshop-9140081673-1122822116%22%2C%22G001-fshop-9140185416-1130749800%22%5D; s_getNewRepe'
                       'at=1631085217371-New; s_ppv=-%2C24%2C13%2C1869'
}


def get_item_url():
    page_no = 1
    url = 'https://list.gome.com.cn/cat10000054-00-0-48-0-0-0-0-1-0-0-1-0-0-0-0-0-0.html?intcmp=list-9000000600-11&page=' + str(page_no)
    response = requests.get(url, headers=headers, timeout=5).text
    temp = re.findall('<li class="product-item" skuid="(.*?)" pid="(.*?)">', response)
    urls = []
    for item in temp:
        url = 'https://item.gome.com.cn/' + item[1] + '-' + item[0] + '.html'
        urls.append(url)
    while 'skuid' in response:
        page_no += 1
        url = 'https://list.gome.com.cn/cat10000054-00-0-48-0-0-0-0-1-0-0-1-0-0-0-0-0-0.html?intcmp=list-9000000600-11&page=' + str(page_no)
        response = requests.get(url, headers=headers, timeout=5).text
        temp = re.findall('<li class="product-item" skuid="(.*?)" pid="(.*?)">', response)
        for item in temp:
            url = 'https://item.gome.com.cn/' + item[1] + '-' + item[0] + '.html'
            urls.append(url)
    return urls
#
# 'firstCategoryName:"电脑 办公打印 文仪",
# 	secondCategoryName:"外设产品",
# 	thirdCategoryName:"U盘",
# breadName:"金士顿",'


def item_content(url):

    response = requests.get(url, headers=headers, timeout=5).text
    flag = re.findall('<span class="identify">(.*?)</span>', response)
    if '自营' not in flag:
        return '非自营'
    first_c1 = ''.join(re.findall('firstCategoryName:"(.*?)"', response))
    second_c2 = ''.join(re.findall('secondCategoryName:"(.*?)"', response))
    third_c3 = ''.join(re.findall('thirdCategoryName:"(.*?)"', response))
    brand_name = ''.join(re.findall('breadName:"(.*?)"', response))

    name = ''.join(re.findall('<meta name="keywords" content="(.*?)">',  response))
    price = ''.join(re.findall('gomePrice:"(.*?)"', response))
    param1 = re.findall('<div class="guigecanshu" .*?>(.*?)</div>', response)
    param2 = ''.join(re.findall('<p class="pedtextbox_cont">(.*?)</p>', response))
    spxq = ''
    if param1 != []:
        for item in param1:
            item = str(item)
            temp = item.split('：')
            final = '"' + temp[0] + '"' + ':' + '"' + temp[1] + '"'
            spxq += final
    else:
        spxq = '无'

    bzqd = ''
    # if param2 != []:
    #     for item in param2:
    #         item = str(item)
    #         temp = item.split('：')
    #         final = '"' + temp[0] + '"' + ':' + '"' + temp[1] + '"'
    #         bzqd += final

    return {'商品链接': url, '一级': first_c1, '二级': second_c2, '三级': third_c3, '四级': brand_name,'产品名称':
        name, '价格': price, '商品详情': spxq, '包装清单': str(param2)}

if __name__ == '__main__':
    urls = get_item_url()
    dff = pd.DataFrame()
    count = 1
    err = []
    for url in urls:
        try:
            print(count)
            if item_content(url) != '非自营':
                df = pd.DataFrame(item_content(url), index=[0])
                print(df)
                dff = dff.append(df)
                count += 1
        except:
            err.append(id)
            count += 1
    print(err)
    dff.to_excel('gm冰箱.xlsx', index=False)