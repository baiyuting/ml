from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.svm import SVC, LinearSVC
from sklearn import datasets
import numpy as np

from sklearn.datasets import make_moons

X, y = make_moons(n_samples=100, noise=0.15, random_state=42)

print(X)
print(y)

polynomial_svm_clf = Pipeline([
    ("poly_features", PolynomialFeatures(degree=3)),
    ("scaler", StandardScaler()),
    ("svm_clf", LinearSVC(C=10, loss="hinge", random_state=42))
])  # 多项式svm
polynomial_svm_clf.fit(X, y)

from sklearn.svm import SVC

poly_kernel_svm_clf = Pipeline([
    ("scaler", StandardScaler()),
    ("svm_clf", SVC(kernel="poly", degree=3, coef0=1, C=5))
])  # 多项式核函数
poly_kernel_svm_clf.fit(X, y)

rbf_kernel_svm_clf = Pipeline([
    ("scaler", StandardScaler()),
    ("svm_clf", SVC(kernel="rbf", gamma=5, C=0.001))
])  # 高斯核函数 - 径向基核函数
rbf_kernel_svm_clf.fit(X, y)

from sklearn.svm import LinearSVR

np.random.seed(42)
m = 50
X = 2 * np.random.rand(m, 1)  # m个 1维向量
y = (4 + 3 * X + np.random.randn(m, 1)).ravel()
svm_reg = LinearSVR(epsilon=1.5, random_state=42)  # 支持向量机线性回归
svm_reg.fit(X, y)

print(np.random.rand(10, 2))  # 10个2维向量
print(2 ** 3)
print(np.random.randn(10, 1))

from sklearn.svm import SVR

np.random.seed(42)
m = 100
X = 2 * np.random.rand(m, 1) - 1
y = (0.2 + 0.1 * X + 0.5 * X ** 2 + np.random.randn(m, 1) / 10).ravel()
svm_poly_reg = SVR(kernel="poly", degree=2, C=100, epsilon=0.1)
svm_poly_reg.fit(X, y)
