import numpy as np
from sklearn.datasets import fetch_california_housing

import tensorflow as tf

housing = fetch_california_housing()
m, n = housing.data.shape
housing_data_plus_bios = np.c_[np.ones((m, 1)), housing.data]

X = tf.constant(housing_data_plus_bios, dtype=tf.float32, name='X')
y = tf.constant(housing.target.reshape(-1, 1), dtype=tf.float32, name='y')
XT = tf.transpose(X)
theta = tf.matmul(tf.matmul(tf.matrix_inverse(tf.matmul(XT, X)), XT), y)

with tf.Session() as sess:
    theta_value = theta.eval()

print(theta_value)

from sklearn.linear_model import LinearRegression

lin_reg = LinearRegression()
lin_reg.fit(housing.data, housing.target.reshape(-1, 1))
print(np.r_[lin_reg.intercept_.reshape(-1, 1), lin_reg.coef_.T])
# print(lin_reg.intercept_.reshape(-1, 1))
# print(lin_reg.coef_.T)

X = housing_data_plus_bios
y = housing.target.reshape(-1,1)
theta_numpy = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(y)
print(theta_numpy)

