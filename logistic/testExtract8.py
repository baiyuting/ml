import json
import re

import jieba

# 读取数据
with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    f.close()

with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data_2.json', 'r', encoding='utf-8') as f:
    data_temp = json.load(f)
    f.close()

data += data_temp

print("number_of_hits\t99\t1")
hit_99_1 = {}

for item in data:
    words = []
    for risk in item['risks']:
        words += risk['hit']
    num = len(words)
    if num not in hit_99_1.keys():
        hit_99_1[num] = [0, 0]
    if item['feedback_type'] == 99:
        hit_99_1[num][0] += 1
    elif item['feedback_type'] == 1:
        hit_99_1[num][1] += 1

for key in hit_99_1.keys():
    print(str(key) + "\t" + str(hit_99_1[key][0]) + "\t" + str(hit_99_1[key][1]) + '\t' + str(
        hit_99_1[key][0] / (hit_99_1[key][0] + hit_99_1[key][1])))

print("下面查看各个label有敏感词的时候，99和1的比例")
print('label\t99\t1')
sent_99_1 = {}
for item in data:
    for risk in item['risks']:
        if len(risk['hit']) != 0:
            if risk['label'] not in sent_99_1.keys():
                sent_99_1[risk['label']] = [0, 0]
            if item['feedback_type'] == 99:
                sent_99_1[risk['label']][0] += 1
            elif item['feedback_type'] == 1:
                sent_99_1[risk['label']][1] += 1

for key in sent_99_1.keys():
    print(str(key) + "\t" + str(sent_99_1[key][0]) + "\t" + str(sent_99_1[key][1]) + '\t' + str(
        sent_99_1[key][0] / (sent_99_1[key][0] + sent_99_1[key][1])))

print("下面查看各个label有敏感词的时候，不同敏感词数量下99和1的比例")
print('label\t99\t1')
label_sent_99_1 = {}
for item in data:
    for risk in item['risks']:
        if len(risk['hit']) != 0:
            num_of_hits = len(risk['hit'])
            if risk['label'] not in label_sent_99_1.keys():
                label_sent_99_1[risk['label']] = {}
            if num_of_hits not in label_sent_99_1[risk['label']].keys():
                label_sent_99_1[risk['label']][num_of_hits] = [0, 0]
            if item['feedback_type'] == 99:
                label_sent_99_1[risk['label']][num_of_hits][0] += 1
            elif item['feedback_type'] == 1:
                label_sent_99_1[risk['label']][num_of_hits][1] += 1

import xlwt

# 创建一个Workbook对象，这就相当于创建了一个Excel文件
# book = xlwt.Workbook(encoding='utf-8', style_compression=0)
#
# # 创建一个sheet对象，一个sheet对象对应Excel文件中的一张表格。
# # 在电脑桌面右键新建一个Excel文件，其中就包含sheet1，sheet2，sheet3三张表
# sheet = book.add_sheet('test', cell_overwrite_ok=True)
# row = 0
# sheet.write(row, 0, '标签类型')
# sheet.write(row, 1, '敏感词hit数')
# sheet.write(row, 2, '错误数')
# sheet.write(row, 3, '正确数')
# sheet.write(row, 4, '比例')
# row = 1
# for label in label_sent_99_1.keys():
#     for num in label_sent_99_1[label].keys():
#         print(str(label) + "\t" + str(num) + "\t" + str(label_sent_99_1[label][num]) + '\t' + str(
#             label_sent_99_1[label][num][0] / (label_sent_99_1[label][num][0] + label_sent_99_1[label][num][1])))
#         sheet.write(row, 0, label)
#         sheet.write(row, 1, num)
#         sheet.write(row, 2, label_sent_99_1[label][num][0])
#         sheet.write(row, 3, label_sent_99_1[label][num][1])
#         sheet.write(row, 4,
#                     label_sent_99_1[label][num][0] / (label_sent_99_1[label][num][0] + label_sent_99_1[label][num][1]))
#         row += 1
#
# # 最后，将以上操作保存到指定的Excel文件中
# book.save(
#     r'D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/test2.xls')  # 在字符串前加r，声明为raw字符串，这样就不会处理其中的转义了。否则，可能会报错

# 接下来查看 单个敏感词在文中出现的次数 和 99 与 1 的关系
print("num_appear_in_text\t99\t1")
number_appear_in_text = {}
for item in data:
    words = []
    for risk in item['risks']:
        words += risk['hit']
    if len(words) > 0:
        text = item['text']
        for word in words:
            num = text.count(word)
            if num not in number_appear_in_text.keys():
                number_appear_in_text[num] = [0, 0]
            if item['feedback_type'] == 99:
                number_appear_in_text[num][0] += 1
            elif item['feedback_type'] == 1:
                number_appear_in_text[num][1] += 1
for key in number_appear_in_text.keys():
    print(str(key) + '\t' + str(number_appear_in_text[key]) + '\t' + str(
        number_appear_in_text[key][0] / (number_appear_in_text[key][0] + number_appear_in_text[key][1])))

print('label\tlabel_num_appear_in_text\t99\t1')
book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('test', cell_overwrite_ok=True)
row = 0
sheet.write(row, 0, '标签类型')
sheet.write(row, 1, '敏感词在文中出现的次数')
sheet.write(row, 2, '错误数')
sheet.write(row, 3, '正确数')
sheet.write(row, 4, '比例')
row = 1
label_num_appear_in_text = {}
for item in data:
    for risk in item['risks']:
        words = []
        words += risk['hit']
        if len(words) > 0:
            if risk['label'] not in label_num_appear_in_text.keys():
                label_num_appear_in_text[risk['label']] = {}
            text = item['text']
            for word in words:
                num = text.count(word)
                if num not in label_num_appear_in_text[risk['label']].keys():
                    label_num_appear_in_text[risk['label']][num] = [0, 0]
                if item['feedback_type'] == 99:
                    label_num_appear_in_text[risk['label']][num][0] += 1
                elif item['feedback_type'] == 1:
                    label_num_appear_in_text[risk['label']][num][1] += 1
for label in label_num_appear_in_text.keys():
    for num in label_num_appear_in_text[label].keys():
        print(str(label) + '\t' + str(num) + '\t' + str(label_num_appear_in_text[label][num]) + '\t' + str(
            label_num_appear_in_text[label][num][0] / (
                    label_num_appear_in_text[label][num][0] + label_num_appear_in_text[label][num][1])))
        sheet.write(row, 0, label)
        sheet.write(row, 1, num)
        sheet.write(row, 2, label_num_appear_in_text[label][num][0])
        sheet.write(row, 3, label_num_appear_in_text[label][num][1])
        sheet.write(row, 4, label_num_appear_in_text[label][num][0] / (
                label_num_appear_in_text[label][num][0] + label_num_appear_in_text[label][num][1]))
        row += 1
book.save(
    r'D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/test3.xls')

print('single_num_appear_in_text\t99\t1')
single_num_appear_in_text = {}
for item in data:
    for risk in item['risks']:
        if len(risk['hit']) == 1:
            text = item['text']
            num = text.count(risk['hit'][0])
            if num not in single_num_appear_in_text.keys():
                single_num_appear_in_text[num] = [0, 0]
            if item['feedback_type'] == 99:
                single_num_appear_in_text[num][0] += 1
            elif item['feedback_type'] == 1:
                single_num_appear_in_text[num][1] += 1
for key in single_num_appear_in_text.keys():
    print(str(key) + '\t' + str(single_num_appear_in_text[key]) + '\t' + str(
        single_num_appear_in_text[key][0] / (single_num_appear_in_text[key][0] + single_num_appear_in_text[key][1])))

print('label\tlabel_single_num_appear_in_text\t99\t1')
book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('test', cell_overwrite_ok=True)

row = 0
sheet.write(row, 0, '标签类型')
sheet.write(row, 1, '单个敏感词在文中出现的次数')
sheet.write(row, 2, '错误数')
sheet.write(row, 3, '正确数')
sheet.write(row, 4, '比例')
row = 1

label_single_num_appear_in_text = {}
for item in data:
    for risk in item['risks']:
        if len(risk['hit']) == 1:
            if risk['label'] not in label_single_num_appear_in_text.keys():
                label_single_num_appear_in_text[risk['label']] = {}
            text = item['text']
            num = text.count(risk['hit'][0])
            if num not in label_single_num_appear_in_text[risk['label']].keys():
                label_single_num_appear_in_text[risk['label']][num] = [0, 0]
            if item['feedback_type'] == 99:
                label_single_num_appear_in_text[risk['label']][num][0] += 1
            elif item['feedback_type'] == 1:
                label_single_num_appear_in_text[risk['label']][num][1] += 1
for label in label_single_num_appear_in_text.keys():
    for num in label_single_num_appear_in_text[label].keys():
        print(str(label) + '\t' + str(num) + '\t' + str(label_single_num_appear_in_text[label][num]) + '\t' + str(
            label_single_num_appear_in_text[label][num][0] / (
                    label_single_num_appear_in_text[label][num][0] + label_single_num_appear_in_text[label][num][1])))
        sheet.write(row, 0, label)
        sheet.write(row, 1, num)
        sheet.write(row, 2, label_single_num_appear_in_text[label][num][0])
        sheet.write(row, 3, label_single_num_appear_in_text[label][num][1])
        sheet.write(row, 4, label_single_num_appear_in_text[label][num][0] / (
                label_single_num_appear_in_text[label][num][0] + label_single_num_appear_in_text[label][num][1]))
        row += 1
book.save(
    r'D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/test4.xls')

print('没有敏感词的文本分析')
book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('test', cell_overwrite_ok=True)

row = 0
sheet.write(row, 0, '广告词语在文中出现的句子所占的比例')
sheet.write(row, 1, '错误数')
sheet.write(row, 2, '正确数')
sheet.write(row, 3, '比例')
row = 1

non_sent = {}
for item in data:
    words = []
    for risk in item['risks']:
        words += risk['hit']
    if len(words) == 0:
        text = item['text']
        num = 0
        num += text.count('微信')
        num += text.count('电话')
        num += text.count('公众号')
        # num += text.count('热线')
        # num += text.count('咨询')
        num += text.count('qq')
        # sentences = re.split('[.?!。]', text)
        # for c in sentences:
        #     if '微信' in c or '电话' in c or '公众号' in c or '热线' in c or '咨询' in c or 'qq' in c:
        #         num += 1
        # num = int(num * 10 / len(sentences))
        if num not in non_sent.keys():
            non_sent[num] = [0, 0]
        if item['feedback_type'] == 99:
            non_sent[num][0] += 1
        elif item['feedback_type'] == 1:
            non_sent[num][1] += 1
for num in non_sent.keys():
    print(str(num) + '\t' + str(non_sent[num]) + '\t' + str(non_sent[num][0] / (non_sent[num][0] + non_sent[num][1])))
    sheet.write(row, 0, num)
    sheet.write(row, 1, non_sent[num][0])
    sheet.write(row, 2, non_sent[num][1])
    sheet.write(row, 3, (non_sent[num][0] / (non_sent[num][0] + non_sent[num][1])))
    row += 1

book.save(
    r'D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/test5.xls')

book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('test', cell_overwrite_ok=True)

row = 0
sheet.write(row, 0, '广告词语在文中出现的次数')
sheet.write(row, 1, '错误数')
sheet.write(row, 2, '正确数')
sheet.write(row, 3, '比例')
row = 1

non_sent = {}
for item in data:
    words = []
    for risk in item['risks']:
        words += risk['hit']
    if len(words) == 0:
        text = item['text']
        num = 0
        num += text.count('微信')
        num += text.count('电话')
        num += text.count('公众号')
        # num += text.count('热线')
        # num += text.count('咨询')
        num += text.count('qq')
        if num not in non_sent.keys():
            non_sent[num] = [0, 0]
        if item['feedback_type'] == 99:
            non_sent[num][0] += 1
        elif item['feedback_type'] == 1:
            non_sent[num][1] += 1
for num in non_sent.keys():
    print(str(num) + '\t' + str(non_sent[num]) + '\t' + str(non_sent[num][0] / (non_sent[num][0] + non_sent[num][1])))
    sheet.write(row, 0, num)
    sheet.write(row, 1, non_sent[num][0])
    sheet.write(row, 2, non_sent[num][1])
    sheet.write(row, 3, (non_sent[num][0] / (non_sent[num][0] + non_sent[num][1])))
    row += 1

book.save(
    r'D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/test6.xls')

print('接下来输出总的词语信息')
words = set()
for item in data:
    for risk in item['risks']:
        words = words.union(set(risk['hit']))
print(words)

print('输出词语对应的正确段落数和错误段落数')
words = {}
book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('test', cell_overwrite_ok=True)
row = 0
sheet.write(row, 0, '词语')
sheet.write(row, 1, '错误数')
sheet.write(row, 2, '正确数')
sheet.write(row, 3, '比例')
row = 1
for item in data:
    for risk in item['risks']:
        hits = risk['hit']
        for hit in hits:
            if hit not in words.keys():
                words[hit] = [0, 0, 0]
            if item['feedback_type'] == 99:
                words[hit][0] += 1
            elif item['feedback_type'] == 1:
                words[hit][1] += 1
            words[hit][2] = risk['label']
for hit in words.keys():
    sheet.write(row, 0, hit)
    sheet.write(row, 1, words[hit][0])
    sheet.write(row, 2, words[hit][1])
    sheet.write(row, 3, words[hit][0] / (words[hit][0] + words[hit][1]))
    sheet.write(row, 4, words[hit][2])
    row += 1
book.save(
    r'D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/test7.xls')
