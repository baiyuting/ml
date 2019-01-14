import json

import re
import jieba

with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/material/material3_pure.json', 'r',
          encoding='utf-8') as f:
    data = json.load(f)
    f.close()

material_3 = []
material_else = []
for item in data:
    # if len(item['risks'][0]['hit']) == 0:
    #     material_3.append(item)
    word_split = 0
    for sen in re.split('[.?!。]', item['text']):  # 对于每一句话
        for item_risk in item['risks']:  # 对于每一个 risk
            for word in item_risk['hit']:  # 对于每一个敏感词
                if word in sen:
                    cuts = list(jieba.cut(sen))
                    for c in cuts:
                        if len(c) == 1:
                            continue
                        if word in c or c in word:
                            word_split = 1

    if word_split == 0:
        material_3.append(item)
    else:
        material_else.append(item)

with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/material/material3_pure_cut_error.json', 'w',
          encoding='utf-8') as f:
    json.dump(material_3, f, ensure_ascii=False)
    f.close()

with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/material/material3_pure_else.json', 'w',
          encoding='utf-8') as f:
    json.dump(material_else, f, ensure_ascii=False)
    f.close()
