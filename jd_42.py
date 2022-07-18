# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2021/7/21
# @Author: zengxinyue
# @File  : dzmc_crawl.py
import re
import pandas as pd
import requests
# from fake_useragent import UserAgent


def get_jd_url(category_url):
        count = 0
        ids = []
        for i in range(1, 500):
            url = category_url + '&page=' + str(i)
            try:
                headers = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chr'
                                  'ome/92.0.4515.159 Safari/537.36',
                     "cookie": "shshshfpa=921e56ac-a37e-9593-173e-59fc71fd0634-1618062800; shshshfpb=taGtMmj3qeXU%20l"
                               "jdZdYOuJg%3D%3D; __jdu=24861711; pinId=EB1j78hsJyvIJCQg9wpYgbV9-x-f3wj7; pin=jd_5575"
                               "9c337ff07; unick=jd_153090ppj; _tp=jbJ22abY%2F05BLtM1J9gPEpEKkWN1OqT7EzzJykuH8r0%3D;"
                               " _pst=jd_55759c337ff07; __guid=143920055.1025991105122264300.1624415732622.317; qrsc"
                               "=3; TrackID=1tvAHArunLBiIDW1JRPCzgeIjx20z42egIB1mfCV3_gX3iQEbCc_hnevmKayE-TR5BcO2ei"
                               "LPX8dJiByrXi_Cctdr_c-8WzfblXFQQFaefkg; __jdv=76161171|direct|-|none|-|1630578148055"
                               "; areaId=22; ipLoc-djd=22-1930-50947-0; PCSYCityID=CN_510000_510100_510107; __jda=12"
                               "2270672.24861711.1623860820.1629451429.1630578148.56; __jdc=122270672; shshshfp=8b3a"
                               "426d25dbd53d214404d239f37975; rkv=1.0; monitor_count=7; 3AB9D23F7A4B3C9B=3L5PGOSRQEF"
                               "FGUZW2V7MVO72PORDVOLCX5ZBABUMETQXPRWQWXHLSGMGHW2PEQYKCBDQEQED4IOUDH6IIAXNCKNKDI; CCC"
                               "_SE=ADC_42%2bT96qNuMMIUKP180Yo1C3LpP4cI7LKxX6R9GrdTzp33TblzLyblCrZBo9bB4PKnB0EekS9Fz"
                               "sev7Lrl1exfkSJpLlBCrgQwnDTVzCNgMRdzDJ2iZzyYWee1oCK1wk3Gs8xTZlxyPsIDP6fcskO3c5YXYUq9u"
                               "7FI7I3By%2b%2f2QR5NfXMBBw6b7ZM3OQ89zcME%2bPZmZoMl0ZX7reFrBoJV6Ps3htDUOlqETX2ziStLesw"
                               "d%2bs4t27UNNzNTjQlm5eNY3sWa431pSlbRinDqzcgkPorIsttCy0DA2I38%2bVPuDxPGFEVqNTRPj5OcY92"
                               "JJej0GTmruTpE0YDMJAY6waoJDEPoX%2b%2bHa6qoQXFJMrC3ntJB0QYx921BabYZohC0j3VF91xiJ62s4w"
                               "1ILdmnXPWvDDFzAolqvsDKqGvas2h7597EGk0osj7da3LPDQjynbt; unpl=V2_ZzNtbUVVREV2D0NXeUtU"
                               "UmJXRwlKUkUddgwUBi8QXQdkAUJdclRCFnUUR1xnGF8UZwoZX0pcRh1FCEdkeR1ZAmYBEV1yZ3MWdThGVU"
                               "saWQxgAxRdQmdzFX0PdmQwTABrIUJQbUJXRBFwCk5WchhsBFcDE19DVUQVcA5OZDB3XUhkBhtaQlFDF"
                               "UUJdlc%3d"}
                # get url content
                response = requests.get(url, headers=headers, timeout=5).text
                # print(response)
                # match paragraph contains images' urls
                temp = re.findall('href="//item.jd.com/(.*?).html"', response)
                # name = ''.join(temp)
                for item in temp:
                    if item not in ids:
                        ids.append(item)
                        count += 1
                if count > 2000:
                    return ids
            except:
                pass
        return ids


def get_product_info(id):
    info_url = 'https://item.jd.com/' + id + '.html'
    price_url = 'https://c.3.cn/recommend?callback=handleComboCallback&methods=accessories&sku=' + id + \
                '&cat=737%2C794%2C798'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.'
                      '4515.159 Safari/537.36',
        "cookie": "shshshfpa=921e56ac-a37e-9593-173e-59fc71fd0634-1618062800; shshshfpb=taGtMmj3qeXU%20ljdZdYOuJg%3D%"
                  "3D; __jdu=24861711; pinId=EB1j78hsJyvIJCQg9wpYgbV9-x-f3wj7; pin=jd_55759c337ff07; unick=jd_153090p"
                  "pj; _tp=jbJ22abY%2F05BLtM1J9gPEpEKkWN1OqT7EzzJykuH8r0%3D; _pst=jd_55759c337ff07; __guid=143920055."
                  "1025991105122264300.1624415732622.317; qrsc=3; TrackID=1tvAHArunLBiIDW1JRPCzgeIjx20z42egIB1mfCV3_g"
                  "X3iQEbCc_hnevmKayE-TR5BcO2eiLPX8dJiByrXi_Cctdr_c-8WzfblXFQQFaefkg; __jdv=76161171|direct|-|none|-|"
                  "1630578148055; areaId=22; ipLoc-djd=22-1930-50947-0; PCSYCityID=CN_510000_510100_510107; __jda=122"
                  "270672.24861711.1623860820.1629451429.1630578148.56; __jdc=122270672; shshshfp=8b3a426d25dbd53d214"
                  "404d239f37975; rkv=1.0; monitor_count=7; 3AB9D23F7A4B3C9B=3L5PGOSRQEFFGUZW2V7MVO72PORDVOLCX5ZBABUM"
                  "ETQXPRWQWXHLSGMGHW2PEQYKCBDQEQED4IOUDH6IIAXNCKNKDI; CCC_SE=ADC_42%2bT96qNuMMIUKP180Yo1C3LpP4cI7LKx"
                  "X6R9GrdTzp33TblzLyblCrZBo9bB4PKnB0EekS9Fzsev7Lrl1exfkSJpLlBCrgQwnDTVzCNgMRdzDJ2iZzyYWee1oCK1wk3Gs8"
                  "xTZlxyPsIDP6fcskO3c5YXYUq9u7FI7I3By%2b%2f2QR5NfXMBBw6b7ZM3OQ89zcME%2bPZmZoMl0ZX7reFrBoJV6Ps3htDUOl"
                  "qETX2ziStLeswd%2bs4t27UNNzNTjQlm5eNY3sWa431pSlbRinDqzcgkPorIsttCy0DA2I38%2bVPuDxPGFEVqNTRPj5OcY92"
                  "JJej0GTmruTpE0YDMJAY6waoJDEPoX%2b%2bHa6qoQXFJMrC3ntJB0QYx921BabYZohC0j3VF91xiJ62s4w1ILdmnXPWvDDFz"
                  "AolqvsDKqGvas2h7597EGk0osj7da3LPDQjynbt; unpl=V2_ZzNtbUVVREV2D0NXeUtUUmJXRwlKUkUddgwUBi8QXQdkAUJd"
                  "clRCFnUUR1xnGF8UZwoZX0pcRh1FCEdkeR1ZAmYBEV1yZ3MWdThGVUsaWQxgAxRdQmdzFX0PdmQwTABrIUJQbUJXRBFwCk5W"
                  "chhsBFcDE19DVUQVcA5OZDB3XUhkBhtaQlFDFUUJdlc%3d"}
    # get url content
    response = requests.get(info_url, headers=headers, timeout=5).text
    zy = re.findall('自营', response)
    if len(zy) <= 3:
        return 'no'
    response1 = requests.get(price_url, headers=headers, timeout=5).text
    params1 = re.findall('<dt>(.*?)</dt><dd>(.*?)</dd>', response)
    params2 = re.findall("<li title='.*?>(.*?)</li>", response)
    full_name_list = re.findall('<title>(.*?)-京东</title>', response)
    brand_list = re.findall("<li title='(.*?)'>品牌：", response)
    name_list = re.findall("<li title='.*?'>商品名称：(.*?)</li>", response)
    price_temp_list = re.findall('"wMeprice":.*?"wMaprice":(.*?)},"status"', response1)

    if not price_temp_list:
        price = '无'
    else:
        price = ''.join(price_temp_list)
    if not full_name_list:
        full_name = '无'
    else:
        full_name = ''.join(full_name_list)
    if not brand_list:
        brand = '无'
    else:
        brand = ''.join(brand_list)
    if not name_list:
        name = '无'
    else:
        name = ''.join(name_list)
    if not params1:
        params1 = '无'
    if not params2:
        params2 = '无'

    temp = ''.join(re.findall("imageList: \[(.*?)\]", response))
    temp_list = temp.split(',')
    pic1 = []
    for item in temp_list:
        pic1.append('https://img14.360buyimg.com/n0/' + item[1:-1])

    response2 = requests.get('https://cd.jd.com/description/channel?skuId=100000290697&mainSkuId=' + id,
                             headers=headers, timeout=5).text
    temp2 = re.findall('//img30.360buyimg.com(.*?).jpg', response2)
    pic2 = []
    for item in temp2:
        pic2.append('https://img30.360buyimg.com' + item + '.jpg')
    return {'商品名称': full_name, '商品品牌': brand, '商品型号': name, '商品价格': price, '商品链接': info_url,
            '商品介绍': str(params2), '规格参数': str(params1), '商品主图': str(pic1), '商品详情图': str(pic2)}


if __name__ == '__main__':
    id_list = get_jd_url('https://search.jd.com/Search?keyword=%E7%AF%AE%E7%90%83&enc=utf-8&wq=%E7%AF%AE%E7%90%83&pvid=430c091954d14988a01ebebd4063db9a')
    print(len(id_list))
    dff = pd.DataFrame()
    count = 1
    for id in id_list:
        print('currently crawling: ' + str(count))
        try:
            dic1 = get_product_info(id)
            if dic1 != 'no':
                df = pd.DataFrame(dic1, index=[0])
                dff = dff.append(df)
        except:
            pass
        count += 1
    dff.to_excel('jd_篮球.xlsx', index=False)