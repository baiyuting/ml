import xlrd
import xlwt

import math


# 定义 函数 p， 返回 对应的抽样概率
def p(p_emin, emin, emax, e):
    if e < emin:
        return p_emin
    elif emin <= e < emax:
        return p_emin + ((1 - p_emin) / (emax - emin)) * (e - emin)
    else:
        return 1


def test_p():
    p_emin = 0.5  # 监督状态时的抽样概率
    emin = 0.1
    emax = 0.2
    e = 0.3
    p_e = p(p_emin, emin, emax, e)
    print(p_e)


def get_res(sheet, p_emin, emin, emax):
    ne_1 = 0
    nr_2 = 0
    ne_2 = 0
    nr_1 = 0
    for i in range(1, sheet.nrows):  # [1, rows)
        row_i = sheet.row_values(i)  # 获取第i行内容
        ne_i = row_i[1]
        nr_i = row_i[2]
        e = row_i[3]
        p_i = p(p_emin, emin, emax, e)
        ne_i_1 = int(p_i * ne_i)
        nr_i_2 = int((1 - p_i) * nr_i)
        ne_i_2 = int((1 - p_i) * ne_i)
        nr_i_1 = int(p_i * nr_i)
        ne_1 += ne_i_1
        nr_2 += nr_i_2
        ne_2 += ne_i_2
        nr_1 += nr_i_1
    # res = math.log(ne_1) + math.log(nr_2) - math.log(ne_2) - math.log(nr_1)
    res = ne_1 + nr_2 - math.log(ne_2) - math.log(nr_1) # 第二种判别方式
    return res


if __name__ == '__main__':
    # 打开文件
    workbook = xlrd.open_workbook(r'D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/test7.xls')
    # 根据sheet索引或者名称获取sheet内容
    sheet2 = workbook.sheet_by_name('test')

    p_emin = 0.5  # 最小的抽样概率 [0.1,0.5] 0.1
    emin = 0.1  # 开始抽样时的错误率 [0.1,0.15] 0.01
    emax = 0.2  # 判定完全不能抽样的错误率 [0.17-0.2] 0.01

    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('test', cell_overwrite_ok=True)

    row = 0
    sheet.write(row, 0, 'p_emin')
    sheet.write(row, 1, 'emin')
    sheet.write(row, 2, 'emax')
    sheet.write(row, 3, 'res')
    row = 1

    for p_emin in [0.1, 0.2, 0.3, 0.4, 0.5]:
        for emin in [0.1, 0.11, 0.12, 0.13, 0.14, 0.15]:
            for emax in [0.17, 0.18, 0.19, 0.2]:
                res = get_res(sheet2, p_emin, emin, emax)
                print(p_emin, emin, emax, res)
                sheet.write(row, 0, p_emin)
                sheet.write(row, 1, emin)
                sheet.write(row, 2, emax)
                sheet.write(row, 3, res)
                row += 1

    book.save(
        r'D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/custom_function.xls')
