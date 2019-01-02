import json

with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/export_feedback_audit_2018-12-13_adjusted.json', 'r',
          encoding='utf-8') as f:
    data = json.load(f)
    f.close()

with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/material/material5_pure_else.json', 'r',
          encoding='utf-8') as f:
    pure_else = json.load(f)
    f.close()

text_name = {}
for item in data:
    text_name[item['text']] = item['category_name']
for item in pure_else:
    item['category_name'] = text_name[item['text']]

with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/material/material5_pure_else_category.json', 'w', encoding='utf-8') as f:
    json.dump(pure_else, f, ensure_ascii=False)
    f.close()

import xlwt

book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('test', cell_overwrite_ok=True)
row = 0
sheet.write(row, 0, 'label')
sheet.write(row, 1, '节目分类')
sheet.write(row, 2, 'feedback_type')
row = 1

for item in pure_else:
    sheet.write(row, 0, 1)
    sheet.write(row, 1, item['category_name'])
    sheet.write(row, 2, item['feedback_type'])
    row += 1

book.save(r'D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/material/material5_pure_else_category.xls')