#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 19:21:01 2021

@author: rico
"""


import pymssql
import pandas as pd
import sys
def get_zgc_params(zgc_categoryname,params_list,source):
    #获取zgc参数项
    try:
        conn_zi_new = pymssql.connect(host='123.56.115.207', user='zgcprice3311',password='zgcprice20200628',database= 'ZI_NEW',autocommit=True)
        cursor_zi_new = conn_zi_new.cursor()
        
        cursor_zi_new.execute(f"select ZI_SubTitle,Other_SubTitle from Product_Relation_Attribute_Subtitle where ZI_SubCategoryCode = '{zgc_categoryname}' and Source = '{source}'")
        data = cursor_zi_new.fetchall()
        subtitle_map_df = pd.DataFrame(data, columns=[tuple[0] for tuple in cursor_zi_new.description])
        
        res_list = list()
        for key in params_list:
            if subtitle_map_df[subtitle_map_df['ZI_SubTitle'] == key].empty:
                    
                    if subtitle_map_df[subtitle_map_df['Other_SubTitle'] == key].empty:
                        
                        flag = False
                        for subtitle in subtitle_map_df['ZI_SubTitle'].tolist():
                            if subtitle in key:
                                res_list.append(subtitle)

                                flag = True
                                break
                        if flag:
                            pass
                        else:
                            res_list.append("无参数项对应关系")
                            continue
                        
                    else:
                        res_list.append(subtitle_map_df[subtitle_map_df['Other_SubTitle'] == key]['ZI_SubTitle'].tolist()[0])

            else:
                res_list.append(key)
                    
        res_dict = dict(zip(params_list, res_list))
         
        conn_zi_new.close()

        code = 1
        msg = "success"
        res = {'code':code,'msg':msg,'paramsAttr_dict':res_dict}
        return res
        return code,msg,res_dict
    
    except Exception as e:
        conn_zi_new.close()
        code = 0
        msg = str(e)
        res = {'code':code,'msg':msg,'paramsAttr_dict':{}}
        return res


def update_params_value(path):

    #创建新产品库链接
    conn_zi_new = pymssql.connect(host='123.56.115.207', user='zgcprice3311',password='zgcprice20200628',database= 'ZI_NEW',autocommit=True)
    cursor_zi_new = conn_zi_new.cursor()

    df = pd.read_excel(path, sheet_name='Sheet1', converters = {'SKU':str})

    df = df.fillna('无')

    for index,row in df.iterrows():
        # if index < 1816:
        #     continue
        #获取sku和skuid
        if index % 20 == 0:
            conn_zi_new.close()
            cursor_zi_new.close()
            conn_zi_new = pymssql.connect(host='123.56.115.207', user='zgcprice3311', password='zgcprice20200628',
                                          database='ZI_NEW', autocommit=True)
            cursor_zi_new = conn_zi_new.cursor()



        sku = row['SKU']
        cursor_zi_new.execute(f"select id from p_sku where sku = '{sku}'")
        data = cursor_zi_new.fetchone()
        skuid = data[0]
        
        #获取指数类别
        category_name = row['指数类别']
        
        #获取新命名的指数名称
        new_name = str(row['指数名称']).strip().replace("'","''")
        
        #获取数据来源（JD/SN）
        source = row['source']
        
        #获取参数信息
        params_ori = eval(row['参数'])
        
        #根据对应关系转换成指数参数项
        params_ori_key = list(params_ori.keys())
        res = get_zgc_params(category_name,params_ori_key,source)
        if res['code'] == 0:
            
            print("异常")
            print(f"{res['msg']}")
            break
        
        else:
            
            params_key_dict = res['paramsAttr_dict']
        
        params_ori_std = {}
        for key in params_ori:
            
            if params_key_dict[key] == '无参数项对应关系':
                continue
            else:
                if params_ori[key] == '':
                    continue
                else:
                    params_ori_std.update({params_key_dict[key]:params_ori[key]})
            
        #获取库内该类别的所有参数项及ID        
        cursor_zi_new.execute(f"select subtitle,subtitleid from vw_property where name = '{category_name}'")
        data = cursor_zi_new.fetchall()
        subtitle_list = [ele[0] for ele in data]
        subtitleid_list = [ele[1] for ele in data]
        # return
        #更新产品名称
        cursor_zi_new.execute(f"update p_sku set skuname = '{new_name}' where sku = '{sku}'")
            
        #更新产品参数值
        for subtitle,subtitleid in zip(subtitle_list,subtitleid_list):
            try:
                value = params_ori_std[subtitle].strip()
            except:
                continue

            cursor_zi_new.execute(f"select id from p_skuvalue where subtitleid = {subtitleid} and value = '{value}'")
            data = cursor_zi_new.fetchall()
            
            try:
                valueid = pd.DataFrame(data, columns=[tuple[0] for tuple in cursor_zi_new.description])['id'].tolist()[0]
            except:
                cursor_zi_new.execute(f"insert into p_skuvalue (subtitleid,value) values ({subtitleid}, '{value}')")
                    
                cursor_zi_new.execute(f"select id from p_skuvalue where subtitleid = {subtitleid} and value = '{value}'")
                valueid = pd.DataFrame(cursor_zi_new.fetchall(), columns=[tuple[0] for tuple in cursor_zi_new.description])['id'].tolist()[0]
                
                
            cursor_zi_new.execute(f"select a.valueid from p_skuvaluemap a \
                                            left join p_skuvalue b \
                                            on a.valueid = b.id \
                                            left join p_skusubtitle c \
                                            on b.subtitleid = c.id \
                                            where a.skuid = {skuid} and c.name = '{subtitle}'")
            data = cursor_zi_new.fetchall()
            valueid_df = pd.DataFrame(data, columns=[tuple[0] for tuple in cursor_zi_new.description])
            
            if valueid_df.empty:
                
                cursor_zi_new.execute(f"select id from p_skuvaluemap where skuid = {skuid} and valueid = {valueid}")
                data = cursor_zi_new.fetchall()
                check_df = pd.DataFrame(data, columns=[tuple[0] for tuple in cursor_zi_new.description])
                if check_df.empty:
                    cursor_zi_new.execute(f"insert into p_skuvaluemap (skuid,valueid) values ({skuid}, {valueid})")
            else:
                
                valueid_list = valueid_df['valueid'].unique().tolist()
                for valueid_ in valueid_list:
                    cursor_zi_new.execute(f"delete from p_skuvaluemap where skuid = {skuid} and valueid = {valueid_}")
                
                cursor_zi_new.execute(f"select id from p_skuvaluemap where skuid = {skuid} and valueid = {valueid}")
                data = cursor_zi_new.fetchall()
                check_df = pd.DataFrame(data, columns=[tuple[0] for tuple in cursor_zi_new.description])
                if check_df.empty:
                    cursor_zi_new.execute(f"insert into p_skuvaluemap (skuid,valueid) values ({skuid}, {valueid})")         
        print(index)
        
    conn_zi_new.close()


if __name__ == "__main__":
    # print(sys.argv)
    update_params_value(sys.argv[1])
