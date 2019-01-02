# -*- coding:utf-8 -*-

import json

# 读取数据
with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    print(data[0])
    f.close()

with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data_2.json', 'r', encoding='utf-8') as f:
    data_temp = json.load(f)
    print(data_temp[0])
    f.close()

data += data_temp

dic = {1: [0, 0], 2: [0, 0], 3: [0, 0], 4: [0, 0], 5: [0, 0]}
dic2 = {1: [0, 0], 2: [0, 0], 3: [0, 0], 4: [0, 0], 5: [0, 0]}
dic3 = {1: [0, 0], 2: [0, 0], 3: [0, 0], 4: [0, 0], 5: [0, 0]}
dic4 = {1: [0, 0], 2: [0, 0], 3: [0, 0], 4: [0, 0], 5: [0, 0]}
for item in data:
    risks = item['risks']
    dic_idx = 0  # 确定 dic 中每个 key-value value[] 中 应该统计哪一个数量 0表示人工审核正错误 1表示人工审核正确
    if item['feedback_type'] == 99:
        dic_idx = 0
    else:
        dic_idx = 1
    for risk in risks:
        hit_len = len(risk['hit'])
        if hit_len == 0:
            dic2[risk['label']][dic_idx] += 1
        if len(risks) == 1:
            dic3[risk['label']][dic_idx] += 1
        if hit_len == 0 and len(risks) == 1:
            dic4[risk['label']][dic_idx] += 1
        for hit_idx in range(hit_len):
            dic[risk['label']][dic_idx] += 1

for key in dic.keys():
    if dic[key][0] + dic[key][1] != 0:
        temp = dic[key][0] / (dic[key][0] + dic[key][1])
        print(temp)
print('有敏感词的统计：\t' + str(dic))
print('没有敏感词的统计：\t' + str(dic2))
print('单个违禁类型的统计：\t' + str(dic3))
print('单个违禁类型且没有敏感词统计：\t' + str(dic4))
