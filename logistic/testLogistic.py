import numpy as np

from sklearn import datasets

iris = datasets.load_iris()
X = iris['data'][:, 3:]  # [[1,2],[3,4]] tf-idf
y = (iris['target'] == 2).astype(np.int)  # [1,2]

print(X)
print(y)


from sklearn.linear_model import LogisticRegression

log_reg = LogisticRegression()
log_reg.fit(X, y)

X = [[4.9]]  # 开始预测
y = log_reg.predict(X)
print(y)
