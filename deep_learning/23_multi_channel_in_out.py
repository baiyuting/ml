import d2lzh as d2l
from mxnet import nd


def corr2d_multi_in(X, K):
    # 沿着 X 和 K 的第0维
    return nd.add_n(*[d2l.corr2d(x, k) for x, k in zip(X, K)])


X = nd.array([[[0, 1, 2], [3, 4, 5], [6, 7, 8]],
              [[1, 2, 3], [4, 5, 6], [7, 8, 9]]])
K = nd.array([[[0, 1], [2, 3]], [[1, 2], [3, 4]]])
z = corr2d_multi_in(X, K)
print(z)


def corr2d_multi_in_out(X, K):
    return nd.stack(*[corr2d_multi_in(X, k) for k in K])


K = nd.stack(K, K + 1, K + 2)
print(K.shape)

y = corr2d_multi_in_out(X, K)
print(y)


def corr2d_multi_in_out_1x1(X, K):
    c_i, h, w = X.shape
    c_o = K.shape[0]
    X = X.reshape((c_i, h * w))
    K = K.reshape((c_o, c_i))
    Y = nd.dot(K, X)
    return Y.reshape((c_o, h, w))


X = nd.random.uniform(shape=(3, 3, 3))
K = nd.random.uniform(shape=(2, 3, 1, 1))

Y1 = corr2d_multi_in_out_1x1(X, K)
Y2 = corr2d_multi_in_out(X, K)

print((Y1 - Y2).norm().asscalar() < 1e-6)
