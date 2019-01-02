import json
import re
from collections import Counter

import jieba
from imblearn.ensemble import EasyEnsembleClassifier
from imblearn.under_sampling import RandomUnderSampler
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
# 接下来根据输入的词向量 集合开始 分类，此处引入 logistic 回归
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC


def get_data_target(text, keywords, label):
    sentences = re.split('[.?!。]', text)
    data = []
    target = []
    for temp in sentences:
        for kw in keywords:
            if kw in temp:
                data.append(temp)
                if label == 99:
                    target.append(-1)
                else:
                    target.append(1)
                break
    # print(data)
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

data_train, data_test, target_train, target_test = train_test_split(data, target)

sent_words = [list(jieba.cut(sent0)) for sent0 in data_train]
document = [" ".join(sent0) for sent0 in sent_words]  # ['我 是 一个 好 青年', '使用 sklearn 提取 文本 的 tfidf 特征 青年 青年']

vec = CountVectorizer()  # 将文本中的词语转换为词频矩阵
X = vec.fit_transform(document)  # 计算个词语出现的次数

transformer = TfidfTransformer()
tf_idf = transformer.fit_transform(X)  # 将词频矩阵X统计成TF-IDF值
print(Counter(target_train))  # 输出训练的 标签比例
print(len(tf_idf.toarray()))
print(len(tf_idf.toarray()[0]))
print(Counter(target_train).get(1))

log_reg = EasyEnsembleClassifier(base_estimator=SVC(gamma='auto'))
log_reg.fit(tf_idf.toarray(), target_train)

sent_words = [list(jieba.cut(sent0)) for sent0 in data_test]
document = [" ".join(sent0) for sent0 in sent_words]  # ['我 是 一个 好 青年', '使用 sklearn 提取 文本 的 tfidf 特征 青年 青年']
X = vec.transform(document)
tf_idf = transformer.transform(X)

y_count_predict = log_reg.predict(tf_idf.toarray())
print(Counter(y_count_predict))

# 从sklearn.metrics 导入 classification_report。
from sklearn.metrics import classification_report, confusion_matrix

print(Counter(target_test))

# 输出更加详细的其他评价分类性能的指标
print(classification_report(target_test, y_count_predict))

from sklearn import metrics

# end svm ,start metrics
test_auc = metrics.roc_auc_score(target_test, y_count_predict)  # 验证集上的auc值
print(test_auc)

print(confusion_matrix(target_test, y_count_predict))
