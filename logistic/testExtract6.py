import json
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

data_audit_error = []
data_audit_right = []

data_error = []  # 错误data
data_right = []  # 正确data
for item in data:
    if item['feedback_type'] == 99:
        data_error.append(item)
    elif item['feedback_type'] == 1:
        data_right.append(item)

for index in range(len(data_error)):
    if index % 8 == 0:  # 每隔 8 个取出一个用于审核
        data_audit_error.append(data_error[index])

# 写入 JSON 数据
with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data_audit1.json', 'w', encoding='utf-8') as f:
    json.dump(data_audit_error, f, ensure_ascii=False)
    f.close()

for index in range(len(data_right)):
    if index % 80 == 0:  # 每隔 80 个取出一个用于审核
        data_audit_right.append(data_right[index])

# 写入 JSON 数据
with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data_audit1_right.json', 'w', encoding='utf-8') as f:
    json.dump(data_audit_right, f, ensure_ascii=False)
    f.close()
