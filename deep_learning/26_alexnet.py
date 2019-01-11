import d2lzh as d2l
from mxnet import gluon, init, nd
from mxnet.gluon import data as gdata, nn
import os
import sys

net = nn.Sequential()
net.add(nn.Conv2D(96, kernel_size=11, strides=4, activation='relu'),
        nn.MaxPool2D(pool_size=3, strides=2),
        # 减小卷积窗口，使用填充为 2 来使得输入输出高宽一致，且增大输出通道数。
        nn.Conv2D(256, kernel_size=5, padding=2, activation='relu'),
        nn.MaxPool2D(pool_size=3, strides=2),
        # 连续三个卷积层，且使用更小的卷积窗口。除了最后的卷积层外，进一步增大了输出通道数。
        # 前两个卷积层后不使用池化层来减小输入的高和宽。
        nn.Conv2D(384, kernel_size=3, padding=1, activation='relu'),
        nn.Conv2D(384, kernel_size=3, padding=1, activation='relu'),
        nn.Conv2D(256, kernel_size=3, padding=1, activation='relu'),
        nn.MaxPool2D(pool_size=3, strides=2),
        # 这里全连接层的输出个数比 LeNet 中的大数倍。使用丢弃层来缓解过拟合。
        nn.Dense(4096, activation='relu'), nn.Dropout(0.5),
        nn.Dense(4096, activation='relu'), nn.Dropout(0.5),
        # 输出层。由于这里使用 Fashion-MNIST，所以用类别数为 10，而非论文中的 1000。
        nn.Dense(10))
X = nd.random.uniform(shape=(1,1,224,224))
net.initialize()
for layer in net:
        X = layer(X)
        print(layer.name, 'output shape:\t', X.shape)

def load_data_fashion_mnist(batch_size, resize=None, root=os.path.join('~', '.mxnet', 'dataset', 'fashion-mnist')):
        root = os.path.expanduser(root)
        transformer = []
        if resize:
                transformer += [gdata.vision.transforms.Resize(resize)]
        transformer += [gdata.vision.transforms.ToTensor()]
        transformer = gdata.vision.transforms.Compose(transformer)
        mnist_train = gdata.vision.FashionMNIST(root=root, train=True)
        mnist_test = gdata.vision.FashionMNIST(root=root, train=False)
