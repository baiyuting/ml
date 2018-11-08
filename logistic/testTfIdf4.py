import json
import re
from collections import Counter

import jieba
from imblearn.over_sampling import SMOTE
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
# 接下来根据输入的词向量 集合开始 分类，此处引入 logistic 回归
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


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

# data = ['我是一个好青年', '使用sklearn提取文本的tfidf特征青年青年开心', '使用sklearn提取文本的tfidf特征青年', '我很开心', '我是一个好青年']
# target = [1, 0, 0, 1, 1]

data_train, data_test, target_train, target_test = train_test_split(data, target, test_size=0.2, random_state=42)

sent_words = [list(jieba.cut(sent0)) for sent0 in data_train]
document = [" ".join(sent0) for sent0 in sent_words]  # ['我 是 一个 好 青年', '使用 sklearn 提取 文本 的 tfidf 特征 青年 青年']

vec = CountVectorizer()  # 将文本中的词语转换为词频矩阵
X = vec.fit_transform(document)  # 计算个词语出现的次数

transformer = TfidfTransformer()
tf_idf = transformer.fit_transform(X)  # 将词频矩阵X统计成TF-IDF值
print(Counter(target_train))  # 输出训练的 标签比例

# 此处要考虑 样本不均衡问题，使用 SMOTE 平衡样本
smo = SMOTE(random_state=42)
X_smo, y_smo = smo.fit_sample(tf_idf, target_train)
print(Counter(y_smo))  # 输出样本均衡过后的 标签比例

log_reg = LogisticRegression()
log_reg.fit(X_smo, y_smo)

sent_words = [list(jieba.cut(sent0)) for sent0 in data_test]
document = [" ".join(sent0) for sent0 in sent_words]  # ['我 是 一个 好 青年', '使用 sklearn 提取 文本 的 tfidf 特征 青年 青年']
X = vec.transform(document)
tf_idf = transformer.transform(X)

score = log_reg.score(tf_idf, target_test)
print(score)  # 准确率

y_count_predict = log_reg.predict(X)

# 从sklearn.metrics 导入 classification_report。
from sklearn.metrics import classification_report

print(Counter(target_test))

# 输出更加详细的其他评价分类性能的指标
print(classification_report(target_test, y_count_predict))

count = 0
for i in range(len(target_test)):
    if target_test[i] == 0 and y_count_predict[i] == 0:
        count += 1
print(count)


# print(metrics)
