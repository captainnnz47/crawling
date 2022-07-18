# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2021/7/21
# @Author: zengxinyue
# @File  : get_images_url.py
import datetime
import re
import pandas as pd
from numpy import random
import requests
import pymysql
from fake_useragent import UserAgent
import time
import urllib.request
from tqdm import tqdm


# read the data from excel
def get_data():
    df = pd.read_excel(io='./Book9.xlsx', converters={'sku': str, 'product_url': str, 'suppliers': str})
    return df


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
        if 'jd' in url:
            headers = {
        'user-agent': UserAgent().random,
        "cookie": "cookie: shshshfpa=3065e100-06f3-3f23-b4b0-6b96c49a743d-1598405644; shshshfpb=i%2Fh8Fj91QwtyPu6wBFlh"
                  "eAw%3D%3D; pinId=jD_7ta1rmN5J11Qck_A6n7V9-x-f3wj7; qrsc=3; areaId=1; pin=jd_5bd3787660efa; unick=j"
                  "d_176333qmo; _tp=aztJyX1aMZr7qQugl%2B0H3kWdaz5p0WYHj0A5A%2Fpc8J4%3D; _pst=jd_5bd3787660efa; mt_xid"
                  "=V2_52007VwMRVlpZUVgcShxsB2BRGlMJCwJGTRlKWRliBhVaQQhbCUxVH1xQMgFCVgoKB1hIeRpdBmYfElNBWFZLH0wSXAxsA"
                  "hFiX2hSahxPG10GbgUWUF1oUlwbTQ%3D%3D; ipLoc-djd=1-72-2799-0; __jda=122270672.1604026030147108994685"
                  ".1604026030.1604026030.1604026030.1; __jdc=122270672; __jdv=122270672|direct|-|none|-|160402603015"
                  "2; __jdu=1604026030147108994685; shshshfp=d1660f158e4b5f2e5ceaf541ba2c82a4; rkv=1.0; 3AB9D23F7A4B3C"
                  "9B=DZLDWIBNPKBPSA6B4NTV7YP3UQLAKRHUPOP2OQDDJCM2E633MIUUBJRCGVIAJEKNCDF6KEPND6COWBORL5BJYGGIZY; shsh"
                  "shsID=7f98e09f96732e4203f7d7fa666161e8_4_1604026082407; __jdb=122270672.4.1604026030147108994685|1"
                  ".1604026030"}
        elif 'sn' in url:
            headers = {
        'user-agent': UserAgent().random,
        "cookie": "cookie: SN_SESSION_ID=455144c4-061b-4280-acd3-ddf56d88bd96; _snmc=1; _snvd=1626937900794ezksbNfiHQe"
                  "; _snzwt=THcFRE17acd0e3fa028B898ef; cityCode=028; districtId=12132; streetCode=0280199; cityId=9265"
                  "; totalProdQty=0; hm_guid=efb2c52a-631b-4a71-b18d-b6528bbd70eb; isScale=false; _df_ud=84dcc9a2-0f0b"
                  "-4050-8125-fd01a78f0186; _device_session_id=p_1d23741c-ab3b-43c0-861e-0c6380532279; tradeMA=179; a"
                  "uthId=siOXbKsPyn8ZcOjqKIPcvdLKeWxjxisOaH; secureToken=F5EB5FCF8B7EB07B38BFCFDC12293275; custLevel="
                  "161000000100; custno=7367889075; ecologyLevel=ML100100; idsLoginUserIdLastTime=; logonStatus=2; ni"
                  "ck=136******02; nick2=136******02; sncnstr=ab9JH%2ByORy0lXdTqQJXXiw%3D%3D; _snsr=baidu%7Creferral%"
                  "7C%7C%7C; smhst=11925988348|0000000000; token=e5805dda-3dba-4fc7-abf3-2668ebc1e036; SN_CITY=230_02"
                  "8_1000268_9265_01_12132_1_1_99_0280199; _memberStInfo=success%7C7367889075%7Cperson%7CE102%7CA9200"
                  "020%7CA1000050%2CA9200020%2Cundefined%2Cundefined%7CA1000100%2CA9200020%2Cundefined%2Cundefined; _"
                  "snma=1%7C162693789991057445%7C1626937899910%7C1626937979439%7C1626937985259%7C6%7C3; _snmp=1626937"
                  "98470053652; _snmb=162693795581671393%7C1626937985280%7C1626937985263%7C3; route=a09bbfa9538f3fa91"
                  "9341db92420a7cd"}
        else:
            headers = {
        'user-agent': UserAgent().random,
        "cookie": "cookie: uid=CjozJ2D5GwIrMGymGG2DAg==; ctx=app-shangcheng|ver-v7.0.0|plt-pc|cmpid-seo_www.baidu.com_"
                  "%E6%97%A0; sajssdk_2015_cross_new_user=1; atgregion=71010300%7C%E5%9B%9B%E5%B7%9D%E7%9C%81%E6%88%90"
                  "%E9%83%BD%E5%B8%82%E9%87%91%E7%89%9B%E5%8C%BA%E8%A5%BF%E5%AE%89%E8%B7%AF%E8%A1%97%E9%81%93%7C710100"
                  "00%7C71000000%7C710103002; cartnum=0_0-1_0; __clickidc=154538894726938120; __c_visitor=154538894726"
                  "938120; __gma=ffb8de7.1562418809860.1626938121139.1626938121139.1626938121139.1; __gmv=156241880986"
                  "0.1626938121139; __gmb=ffb8de7.1.1562418809860|1.1626938121139; __gmc=ffb8de7; __gmz=ffb8de7|www.go"
                  "me.com.cn|-|referrer|-|-|-|1562418809860.1626938121139|dc-1|1626938121140; s_cc=true; gpv_p22=no%20"
                  "value; ufpd=20ef51df9d72c872524609ca774af6648641291c95d904fa057527793beff1e4b5fc9dca990722caf72665e"
                  "0ecb13f52cc2eb67d95c2b80dad2136bea3e32619|60f91b0aLgVnbOE2NnH3e9FlewTVrKqMCgm5azp1; SCN=NICD0w17dk"
                  "HUH2xBoY24WAS6b0kzoxjGLXc%2BdlH3o9Z%2BayEh69YuOs9ygdW%2FlsMa7t6xHXfBGqlRp1gbStY2Mehdgs1q9ylqs95OdS"
                  "EwA8GvbGvUoUMF7A%3D%3D0fbef69933ed7aea7c33a42101fa081e; sid=86495204721; SSO_USER_ID=86495204721; "
                  "isCare=N; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2286495204721%22%2C%22first_id%22%3A%2"
                  "217acd1184c88a7-09f00e9bc6f87c-303464-1327104-17acd1184c963f%22%2C%22props%22%3A%7B%22%24latest_t"
                  "raffic_source_type%22%3A%22%E7%A4%BE%E4%BA%A4%E7%BD%91%E7%AB%99%E6%B5%81%E9%87%8F%22%2C%22%24lates"
                  "t_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22h"
                  "ttps%3A%2F%2Fopen.weixin.qq.com%2F%22%2C%22_latest_cmpid%22%3A%22seo_www.baidu.com_%E6%97%A0%22%7D"
                  "%2C%22%24device_id%22%3A%2217acd1184c88a7-09f00e9bc6f87c-303464-1327104-17acd1184c963f%22%7D; DSESS"
                  "IONID=797730bb35e74db0ac476b7eccef4999; compare=; gpv_pn=no%20value; s_ppv=-; s_getNewRepeat=162693"
                  "8347558-New; s_sq=gome-prd%3D%2526pid%253Dhttps%25253A%25252F%25252Flist.gome.com.cn%25252Fcat10000"
                  "070-00-0-48-1-0-0-0-1-1aK0-0-0-10-0-0-0-0-0.html%25253Fintcmp%25253Dprom102276-1000051971-1%2526oid"
                  "%253Dhttps%25253A%25252F%25252Fitem.gome.com.cn%25252F9140252663-1130947932.html%25253Fintcmp%25253"
                  "Dlist-9000000700-1_1_1%252526search_id%25253DCATPL%2525401GK%2526ot%253DA; proid120517atg=%5B%22G00"
                  "1-fshop-9140252663-1130947932%22%5D; gradeId=11"}
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


def get_jd_image_url(url, ip=1, err_num=0):
    try:
        pics = []
        err_num = err_num
        # get url content
        response = get_url(url, ip=ip).text
        # match paragraph contains images' urls
        try:
            temp = re.search('imageList:(.*?)]', response)
            # process raw data to urls' list
            result = str(temp[1])[2:-1]
            pic_list = result.split(",")
            # strip and concat urls into right forms
            for i in range(len(pic_list)):
                temp_url = 'https://img30.360buyimg.com/sku/' + pic_list[i][1:-1]
                if i == len(pic_list) - 1:
                    temp_url += 'g'
                pics.append(temp_url)
        except:
            pass
        # return urls' list
        return pics
    except:
        s = requests.session()
        s.keep_alive = False
        err_num += 1
        # maximum three-time requesting
        if err_num <= 3:
            time.sleep(1)
            res = get_jd_image_url(url, ip=1, err_num=err_num)
        return res


def get_sn_image_url(url, ip=1, err_num=0):
    try:
        err_num = err_num
        # get url content
        response = get_url(url, ip=ip).text
        # match paragraph contains images' urls
        try:
            temp = re.findall('//uimgproxy.*?.jpg', response, re.M)
            if len(temp[0]) >= 130:
                temp = re.findall('//uimgproxy.*?.png', response, re.M)
        except:
            pass
        pics = []
        for item in temp:
            temp_url = 'http:' + item
            pics.append(temp_url)
        # return urls' list
        return pics
    except:
        s = requests.session()
        s.keep_alive = False
        err_num += 1
        # maximum three-time requesting
        if err_num <= 3:
            time.sleep(1)
            res = get_sn_image_url(url, ip=1, err_num=err_num)
        return res


def get_gm_image_url(url, ip=1, err_num=0):
    try:
        pics = []
        err_num = err_num
        response = get_url(url, ip=ip).text
        # match paragraph contains images' urls
        try:
            temp = re.findall('<img width=.*?bpic="(.*?).jpg', response, re.M)
            for item in temp:
                temp_url = 'http:' + item + '.jpg'
                pics.append(temp_url)
        except:
            pass
        # return urls' list
        return pics
    except:
        s = requests.session()
        s.keep_alive = False
        err_num += 1
        # maximum three-time requesting
        if err_num <= 3:
            time.sleep(1)
            res = get_gm_image_url(url, ip=1, err_num=err_num)
        return res


def img_download(sku_summary):
    # get the sku for every product
    for key in sku_summary:
        count = 1
        # get the urls' list for every product and download the pictures
        for item in sku_summary[key]:
            path = 'C:/Users/zxyul/Desktop/pics/' + str(key) + '_' + str(count) + '.jpg'
            urllib.request.urlretrieve(url=str(item), filename=path)
            print('successfully download ' + str(key) + '-' + str(count))
            count += 1


if __name__ == '__main__':
    # create a timer
    starttime = datetime.datetime.now()
    # read the excel
    df1 = get_data()
    sku_summary1 = {}
    # number of lines to run
    e = 200
    pbar = tqdm(total=e, desc='Crawling:')

    for j in range(0, e):
        pbar.update(1)
        url1 = df1.iat[j, 1]
        # deal with specific product
        # 1. get a list of urls on one product
        # 2. store urls' list and sku value into dictionary
        # 3. add urls' list on image_url column
        try:
            # case 1: product from JD
            if df1.iat[j, 2] == 'JD':
                url2 = get_jd_image_url(url1, ip=1)
                sku_summary1[df1.iat[j, 0]] = url2
                df1.iat[j, 3] = url2
            # case 2: product from SN
            elif df1.iat[j, 2] == 'SN':
                url2 = get_sn_image_url(url1, ip=1)
                sku_summary1[df1.iat[j, 0]] = url2
                df1.iat[j, 3] = url2
            # case 3: product from GM
            else:
                url2 = get_gm_image_url(url1, ip=1)
                sku_summary1[df1.iat[j, 0]] = url2
                df1.iat[j, 3] = url2
        except:
            pass
    pbar.close()
    # output as excel
    df1.to_excel('result.xlsx', index=False)
    # output the time used
    crwalTime = datetime.datetime.now()
    print('CrawlTime use:', crwalTime-starttime)
    img_download(sku_summary1)
    dtime = datetime.datetime.now()
    print('DownLoadTime use:', dtime-crwalTime)




