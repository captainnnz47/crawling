#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import pymssql


def insert_data():
    # read the excel which stores the parameters waiting to be added
    sheet = pd.read_excel("./待新增二级参数项.xlsx", sheet_name='Sheet1')
    # create a log to trace the program
    log_txt = ""
    # make a connection with the sql server
    conn_zi_new = pymssql.connect(host='123.56.115.207', user='zgcprice3311', password='zgcprice20200628', database='ZI_NEW',
                                  autocommit=True)
    # create a cursor
    cursor = conn_zi_new.cursor()

    # find all the first order parameters
    first_sql = 'select name, id  from p_skusubtitle where lev = 1'
    cursor.execute(first_sql)
    data = cursor.fetchall()
    # store the data into dictionary
    first_params = dict(data)

    # traverse all the data in the dataset and strip all the parameters
    for index, row in sheet.iterrows():
        first_param = row["一级参数项"].strip()
        second_param = row["二级参数项"].strip()

        # case 1: first order parameter not in dataset then fail to add
        if first_param not in first_params:
            log_txt = f"{log_txt}表中名称为{index + 2}的一级参数项'{first_param}'不存在，添加失败\n"
            continue
        else:
            pid = first_params[first_param]
            second_sql = f"select name, id from p_skusubtitle where lev = 2 and pid = {pid} and name = '{second_param}'"
            second_params = cursor.execute(second_sql)
            # case 2: second order parameter already existed in dataset then fail to add
            data = cursor.fetchall()
            if len(data) > 0:
                log_txt = f"{log_txt}表中名称为{index + 2}的参数项在数据库中已存在，添加失败\n"
                continue
            # if not in case 1 or 2 then add the parameter into dataset successfully
            insert_sql = f"insert into p_skusubtitle (name, lev, pid) values ('{second_param}', 2, {pid})"
            cursor.execute(insert_sql)
    # export_category = pd.DataFrame(data, columns=[tuple[0] for tuple in cursor.description])
    # close the dataset and cursor
    conn_zi_new.close()
    cursor.close()
    # print the log statements
    print(log_txt)
    return log_txt


if __name__ == "__main__":

    insert_data()