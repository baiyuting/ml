
import json

# 读取数据
with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data2.json', 'r', encoding='utf-8') as f:
    data2 = json.load(f)
    f.close()

with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data7.json', 'r', encoding='utf-8') as f:
    data7 = json.load(f)
    f.close()

data2 += data7


data = []
target = []
words = []
for d in data2:
    data_temp, target_temp, words_temp = d['text'], d['label'], d['words']
    if target_temp == 99:
        target_temp = 0
    data.append(data_temp)
    target.append(target_temp)
    words.append(words_temp)


print("number_of_hits\t99\t1")
hit_99_1 = {}

for i in range(len(data)):
    num = len(words[i])
    if num not in hit_99_1.keys():
        hit_99_1[num] = [0, 0]
    if target[i] == 0:
        hit_99_1[num][0] += 1
    elif target[i] == 1:
        hit_99_1[num][1] += 1

for key in hit_99_1.keys():
    print(str(key) + "\t" + str(hit_99_1[key][0]) + "\t" + str(hit_99_1[key][1]) + '\t' + str(hit_99_1[key][0]/(hit_99_1[key][0] + hit_99_1[key][1])))

