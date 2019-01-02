# -*- coding:utf-8 -*-

import json
import re

import jieba

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

count_idle_error = 0
count_idle_error2 = 0
count_idle_error3 = 0

data2 = []  # 有敏感词
data3 = []  # 没有敏感词 【本身没有敏感词、因过滤单字和敏感词不成词而被过滤形成的敏感词】
data4 = []  # 没有敏感词 【本身没有敏感词】
data5 = []  # 没有敏感词 【因过滤单字和敏感词不成词而被过滤形成的敏感词】
data6 = []  # 没有敏感词 【过滤单字】
data7 = []  # 没有敏感词 【敏感词不成词】
for item in data:
    risks = item['risks']
    if item['feedback_type'] != 0:  # 如果说人工审核过了
        words = []
        for risk in risks:
            words += risk['hit']
        cut = list(jieba.cut(item['text']))
        cutDic = {}
        for cutItem in cut:
            cutDic[cutItem] = 1
        # 此时的 words 中有一些词不是词，是由 空格 隔开的，需要分开，分开之后长度为 1 的词不考虑
        words2 = []
        enter = 0
        multiple_words = 0
        multiples = []
        for word in words:
            splits = word.split()
            for split in splits:
                enter = 1
                if len(split) > 1:
                    multiple_words = 1  # 多字
                    multiples.append(split)
                    if split in cutDic.keys():  # 如果切分的词长度 > 1 并且 在结巴分词中
                        words2.append(split)
        if len(words2) == 0:  # 如果没有敏感词，不考虑，归到 data3 中
            temp = {"text": item['text'], 'label': item['feedback_type']}
            data3.append(temp)
            if enter == 0:
                data4.append(temp)
            else:
                if multiple_words == 0:  # 单字
                    data6.append(temp)
                else:  # 多字，敏感词不成词
                    temp['words'] = multiples
                    data7.append(temp)
                data5.append(temp)
            if item['feedback_type'] == 99:
                if enter == 1:
                    count_idle_error2 += 1
                count_idle_error += 1
            continue
        if item['feedback_type'] == 99:
            count_idle_error3 += 1
        temp = {"text": item['text'], 'words': words2, 'label': item['feedback_type']}
        data2.append(temp)  # [{"text": "hi hello", "words": ["hi", "hello"], "label": 1}]
# 写入 JSON 数据
with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data2.json', 'w', encoding='utf-8') as f:
    json.dump(data2, f, ensure_ascii=False)
    f.close()
with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data3.json', 'w', encoding='utf-8') as f:
    json.dump(data3, f, ensure_ascii=False)
    f.close()
with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data4.json', 'w', encoding='utf-8') as f:
    json.dump(data4, f, ensure_ascii=False)
    f.close()
with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data5.json', 'w', encoding='utf-8') as f:
    json.dump(data5, f, ensure_ascii=False)
    f.close()
with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data6.json', 'w', encoding='utf-8') as f:
    json.dump(data6, f, ensure_ascii=False)
    f.close()
with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data7.json', 'w', encoding='utf-8') as f:
    json.dump(data7, f, ensure_ascii=False)
    f.close()

print(count_idle_error3)
print(count_idle_error2)

print(count_idle_error)

# 读取数据
with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    f.close()
fo = open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data3.txt', 'w', encoding='utf-8')
for d in data:
    line = str(d['label']) + '\t' + str(d['words']) + '\t' + d['text'] + '\n'
    fo.write(line)
fo.close()
