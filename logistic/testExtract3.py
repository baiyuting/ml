import json
import re


def get_data_target(text, keywords, label):
    sentences = re.split('[.?!。]', text)
    data = []
    target = []
    for temp in sentences:
        for kw in keywords:
            if kw in temp:
                data.append(temp)
                if label == 99:
                    target.append(0)
                else:
                    target.append(1)
                break
    print(data)
    return data, target


# 读取数据
with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data2.json', 'r', encoding='utf-8') as f:
    data2 = json.load(f)
    f.close()

data = []
target = []
for d in data2:
    data_temp, target_temp = get_data_target(d['text'], d['words'], d['label'])
    data += data_temp
    target += target_temp

dic = {0: [], 1: []}  # {label:[]}

for i in range(len(data)):
    key = target[i]
    dic[key].append(data[i])

data_dic_temp = []
target_dic_temp = []
for key in list(dic.keys()):
    data_dic_temp += dic[key]
    for label in dic[key]:
        target_dic_temp.append(key)

# 写入 data4.txt 文件
fo = open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data4.txt', 'w', encoding='utf-8')
for i in range(len(data_dic_temp)):
    line = str(target_dic_temp[i]) + '\t' + data_dic_temp[i] + '\n'
    fo.write(line)
fo.close()

from collections import Counter

print(Counter(target))
