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
            'cookies': 'SN_CITY=230_028_1000268_9265_01_12132_2_0_99_0280199; cityId=9265; districtId=12132; streetCo'
                       'de=0280199; _snvd=1630921753616je9GgOgfpmr; isScale=false; hm_guid=5a523963-f6c7-4f31-9ee8-e17'
                       '38e7085a2; _df_ud=fadeba9d-869e-4cc7-ae18-59720c109595; route=28dcdbd6c65624977e9dbc2da86d9446'
                       '; SN_SESSION_ID=f41a7b4d-3946-48ec-9236-360b2e21b8bf; _snmc=1; totalProdQty=0; _snzwt=THN8K717'
                       'bbed004f5ZlQk8cd7; _device_session_id=p_b18a5e3b-3bea-4e5c-92c0-6a2abeddf166; tradeMA=179; aut'
                       'hId=sijrPboBDrn6Blm3n6oACouZQe02F1W2tS; secureToken=3DDBF232F10D270899A7696D7788DBC6; custLeve'
                       'l=161000000100; custno=7367889075; ecologyLevel=ML100100; idsLoginUserIdLastTime=; logonStatus'
                       '=2; nick=136******02; nick2=136******02; sncnstr=ab9JH%2ByORy0lXdTqQJXXiw%3D%3D; _snsr=open.we'
                       'ixin.qq.com%7Creferral%7C%7C%7C; sesab=ACBAABC; sesabv=3%2C12%2C16%2C1%2C2%2C8%2C3; _memberStI'
                       'nfo=success%7C7367889075%7Cperson%7CE102%7CA9200020%7CA1000050%2CA9200020%2Cundefined%2Cundef'
                       'ined%7CA1000100%2CA9200020%2Cundefined%2Cundefined; smhst=12245860555|0000000000a11821560235|'
                       '0000000000a12308480323|0000000000a12311890217|0000000000a12107236141|0000000000a12107233704|0'
                       '000000000a10912566904|0000000000; _snma=1%7C163092175284797427%7C1630921752847%7C163099491621'
                       '2%7C1630995034345%7C15%7C3; _snmp=163099503408469659; _snmb=163099414255149596%7C163099503436'
                       '1%7C1630995034347%7C9; token=0c55d5dd-bed1-471a-907d-303d63771040'}


def get_item_id():
    page_no = 1
    ids = []
    dis = []
    url = 'https://list.suning.com/emall/searchV1Product.do?ci=20064&pg=03&yjhx=0&cp=0&il=0&st=0&iy=-1&ct=1&isNoR' \
          'esult=0&n=1&sesab=ACBAABC&id=IDENTIFYING&cc=028&paging=' + str(page_no) + '&sub=0&spf=_&jzq=276'
    response = requests.get(url, headers=headers, timeout=5).text
    temp = re.findall('datasku="(.*?)\|\|', response)
    temp2 = re.findall('datasku=.*?\|\|(.*?)"', response)
    ids += temp
    dis += temp2
    while len(response) >= 1000:
        page_no += 1
        url = 'https://list.suning.com/emall/searchV1Product.do?ci=20064&pg=03&yjhx=0&cp=0&il=0&st=0&iy=-1&ct=1&isNoR' \
          'esult=0&n=1&sesab=ACBAABC&id=IDENTIFYING&cc=028&paging=' + str(page_no) + '&sub=0&spf=_&jzq=276'
        response = requests.get(url, headers=headers, timeout=5).text
        temp = re.findall('datasku="(.*?)\|\|', response)
        temp2 = re.findall('datasku=.*?\|\|(.*?)"', response)
        ids += temp
        dis += temp2
    result = []
    for item in dis:
        temp = item[-10:]
        result.append(temp)
    print(len(ids))
    print(len(dis))
    return ids, result


def get_id():
    url = 'https://list.suning.com/0-20064-0-2-1-0-0___0_0.html#second-filter'
    response = requests.get(url, headers=headers, timeout=5).text
    temp = re.findall('datasku="(.*?)\|\|', response)
    temp2 = re.findall('datasku=.*?\|\|(.*?)"', response)
    result = []
    for item in temp2:
        te = item[-10:]
        result.append(te)
    return result, temp


def get_item_content(dis, id):
    url = 'https://product.suning.com/' + dis + '/' + id + '.html'
    response = requests.get(url, headers=headers, timeout=5).text
    print(response)
    flag = ''.join(re.findall('<span class="zy" id="itemNameZy"(.*?)</span>', response))
    if '自营' not in flag:
        return '非自营'

    category_1 = ''.join(re.findall('"categoryName1":"(.*?)",', response))
    category_2 = ''.join(re.findall('<a class="ft outline-blind" name=".*?mulu02" href="//list.suning.com/0-.*?-0.html">(.*?)</a>', response))
    category_3 = ''.join(re.findall('<a class="ft outline-blind" name=".*?mulu03" href="//list.suning.com/0-.*?-0.html">(.*?)</a>', response))
    category_4 = ''.join(re.findall('"seoBreadCrumbName":"(.*?)",', response))

    产品名称 = ''.join(re.findall('"itemDisplayName":"(.*?)",', response))
    params = re.findall('更多参数</a></span> </div> <ul class="cnt clearfix">(.*?)</li> </ul> </div>', response)
    核心参数 = re.findall('<li tabindex="0" title=".*?">(.*?)</li>', str(params))
    params2 = re.findall('<div class="procon-param">(.*?)<div id="J-procon-comment"', response)
    包装清单 = re.findall('<td tabindex="0" class="name">(.*?)</td><td class="val" tabindex="0">(.*?)</td>', str(params2))
    主体 = re.findall('<div class="name-inner"> <span>(.*?)</span>.*?<td class="val">(.*?)</td> ', str(params2))

    if 核心参数 != []:
        final = ''
        for item in 核心参数:
            if '品牌' in item:
                continue
            else:
                temp = item.split('：')
                str1 = temp[0] + "'"
                str2 = "'" + temp[1]
                str_final = str1 + ':' + str2 + ','
                str_final = str_final.replace("'", '"')
                final += str_final
        核心参数2 = final[0:-2]
    else:
        核心参数2 = '无'

    if 包装清单 != []:
        final2 = ''
        for item in 包装清单:
            temp = str(item)[1:-1]
            li = temp.split(', ')
            str1 = li[0]
            str2 = li[1]
            str_final = str1 + ':' + str2 + ','
            str_final = str_final.replace("'", '"')
            final2 += str_final

        包装清单2 = final2[0:-1]
    else:
        包装清单2 = ''

    if 主体 != []:
        final3 = ''
        for item in 主体:
            if '品牌' in str(item):
                continue
            else:
                temp = str(item)[1:-1].replace("'", '"')
                li = temp.split(', ')
                str_final = li[0] + ':' + li[1] + ','
                final3 += str_final.strip()
        主体2 = final3[0:-1]
    else:
        主体2 = '无'


    price_url = 'https://pas.suning.com/nspcsale_0_0000000' + id + '_0000000' + id + '_0000000000_230_028_02801' \
                '99_157122_1000268_9265_12132_Z001_161000000100__R9000002_0.01_0___0000579T5____0_01_7367889075_1040' \
                '600.0_1_01_157237_240503__.html?callback=pcData&_=1630996439945'
    response1 = requests.get(price_url, headers=headers, timeout=5).text
    price = ''.join(re.findall('"netPrice":"(.*?)",', response1))

    return {'商品链接': url, '一级': category_1, '二级': category_2, '三级': category_3, '四级': category_4,'产品名称':
        产品名称, '价格': price, '核心参数': 核心参数2, '包装清单': 包装清单2, '主体': 主体2}


if __name__ == '__main__':
    dis, ids = get_id()
    dff = pd.DataFrame()
    count = 1
    err = []
    for i in range(len(ids)):
        try:
            print(count)
            dic = get_item_content(dis[i], ids[i])
            print(dic)
            if dic != '非自营':
                df = pd.DataFrame(dic, index=[0])
                dff = dff.append(df)
            count += 1
        except:
            err.append(id)
            count += 1
    print(err)
    dff.to_excel('单反相机.xlsx', index=False)