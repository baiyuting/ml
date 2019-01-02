import json
import re
from collections import Counter

import jieba
from imblearn.ensemble import EasyEnsembleClassifier, EasyEnsemble, BalancedBaggingClassifier, \
    BalancedRandomForestClassifier
from imblearn.under_sampling import RandomUnderSampler
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
# 接下来根据输入的词向量 集合开始 分类，此处引入 logistic 回归
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
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
with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/data7.json', 'r', encoding='utf-8') as f:
    data7 = json.load(f)
    f.close()
data2 += data7

data = []
target = []
for d in data2:
    data_temp, target_temp = get_data_target(d['text'], d['words'], d['label'])
    data += data_temp
    target += target_temp

avg_auc = 0.0
avg_accuracy = 0.0
avg_recall = 0.0
avg_accuracy0 = 0.0
avg_accuracy1 = 0.0
avg_recall0 = 0.0
avg_recall1 = 0.0
count = 10
for i in range(count):
    data_train, data_test, target_train, target_test = train_test_split(data, target)
    print(Counter(target_test))

    sent_words = [list(jieba.cut(sent0)) for sent0 in data_train]
    document = [" ".join(sent0) for sent0 in sent_words]  # ['我 是 一个 好 青年', '使用 sklearn 提取 文本 的 tfidf 特征 青年 青年']

    vec = CountVectorizer()  # 将文本中的词语转换为词频矩阵
    X = vec.fit_transform(document)  # 计算个词语出现的次数

    transformer = TfidfTransformer()
    tf_idf = transformer.fit_transform(X)  # 将词频矩阵X统计成TF-IDF值

    # vec = TfidfVectorizer()
    # tf_idf = vec.fit_transform(document)

    # 随机下采样
    # renn = RandomUnderSampler()
    # tf_idf, target_train = renn.fit_sample(tf_idf, target_train)

    # log_reg = EasyEnsembleClassifier(base_estimator=LogisticRegression(solver='lbfgs'))
    log_reg = EasyEnsembleClassifier(base_estimator=MultinomialNB())
    # log_reg = EasyEnsembleClassifier(base_estimator=DecisionTreeClassifier())
    # log_reg = LogisticRegression(solver='lbfgs')
    # log_reg = DecisionTreeClassifier()
    # log_reg = BalancedBaggingClassifier()
    # log_reg = BalancedBaggingClassifier(base_estimator=MultinomialNB())
    # log_reg = BalancedBaggingClassifier(base_estimator=LogisticRegression(solver='lbfgs'))
    # log_reg = RandomForestClassifier()
    # log_reg = SVC(gamma='auto')
    # log_reg = EasyEnsembleClassifier(base_estimator=BernoulliNB())
    # log_reg = BalancedRandomForestClassifier()
    log_reg.fit(tf_idf.toarray(), target_train)

    # log_reg = DecisionTreeClassifier(class_weight='balanced')
    # log_reg.fit(tf_idf, target_train)

    # tf_idf_train_1 = []
    # target_train_1 = []
    # tf_idf_train_0 = []
    # target_train_0 = []
    # array = tf_idf.toarray()
    # for j in range(len(target_train)):
    #     if target_train[j] == 1:
    #         tf_idf_train_1.append(array[j])
    #         target_train_1.append(1)
    #     else:
    #         tf_idf_train_0.append(array[j])
    #         target_train_0.append(-1)
    #
    # temp_train_0 = []
    # temp_target_train_0 = []
    # rate = len(target_train_1) / len(target_train_0)
    # for j in range(int(rate)):
    #     temp_train_0 += tf_idf_train_0
    #     temp_target_train_0 += target_train_0
    #
    # data_train_new = temp_train_0 + tf_idf_train_1
    # target_train_new = temp_target_train_0 + target_train_1
    # print(Counter(target_train_new))
    #
    # log_reg = MultinomialNB()
    # log_reg = DecisionTreeClassifier()
    # log_reg = LogisticRegression(solver='lbfgs')
    # log_reg.fit(data_train_new, target_train_new)

    # log_reg = OneClassSVM(gamma='auto')
    # log_reg.fit(tf_idf_train_1)

    # renn = RandomUnderSampler()
    # X_smoenn, y_smoenn = renn.fit_sample(tf_idf, target_train)
    # log_reg = SVC(gamma='auto')
    # log_reg.fit(X_smoenn, y_smoenn)

    # log_reg = LogisticRegression(solver='lbfgs')
    # log_reg.fit(X_smoenn, y_smoenn)

    # ee = EasyEnsemble(n_subsets=31)
    # X_resampled, y_resampled = ee.fit_sample(tf_idf, target_train)
    #
    # log_reg = SVC(gamma='auto')
    # for i in range(len(y_resampled)):
    #     log_reg.fit(X_resampled[i].toarray(), y_resampled[i])

    sent_words = [list(jieba.cut(sent0)) for sent0 in data_test]
    document = [" ".join(sent0) for sent0 in sent_words]  # ['我 是 一个 好 青年', '使用 sklearn 提取 文本 的 tfidf 特征 青年 青年']
    X = vec.transform(document)
    tf_idf = transformer.transform(X)
    # tf_idf = vec.transform(document)

    # renn = RandomUnderSampler()
    # tf_idf, target_test = renn.fit_sample(tf_idf, target_test)

    y_count_predict = log_reg.predict(tf_idf.toarray())

    from sklearn import metrics

    # end svm ,start metrics
    test_auc = metrics.roc_auc_score(target_test, y_count_predict)  # 验证集上的auc值
    avg_auc += test_auc

    test_accuracy = metrics.accuracy_score(target_test, y_count_predict)
    avg_accuracy += test_accuracy

    test_recall = metrics.recall_score(target_test, y_count_predict)
    avg_recall += test_recall

    c_m = confusion_matrix(target_test, y_count_predict)
    avg_accuracy0 += (c_m[0][0] * 1.0 / (c_m[1][0] + c_m[0][0]))
    avg_accuracy1 += (c_m[1][1] * 1.0 / (c_m[0][1] + c_m[1][1]))

    avg_recall0 += (c_m[0][0] * 1.0 / (c_m[0][0] + c_m[0][1]))
    avg_recall1 += (c_m[1][1] * 1.0 / (c_m[1][0] + c_m[1][1]))

avg_auc /= count
print("平均 auc " + str(avg_auc))

avg_accuracy /= count
avg_accuracy0 /= count
avg_accuracy1 /= count

avg_recall /= count
avg_recall0 /= count
avg_recall1 /= count

print('平均总精度' + str(avg_accuracy))

print('判定为-1的样本精度' + str(avg_accuracy0))
print('判定为1的样本精度' + str(avg_accuracy1))

print('-1样本召回率' + str(avg_recall0))
print('1样本找回率' + str(avg_recall1))
