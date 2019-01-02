import jieba

import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn import metrics

with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/material/material1_pure_else.json', 'r',
          encoding='utf-8') as f:
    data = json.load(f)
    f.close()

sent_words = [list(jieba.cut(item['text'])) for item in data]
document = [" ".join(sent0) for sent0 in sent_words]  # ['我 是 一个 好 青年', '使用 sklearn 提取 文本 的 tfidf 特征 青年 青年']
vec = TfidfVectorizer()
X = vec.fit_transform(document)
X = X.toarray()

import xlwt

book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('test', cell_overwrite_ok=True)

row = 1
k = 2
while k <= 6:
    max_iterator = 300
    column = 1
    while max_iterator <= 800:
        y_pred = KMeans(n_clusters=k, max_iter=max_iterator).fit_predict(X)  # 预测值
        score = metrics.calinski_harabaz_score(X, y_pred)
        sheet.write(row, column, k)
        sheet.write(row, column, score)
        print(str(k) + '->' + str(max_iterator) + '->' + str(score))
        column += 1
        max_iterator += 100
    row += 1
    k += 1

book.save(r'D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/material/material1_pure_else.xls')

# 基本确认 k=2/max_ite=500
