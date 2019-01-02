import json
import re

import jieba

# 读取数据
import xlwt

with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    f.close()

with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data_2.json', 'r', encoding='utf-8') as f:
    data_temp = json.load(f)
    f.close()

data += data_temp

print(len(data))

data_for_terrorist = []

count = 1
for item in data:
    for risk in item['risks']:
        if risk['label'] == 1:
            if count % 80 == 0:
                item['feedback_type'] = 0
                data_for_terrorist.append(item)
            count += 1

data_for_sex = []
count = 1
for item in data:
    for risk in item['risks']:
        if risk['label'] == 2:
            if count % 8 == 0:
                item['feedback_type'] = 0
                data_for_sex.append(item)
            count += 1

with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data_for_terrorist.json', 'w', encoding='utf-8') as f:
    json.dump(data_for_terrorist, f, ensure_ascii=False)
    f.close()

with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data_for_sex.json', 'w', encoding='utf-8') as f:
    json.dump(data_for_sex, f, ensure_ascii=False)
    f.close()