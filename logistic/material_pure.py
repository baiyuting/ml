import json

# with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/material/material4.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)
#     f.close()

dd = []
for i in [1, 2, 3, 4, 5]:
    with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/material/material' + str(i) + '.json', 'r',
              encoding='utf-8') as f:
        temp = json.load(f)
        dd.append(temp)
        f.close()

for i in [1, 2, 3, 4, 5]:
    data = dd[i - 1]
    material = []
    for item in data:
        if len(item['risks']) == 1:
            material.append(item)

    with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/material/material' + str(i) + '_pure.json', 'w',
              encoding='utf-8') as f:
        json.dump(material, f, ensure_ascii=False)
        f.close()
