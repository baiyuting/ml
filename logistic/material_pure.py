## 找出 色情类 规则
import json


with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/material/material4.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    f.close()

material_4 = []
for item in data:
    if len(item['risks']) == 1:
        material_4.append(item)

with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/material/material4_pure.json', 'w', encoding='utf-8') as f:
    json.dump(material_4, f, ensure_ascii=False)
    f.close()