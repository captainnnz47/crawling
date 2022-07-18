#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import pymssql
from public import Index


def get_point_category_params_data(category):
    
    category_sheet_name = category.replace("/", "_")

    conn_zi_new = pymssql.connect(host='123.56.115.207', user='zgcprice3311', password='zgcprice20200628',
                                  database='ZI_NEW', autocommit=True)
    cursor = conn_zi_new.cursor()
    
    conn_zdindex = pymssql.connect(host='123.56.115.207', user='zgcprice3311', password='zgcprice20200628',
                                   database='zdindex', autocommit=True)
    cursor_zdindex = conn_zdindex.cursor()
    
    cursor.execute(f"select id,name from p_category where id not in (select distinct pid from p_category) and "
                   f"name in ('{category}')")
    
    data = (cursor.fetchall())
    export_category = pd.DataFrame(data,columns=[tuple[0] for tuple in cursor.description])
    
    writer = pd.ExcelWriter(f"{category_sheet_name}参数确认.xlsx")
    
    for category_code,category_name in zip(export_category['id'].tolist(),export_category['name'].tolist()):
        
        print(f"开始提取{category_name}参数数据")

        # 获取产品信息
        cursor.execute(f"select a.*,h.name as father_brand_name,d.name as brand_name,g.name as attr_name,f.value "
                       f"from p_sku a \
                       left join p_spu b \
                       on a.spuid = b.id \
                       left join p_category c \
                       on b.categoryid = c.id \
                       left join p_brand d \
                       on b.brandid = d.id \
                       left join p_skuvaluemap e \
                       on a.id = e.skuid \
                       left join p_skuvalue f \
                       on e.valueid = f.id \
                       left join p_skusubtitle g \
                       on f.subtitleid = g.id \
                       left join p_brand h \
                       on d.pid = h.id \
                       where b.categoryid = {category_code} and a.state in (1,4)")
        data = (cursor.fetchall())
        df_sku = pd.DataFrame(data, columns=[tuple[0] for tuple in cursor.description])
        sku_list = []
        for item in data:
            sku_list.append(item[2])
        
        cursor.execute(f"select a.*,d.name as brand_name,g.name as attr_name,f.value from p_sku a \
                   left join p_spu b \
                   on a.spuid = b.id \
                   left join p_category c \
                   on b.categoryid = c.id \
                   left join p_brand d \
                   on b.brandid = d.id \
                   left join p_valuemap e \
                   on b.id = e.spuid \
                   left join p_value f \
                   on e.valueid = f.id \
                   left join p_subtitle g \
                   on f.subtitleid = g.id \
                   where b.categoryid = {category_code} and a.state in (1,4)")
        data = (cursor.fetchall())
        df_spu = pd.DataFrame(data,columns=[tuple[0] for tuple in cursor.description])
        
        res = pd.DataFrame()
        id_list = []
        state_list = []
        product_name_list = []
        father_brand_list = []
        brand_list = []
        category_list = []
        
        cursor.execute(f"select * from vw_property where categoryid = {category_code}")
        data = cursor.fetchall()
        params_df = pd.DataFrame(data, columns=[tuple[0] for tuple in cursor.description])
        params_df['needed_param'] = params_df['identy'].apply(lambda x: x[0])
        params_df['standard_param'] = params_df['identy'].apply(lambda x: x[2])
        
        params_df = params_df[params_df['needed_param'] != '0']
        params_df['subtitle'] = params_df['subtitle'].apply(lambda x: x.strip())

        param_list = params_df['subtitle'].tolist()
        for param in param_list:
            param_var = '_' + ''.join(param.split()).replace('（', '').replace('）', '').replace('/', '').\
                replace('(', '').replace(')', '').replace('+', '').replace('-', '').replace('*', '').replace('.', '')
            exec('%s_list=[]'%param_var)

        process_index = 0
        index = Index()
        
        for prodcut_id in list(df_sku['sku'].unique()):
            try:
                print(index(process_index, len(list(df_sku['sku'].unique()))-1), end='%')
            except:
                print(index(process_index, 1), end='%')
            process_index += 1
            
            id_list.append(prodcut_id)
            state_list.append(df_sku[df_sku['sku'] == prodcut_id]['state'].tolist()[0])
            product_name_list.append(df_sku[df_sku['sku'] == prodcut_id]['skuname'].tolist()[0])
            
            father_brand_list.append(df_sku[df_sku['sku'] == prodcut_id]['father_brand_name'].tolist()[0])
            brand_list.append(df_sku[df_sku['sku'] == prodcut_id]['brand_name'].tolist()[0])
            
            category_list.append(category_name)
            
            for param in param_list:
                param_var = '_' + ''.join(param.split()).replace('（', '').replace('）', '').replace('/', '').\
                    replace('(', '').replace(')', '').replace('+', '').replace('-', '').replace('*', '').replace('.', '')
                try:
                    exec("%s_list.append(df_sku[(df_sku['sku'] == prodcut_id) & (df_sku['attr_name'] == '%s')]['value']"
                         ".tolist()[0])" % (param_var,param))
                except:
                    try:
                        exec("%s_list.append(df_spu[(df_spu['sku'] == prodcut_id) & (df_spu['attr_name'] == '%s')]"
                             "['value'].tolist()[0])" % (param_var,param))
                    except:
                        exec("%s_list.append('无参数，需补充')" % param_var)

        res['产品编码'] = id_list
        res['产品状态'] = state_list
        res['产品名称'] = product_name_list
        res['产品父品牌'] = father_brand_list
        res['产品品牌'] = brand_list
        res['产品类别'] = category_list

        for index,row in params_df.iterrows():
            param = row['subtitle']
            needed_flag = row['needed_param']
            standard_flag = row['standard_param']
            if param == '产品名称':
                continue
            
            param_var = '_' + ''.join(param.split()).replace('（', '').replace('）', '').replace('/', '').\
                replace('(', '').replace(')', '').replace('+', '').replace('-', '').replace('*', '').replace('.', '')

            # 标记标准项
            if needed_flag == '1' and standard_flag == '1':
                param = '*' + param

            exec("res['%s']=%s_list"%(param,param_var))
    
        res.to_excel(writer,f"{category_sheet_name}参数数据")

        cursor_zdindex.execute(f"select goods_id, goods_url, max(periods) from zd_week_price where sub_category_code ="
                               f" {category_code} and goods_url is not null group by goods_id, goods_url")
        data = (cursor_zdindex.fetchall())
        sku_2 = []
        url = []
        for item in data:
            sku_2.append(item[0])
            url.append(item[1])
        price_df = pd.DataFrame({'goods_id': sku_list})
        for i in range(len(sku_list)):
            for j in range(len(sku_2)):
                if sku_2[j] == sku_list[i]:
                    price_df.loc[i, 1] = url[j]
        inde = []
        for i in range(price_df.shape[0]):
            if len(str(price_df.iat[i, 1])) < 10:
                inde.append(i)
        supplement_sku = []
        for index in inde:
            supplement_sku.append(str(price_df.iat[index, 0]))
        url_li = {}
        for sku in supplement_sku:
            cursor_zdindex.execute(f"select distinct goods_url from zd_week_price_copy where goods_id = '{str(sku)}'")
            url = cursor_zdindex.fetchall()
            url_li[sku] = str(url)
        for i in range(price_df.shape[0]):
            for key in url_li.keys():
                if str(price_df.iat[i, 0]) == key:
                    price_df.loc[i, 1] = url_li[key]
        price_df.to_excel(writer, f"{category_sheet_name}价格链接数据")
        print(f"{category_name}数据导出完毕！")
        
    writer.save()
    conn_zi_new.close()


get_point_category_params_data('搬运车')