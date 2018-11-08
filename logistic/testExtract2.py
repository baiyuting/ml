# -*- coding:utf-8 -*-

import json

# 读取数据
with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    print(data[0])
    f.close()

# 写入 JSON 数据
with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data2.json', 'w', encoding='utf-8') as f:
    res = []
    for item in data:
        risks = item['risks']
        if item['feedback_type'] != 0:  # 如果说人工审核过了
            words = []
            for risk in risks:
                words += risk['hit']
            # 此时的 words 中有一些词不是词，是由 空格 隔开的，需要分开，分开之后长度为 1 的词不考虑
            words2 = []
            for word in words:
                splits = word.split()
                for split in splits:
                    if len(split) > 1:
                        words2.append(split)
            if len(words) == 0:  # 如果没有敏感词，不考虑
                continue
            temp = {"text": item['text'], 'words': words2, 'label': item['feedback_type']}
            res.append(temp)  # [{"text": "hi hello", "words": ["hi", "hello"], "label": 1}]
    json.dump(res, f, ensure_ascii=False)
    f.close()

# 读取数据
with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    f.close()
fo = open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data3.txt', 'w', encoding='utf-8')
for d in data:
    line = str(d['label']) + '\t' + str(d['words']) + '\t' + d['text'] + '\n'
    fo.write(line)
fo.close()
