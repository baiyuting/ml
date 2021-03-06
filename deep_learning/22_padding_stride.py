from mxnet import nd
from mxnet.gluon import nn


def comp_conv2d(conv2d, X):
    conv2d.initialize()
    X = X.reshape((1, 1) + X.shape)
    Y = conv2d(X)
    return Y.reshape(Y.shape[2:])  # 排除：批量和通道


conv2d = nn.Conv2D(1, kernel_size=3, padding=1)
X = nd.random.uniform(shape=(8, 8))
print(comp_conv2d(conv2d, X).shape)

conv2d = nn.Conv2D(1, kernel_size=(5, 3), padding=(2, 1))
print(comp_conv2d(conv2d, X).shape)

conv2d = nn.Conv2D(1, kernel_size=3, padding=1, strides=2)
print(comp_conv2d(conv2d, X).shape)
