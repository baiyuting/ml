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
with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data2.json', 'r', encoding='utf-8') as f:
    data2 = json.load(f)
    f.close()

with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data7.json', 'r', encoding='utf-8') as f:
    data7 = json.load(f)
    f.close()

data2 += data7

data = []
target = []
words = []
for d in data2:
    data_temp, target_temp, words_temp = d['text'], d['label'], d['words']
    if target_temp == 99:
        target_temp = 0
    data.append(data_temp)
    target.append(target_temp)
    words.append(words_temp)

count = 1
c = [[0, 0], [0, 0]]
for index in range(count):
    data_train, data_test, target_train, target_test = train_test_split(data, target)
    print(Counter(target))

    sent_words = [list(jieba.cut(sent0)) for sent0 in data_train]
    document = [" ".join(sent0) for sent0 in sent_words]  # ['我 是 一个 好 青年', '使用 sklearn 提取 文本 的 tfidf 特征 青年 青年']

    vec = TfidfVectorizer()
    tf_idf = vec.fit_transform(document)

    log_reg = EasyEnsembleClassifier(base_estimator=MultinomialNB())
    log_reg.fit(tf_idf.toarray(), target_train)

    sent_words = [list(jieba.cut(sent0)) for sent0 in data_test]
    document = [" ".join(sent0) for sent0 in sent_words]  # ['我 是 一个 好 青年', '使用 sklearn 提取 文本 的 tfidf 特征 青年 青年']
    tf_idf = vec.transform(document)

    y_count_predict = log_reg.predict(tf_idf.toarray())
    print(Counter(y_count_predict))

    from sklearn.metrics import classification_report, confusion_matrix

    print(Counter(target_test))

    print(classification_report(target_test, y_count_predict))

    from sklearn import metrics, svm

    test_auc = metrics.roc_auc_score(target_test, y_count_predict)  # 验证集上的auc值
    print(test_auc)

    print(confusion_matrix(target_test, y_count_predict))

    matrix = confusion_matrix(target_test, y_count_predict)
    c[0][0] += matrix[0][0]
    c[0][1] += matrix[0][1]
    c[1][0] += matrix[1][0]
    c[1][1] += matrix[1][1]



print(c)