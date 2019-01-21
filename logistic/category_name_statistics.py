import json
import xlwt


def save_excel(path, pure_else):
    """
    保存 excel
    r'D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/material/material5_pure_else_category.xls'
    :param path:
    :param pure_else:
    :return:
    """
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
    book.save(path)


def handle_pure_else(pure_else, data):
    """
    处理 pure_else
    :param pure_else:
    :return:
    """
    text_name = {}
    for item in data:
        text_name[item['text']] = item['category_name']
    for item in pure_else:
        item['category_name'] = text_name[item['text']]


with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/export_feedback_audit_2018-12-13_adjusted.json', 'r',
          encoding='utf-8') as f:
    data = json.load(f)
    f.close()

for i in [1, 2, 3, 4, 5]:
    with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/material/material' + str(i) + '_pure_else.json',
              'r', encoding='utf-8') as f:
        pure_else = json.load(f)
        f.close()

    handle_pure_else(pure_else, data)

    with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/material/material' + str(
            i) + '_pure_else_category.json', 'w',
              encoding='utf-8') as f:
        json.dump(pure_else, f, ensure_ascii=False)
        f.close()
    save_excel(
        r'D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/material/material' + str(i) + '_pure_else_category.xls', pure_else)
