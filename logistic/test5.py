## 找出 色情类 规则
import json

import re
import jieba

with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/material/material5_pure_else.json', 'r',
          encoding='utf-8') as f:
    data = json.load(f)
    f.close()

temp = []
for i in range(len(data)):
    if data[i]['feedback_type'] == 99:
        temp.append(data[i])
    else:
        if i % 8 == 0:
            temp.append(data[i])

with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/material/material5_pure_else_sample.json', 'w',
          encoding='utf-8') as f:
    json.dump(temp, f, ensure_ascii=False)
    f.close()

