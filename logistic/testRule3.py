## 找出 色情类 规则
import json

with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    f.close()

with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data_2.json', 'r', encoding='utf-8') as f:
    data_temp = json.load(f)
    f.close()

data += data_temp

material = [[],[],[],[],[]]

for item in data:
    for risk in item['risks']:
        material[risk['label'] - 1].append(item)

path = 'D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/material/'
for i in range(len(material)):
    temp = path + 'material' + str((i+1)) + ".json"
    # 写入 JSON 数据
    with open(temp, 'w', encoding='utf-8') as f:
        json.dump(material[i], f, ensure_ascii=False)
        f.close()

