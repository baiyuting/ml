import json
import re

import jieba

# 读取数据
import xlwt

with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    f.close()

with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data_2.json', 'r', encoding='utf-8') as f:
    data_temp = json.load(f)
    f.close()

data += data_temp

no_hit_data = []
has_hit_data = []

for item in data:
    words = []
    for risk in item['risks']:
        words += risk['hit']
    if len(words) == 0:
        no_hit_data.append(item)

book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('test', cell_overwrite_ok=True)
row = 0
sheet.write(row, 0, '词语')
sheet.write(row, 1, '数量')
row = 1

word_num = {}

for item in no_hit_data:
    if item['feedback_type'] == 99:
        text = item['text']
        cut_words = list(jieba.cut(text))
        for cut_word in cut_words:
            if len(cut_word) <= 1:
                continue
            if cut_word not in word_num.keys():
                word_num[cut_word] = 0
            word_num[cut_word] += 1
for cut_word in word_num.keys():
    sheet.write(row, 0, cut_word)
    sheet.write(row, 1, word_num[cut_word])
    row += 1
book.save(r'D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/no_hit_data_error_word_num.xls')


with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/no_hit_data.json', 'w', encoding='utf-8') as f:
    json.dump(no_hit_data, f, ensure_ascii=False)
    f.close()