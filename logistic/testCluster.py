# -*- coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs

plt.figure()
X, y = make_blobs(n_samples=1000, n_features=2, centers=[[-1, -1], [0, 0], [1, 1], [2, 2]],
                  cluster_std=[0.4, 0.2, 0.2, 0.2], random_state=9)  # 生成测试数据
for index, k in enumerate((2, 3, 4, 5)):
    plt.subplot(2, 2, index + 1)
    y_pred = KMeans(n_clusters=k, random_state=9).fit_predict(X)  # 预测值
    score = metrics.calinski_harabaz_score(X, y_pred)
    plt.scatter(X[:, 0], X[:, 1], c=y_pred, s=10, edgecolor='k')
    plt.text(.99, .01, ('k=%d, score: %.2f' % (k, score)),  # 文本注释，标注关键信息
             transform=plt.gca().transAxes, size=10, horizontalalignment='right')
plt.show()
