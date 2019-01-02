# -*- coding: utf-8 -*-
# 导入xlwt模块
import xlwt

import json
import jieba

# 创建一个Workbook对象，这就相当于创建了一个Excel文件
book = xlwt.Workbook(encoding='utf-8', style_compression=0)

# 创建一个sheet对象，一个sheet对象对应Excel文件中的一张表格。
# 在电脑桌面右键新建一个Excel文件，其中就包含sheet1，sheet2，sheet3三张表
sheet = book.add_sheet('test', cell_overwrite_ok=True)

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

data_0_0 = []  # 无敏感词 错误
data_0_1 = []  # 无敏感词 正确
data_1_0 = []  # 有敏感词 错误
data_1_1 = []  # 有敏感词 正确

for item in data:
    words = []
    for risk in item['risks']:
        words += risk['hit']
    if len(words) == 0:
        if item['feedback_type'] == 99:
            data_0_0.append(item)
        elif item['feedback_type'] == 1:
            data_0_1.append(item)
    else:
        if item['feedback_type'] == 99:
            data_1_0.append(item)
        elif item['feedback_type'] == 1:
            data_1_1.append(item)

data = [data_0_0, data_0_1, data_1_0, data_1_1]
gap = [3, 74, 10, 78]
handle_check = ['未通过', '通过', '未通过', '通过']

sheet.write(0, 0, '敏感词')
sheet.write(0, 1, '文本内容')
sheet.write(0, 2, '人工审核结果')
sheet.write(0, 3, '复审结果')
sheet.write(0, 4, '复审理由')

row = 1

for i in range(len(data)):
    for j in range(len(data[i])):
        item = data[i][j]
        if item['feedback_type'] != 99:
            continue
        # if (j + 1) % gap[i] == 0: # 此时开始输出
        words = []
        for risk in item['risks']:
            label = ''
            if risk['label'] == 1:
                label = '暴恐违禁'
            elif risk['label'] == 2:
                label = '文本色情'
            elif risk['label'] == 3:
                label = '政治敏感'
            elif risk['label'] == 4:
                label = '恶意推广'
            elif risk['label'] == 5:
                label = '低俗辱骂'
            words.append(label + ':' + str(risk['hit']))
        sheet.write(row, 0, str(words))
        sheet.write(row, 1, item['text'])
        sheet.write(row, 2, handle_check[i])
        row += 1

# 其中的test是这张表的名字,cell_overwrite_ok，表示是否可以覆盖单元格，其实是Worksheet实例化的一个参数，默认值是False
# 向表test中添加数据
# sheet.write(0, 0, 'EnglishName')  # 其中的'0-行, 0-列'指定表中的单元，'EnglishName'是向该单元写入的内容
# sheet.write(1, 0, 'Marcovaldo')
# txt1 = '中文名字'
# sheet.write(0, 1, txt1)  # 此处需要将中文字符串解码成unicode码，否则会报错
# txt2 = '马可瓦多'
# sheet.write(1, 1, txt2)

# 最后，将以上操作保存到指定的Excel文件中
book.save(r'D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/取样数据用于提供审核理由.xls')  # 在字符串前加r，声明为raw字符串，这样就不会处理其中的转义了。否则，可能会报错
