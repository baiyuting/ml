import json
import re
from collections import Counter

import jieba
import svm as svm
from imblearn.combine import SMOTEENN, SMOTETomek
from imblearn.ensemble import BalancedBaggingClassifier, BalanceCascade, EasyEnsembleClassifier, \
    BalancedRandomForestClassifier
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RepeatedEditedNearestNeighbours, AllKNN, EditedNearestNeighbours, ClusterCentroids, \
    RandomUnderSampler, NearMiss
from sklearn.covariance import EllipticEnvelope
from sklearn.ensemble import RandomForestClassifier, VotingClassifier, BaggingClassifier, AdaBoostClassifier, \
    IsolationForest
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
# 接下来根据输入的词向量 集合开始 分类，此处引入 logistic 回归
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC, OneClassSVM
from sklearn.tree import DecisionTreeClassifier


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

data_train, data_test, target_train, target_test = train_test_split(data, target)
print(Counter(target))

sent_words = [list(jieba.cut(sent0)) for sent0 in data_train]
document = [" ".join(sent0) for sent0 in sent_words]  # ['我 是 一个 好 青年', '使用 sklearn 提取 文本 的 tfidf 特征 青年 青年']

vec = TfidfVectorizer()
tf_idf = vec.fit_transform(document)

print(Counter(target_train))  # 输出训练的 标签比例
print(len(tf_idf.toarray()))
print(len(tf_idf.toarray()[0]))
print(Counter(target_train).get(1))

tf_idf_train_1 = []
target_train_1 = []
tf_idf_train_0 = []
target_train_0 = []
array = tf_idf.toarray()
for i in range(len(target_train)):
    if target_train[i] == 1:
        tf_idf_train_1.append(array[i])
        target_train_1.append(1)
    else:
        tf_idf_train_0.append(array[i])
        target_train_0.append(-1)

temp_train_0 = []
temp_target_train_0 = []
rate = len(target_train_1) / len(target_train_0)
for i in range(int(rate)):
    temp_train_0 += tf_idf_train_0
    temp_target_train_0 += target_train_0

data_train_new = temp_train_0 + tf_idf_train_1
target_train_new = temp_target_train_0 + target_train_1
print(Counter(target_train_new))

log_reg = MultinomialNB()
log_reg.fit(data_train_new, target_train_new)

sent_words = [list(jieba.cut(sent0)) for sent0 in data_test]
document = [" ".join(sent0) for sent0 in sent_words]  # ['我 是 一个 好 青年', '使用 sklearn 提取 文本 的 tfidf 特征 青年 青年']
tf_idf = vec.transform(document)

y_count_predict = log_reg.predict(tf_idf.toarray())
print(Counter(y_count_predict))

# 从sklearn.metrics 导入 classification_report。
from sklearn.metrics import classification_report, confusion_matrix

print(Counter(target_test))

# 输出更加详细的其他评价分类性能的指标
print(classification_report(target_test, y_count_predict))

from sklearn import metrics, svm

# end svm ,start metrics
test_auc = metrics.roc_auc_score(target_test, y_count_predict)  # 验证集上的auc值
print(test_auc)

print(confusion_matrix(target_test, y_count_predict))
