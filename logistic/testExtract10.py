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

data_for_machine = []
for i in range(len(data)):
    if (i + 1) % 100 == 0:
        # data[i]['feedback_type'] = 0
        data_for_machine.append(data[i])

with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data_for_machine.json', 'w', encoding='utf-8') as f:
    json.dump(data_for_machine, f, ensure_ascii=False)
    f.close()
    