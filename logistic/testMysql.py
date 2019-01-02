#!/usr/bin/python3
import json

import pymysql


def query(program_id):
    # 打开数据库连接
    db = pymysql.connect("47.97.193.44", "cmsread", "cmsread@2018", "newcms")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    data = query_category_name_by_program_id(cursor, program_id)
    # 关闭数据库连接
    db.close()
    return data


def query_category_name_by_program_id(cursor, program_id):
    # 使用 execute()  方法执行 SQL 查询
    query_category_name_of_program = "select name from radio_category where id in(select category_id from " \
                                     "radio_channel_to_category where channel_id =(select radio_channel_id from " \
                                     "radio_channel_to_program where " \
                                     "radio_program_id=" + str(program_id) + " and status=99) and status=99) and " \
                                                                             "status=99 "
    cursor.execute(query_category_name_of_program)
    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchone()
    return data


def query_category_name_by_program_ids(program_ids):
    # 打开数据库连接
    db = pymysql.connect("47.97.193.44", "cmsread", "cmsread@2018", "newcms")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 开始分页查询
    query_sql = """select t1.radio_program_id, t3.`name` from radio_channel_to_program t1, radio_channel_to_category 
        t2,  radio_category t3 where t1.radio_channel_id=t2.channel_id and t2.category_id = t3.id and t1.`status`=99 and 
        t3.`status`=99 and t3.hierarchy_pid=12 and t1.radio_program_id in  """  # (10057016,9933414,10228534);
    query_sql += str(tuple(program_ids))
    cursor.execute(query_sql)
    data = cursor.fetchall()
    # 关闭数据库连接
    db.close()
    return data


# [] -> {}
def to_dict(query_data):
    data = {}
    for item in query_data:
        if item[0] not in data.keys():
            data[item[0]] = item[1]
    return data


if __name__ == '__main__':
    with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/export_feedback_audit_2018-12-13.json', 'r',
              encoding='utf-8') as f:
        data = json.load(f)
        f.close()

    p = 0
    while p < len(data):
        temp = data[p:p + 500]
        program_ids = []
        for item in temp:
            program_ids.append(item['program_id'])
        query_data = query_category_name_by_program_ids(program_ids)

        query_data = to_dict(query_data)
        for item in temp:
            if item['program_id'] in query_data.keys():
                item['category_name'] = query_data[item['program_id']]
            else:
                item['category_name'] = '未定'
        p += 500

    with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/export_feedback_audit_2018-12-13_adjusted.json',
              'w',
              encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
        f.close()

    print(data[0])
