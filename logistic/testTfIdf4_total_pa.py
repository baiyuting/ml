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
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC, OneClassSVM
from sklearn.tree import DecisionTreeClassifier

# 读取数据
with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data2_2.json', 'r', encoding='utf-8') as f:
    data2 = json.load(f)
    f.close()

data = []
target = []
for d in data2:
    data_temp, target_temp = d['text'], d['label']
    if target_temp == 99:
        target_temp = 0
    data.append(data_temp)
    target.append(target_temp)

# data = ['我是一个好青年', '使用sklearn提取文本的tfidf特征青年青年开心', '使用sklearn提取文本的tfidf特征青年', '我很开心', '我是一个好青年']
# target = [1, 0, 0, 1, 1]

data_train, data_test, target_train, target_test = train_test_split(data, target, random_state=42)
print(Counter(target))

sent_words = [list(jieba.cut(sent0)) for sent0 in data_train]
document = [" ".join(sent0) for sent0 in sent_words]  # ['我 是 一个 好 青年', '使用 sklearn 提取 文本 的 tfidf 特征 青年 青年']

# vec = CountVectorizer()  # 将文本中的词语转换为词频矩阵
# X = vec.fit_transform(document)  # 计算个词语出现的次数
#
# transformer = TfidfTransformer()
# tf_idf = transformer.fit_transform(X)  # 将词频矩阵X统计成TF-IDF值

vec = TfidfVectorizer()
tf_idf = vec.fit_transform(document)

print(Counter(target_train))  # 输出训练的 标签比例
print(len(tf_idf.toarray()))
print(len(tf_idf.toarray()[0]))
print(Counter(target_train).get(1))

# tf_idf_train_1 = []
# target_train_1 = []
# tf_idf_train_0 = []
# target_train_0 = []
# array = tf_idf.toarray()
# for i in range(len(target_train)):
#     if target_train[i] == 1:
#         tf_idf_train_1.append(array[i])
#         target_train_1.append(1)
#     else:
#         tf_idf_train_0.append(array[i])
#         target_train_0.append(-1)
#
# temp_train_0 = []
# temp_target_train_0 = []
# rate = len(target_train_1) / len(target_train_0)
# for i in range(int(rate)):
#     temp_train_0 += tf_idf_train_0
#     temp_target_train_0 += target_train_0

# data_train_new = temp_train_0 + tf_idf_train_1
# target_train_new = temp_target_train_0 + target_train_1
# print(Counter(target_train_new))

# 此处要考虑 样本不均衡问题，使用 SMOTE 平衡样本
# smo = SMOTE()
# X_smo, y_smo = smo.fit_sample(tf_idf, target_train)
# print(Counter(y_smo))  # 输出样本均衡过后的 标签比例

# 欠采样
# renn = RandomUnderSampler()
# X_smoenn, y_smoenn = renn.fit_sample(tf_idf, target_train)
# print(Counter(y_smoenn))

# 朴素贝叶斯
# log_reg = MultinomialNB()
# log_reg = LogisticRegression(solver='lbfgs')
# log_reg = DecisionTreeClassifier()
# log_reg = SVC(gamma='auto')
# log_reg.fit(X_smoenn, y_smoenn)


from imblearn.ensemble import EasyEnsemble

# ee = EasyEnsemble(n_subsets=31)
# ee = BalanceCascade(random_state=42,
#                     estimator=SVC(random_state=42, gamma='auto'),
#                     n_max_subset=31)
# X_resampled, y_resampled = ee.fit_sample(tf_idf, target_train)
# print(sorted(Counter(y_resampled[0]).items()))

import sklearn.neural_network as sk_nn

# log_reg = sk_nn.MLPClassifier()
# log_reg.fit(X_smoenn.toarray(), y_smoenn)

# log_reg = BaggingClassifier(random_state=42)
# log_reg.fit(X_smoenn, y_smoenn)

# log_reg = SVC(gamma='auto', class_weight="balanced")

# log_reg = VotingClassifier(estimators=[('svc', SVC(gamma='auto')), ('dt', DecisionTreeClassifier()), ('lr', LogisticRegression(
# ))], voting='hard')
#
# log_reg.fit(tf_idf.toarray(), target_train)

# log_reg = SVC(gamma='auto', class_weight='balanced')
#
# for i in range(len(y_resampled)):
#     log_reg.fit(X_resampled[i].toarray(), y_resampled[i])

# log_reg = EasyEnsembleClassifier(random_state=42,
#                                  base_estimator=MLPClassifier(random_state=42, max_iter=300))
# log_reg = EasyEnsembleClassifier(base_estimator=SVC(gamma='auto'))
# log_reg = EasyEnsembleClassifier(base_estimator=LogisticRegression(solver='lbfgs'))
# log_reg = SVC(class_weight='balanced')
# log_reg = LogisticRegression(class_weight='balanced', solver='lbfgs')
# log_reg = DecisionTreeClassifier(class_weight='balanced')
# log_reg = RandomForestClassifier(class_weight='balanced', n_estimators=100)
# log_reg = RandomForestClassifier(n_estimators=100)
log_reg = EasyEnsembleClassifier(base_estimator=MultinomialNB())
# log_reg = BalancedBaggingClassifier(base_estimator=MultinomialNB())
# log_reg = EasyEnsembleClassifier(base_estimator=GaussianNB())
# log_reg = EasyEnsembleClassifier(base_estimator=DecisionTreeClassifier())
# log_reg = EasyEnsembleClassifier(base_estimator=BernoulliNB())
# log_reg = AdaBoostClassifier(base_estimator=MultinomialNB())
log_reg.fit(tf_idf.toarray(), target_train)
# log_reg = OneClassSVM(gamma='auto')
# log_reg = IsolationForest(behaviour='new', contamination='auto')
# log_reg = EllipticEnvelope()
# print(Counter(target_train))
# log_reg.fit(tf_idf_train_1)
# print(len(tf_idf_train_1))

# 过采样
# log_reg = MultinomialNB()
# log_reg.fit(data_train_new, target_train_new)
# log_reg.fit(X_smo, y_smo)

# log_reg = LogisticRegression(solver='lbfgs', class_weight='balanced')
# log_reg = DecisionTreeClassifier(class_weight='balanced')
# log_reg = SVC(class_weight="balanced", gamma='auto')
# log_reg.fit(tf_idf, target_train)

# y = log_reg.predict(tf_idf_train_1)
# print(Counter(target_train_1))
# print(Counter(y))

sent_words = [list(jieba.cut(sent0)) for sent0 in data_test]
document = [" ".join(sent0) for sent0 in sent_words]  # ['我 是 一个 好 青年', '使用 sklearn 提取 文本 的 tfidf 特征 青年 青年']
# X = vec.transform(document)
# tf_idf = transformer.transform(X)
tf_idf = vec.transform(document)

# score = log_reg.score(tf_idf.toarray(), target_test)
# print(score)  # 准确率

# renn = RandomUnderSampler()
# tf_idf, target_test = renn.fit_sample(tf_idf, target_test)

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

# import sklearn.model_selection as sk_model_selection

# sent_words = [list(jieba.cut(sent0)) for sent0 in data]
# document = [" ".join(sent0) for sent0 in sent_words]
# X = vec.transform(document)
# tf_idf = transformer.transform(X)
# accs = sk_model_selection.cross_val_score(log_reg, tf_idf.toarray(), y=target, scoring=None, cv=10, n_jobs=1)
# print('交叉验证结果:', accs)
