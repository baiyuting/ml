import collections
import json
import time

import jieba
from mxnet import nd, autograd
from mxnet.contrib import text
from mxnet.gluon import nn, rnn
from mxnet.gluon.loss import Loss

import d2lzh as d2l


class BiRNN(nn.Block):
    """
    循环网络，二分类
    """

    def __init__(self, vocab, embed_size, num_hiddens, num_layers, **kwargs):
        super(BiRNN, self).__init__(**kwargs)
        self.embedding = nn.Embedding(len(vocab), embed_size)
        # bidirectional 设 True 即得到双向循环神经网络。
        self.encoder = rnn.LSTM(num_hiddens, num_layers=num_layers,
                                bidirectional=True, input_size=embed_size)
        self.decoder = nn.Dense(2)

    def forward(self, inputs):
        # inputs 的形状是（批量大小，词数），因为 LSTM 需要将序列作为第一维，所以将输入转
        # 置后再提取词特征，输出形状为（词数，批量大小，词向量维度）。
        embeddings = self.embedding(inputs.T)
        # states 形状是（词数，批量大小，2 * 隐藏单元个数）。
        states = self.encoder(embeddings)
        # 连结初始时间步和最终时间步的隐藏状态作为全连接层输入。它的形状为（批量大小，
        # 4 * 隐藏单元个数）。
        encoding = nd.concat(states[0], states[-1])
        outputs = self.decoder(encoding)
        return outputs


def get_tokenized(data):  # 本函数已保存在 gluonbook 包中方便以后使用。
    """
    :param data: 数据 [[text, 1]]
    :return: [[token1,token2],[token3, token4]]
    """

    def tokenizer(text):
        split_ = list(jieba.cut(text))  # 中文分词
        return split_

    return [tokenizer(review) for review, _ in data]


def get_vocab(data):  # 本函数已保存在 gluonbook 包中方便以后使用。
    tokenized_data = get_tokenized(data)
    counter = collections.Counter([tk for st in tokenized_data for tk in st])
    return text.vocab.Vocabulary(counter, min_freq=5)  # 次数 <5 过滤


def get_external_vocab():
    """
    自定义词典，从其他来源
    :return: 返回一个词典
    """
    return


def preprocess(data, vocab):  # 本函数已保存在 gluonbook 包中方便以后使用。
    max_l = 500  # 将每条评论通过截断或者补 0，使得长度变成 500。

    def pad(x):
        return x[:max_l] if len(x) > max_l else x + [0] * (max_l - len(x))

    tokenized_data = get_tokenized(data)
    features = nd.array([pad(vocab.to_indices(x)) for x in tokenized_data])
    labels = nd.array([score for _, score in data])
    return features, labels


def read_total_data():
    """
    获取所有的数据
    :return: [[text1,0],[text2,1]]
    """
    data = []
    res = read_source_data()
    for item in res:
        if item['feedback_type'] == 0:
            continue
        data.append([item['text'], 0 if item['feedback_type'] == 99 else 1])  # 99:0 1:1
    return data


def read_source_data():
    """读取原始数据"""
    res = []
    with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/export_feedback_audit_2018-12-13.json', 'r',
              encoding='utf-8') as f:
        res += json.load(f)
        f.close()
    return res


def get_confusion_matrix(test_iter, net):
    """
    :param test_iter: 测试集迭代器
    :param net: 训练好的网络
    :return: 混淆矩阵
        0   1
    0   xx  xx
    1   xx  xx
    """
    y = []
    y_true = []
    for batch in test_iter:
        y_true += batch[1].asnumpy().tolist()
        y += net(batch[0]).argmax(axis=1).asnumpy().tolist()
    m = nd.zeros((2, 2), dtype='int32').asnumpy().tolist()
    for i in range(len(y)):
        m[int(y[i])][int(y_true[i])] += 1
    print("0精度", 0 if (m[0][0] + m[0][1]) == 0 else m[0][0] * 1.0 / (m[0][0] + m[0][1]))
    print("1精度", 0 if (m[1][0] + m[1][1]) == 0 else m[1][1] * 1.0 / (m[1][0] + m[1][1]))
    print("0召回", 0 if (m[0][0] + m[1][0]) == 0 else m[0][0] * 1.0 / (m[0][0] + m[1][0]))
    print("1召回", 0 if (m[0][1] + m[1][1]) == 0 else m[1][1] * 1.0 / (m[0][1] + m[1][1]))
    return m


def confusion_matrix(test_iter, net, ctx, loss):
    """
    生成混淆矩阵
    :param test_iter:
    :param net:
    :param ctx:
    :param loss:
    :return:
        0   1
    0   X   X
    1   X   X
    """
    test_acc_sum = 0.0
    test_n = 0
    test_l_sum = 0.0
    m = nd.zeros(shape=(2, 2), ctx=ctx)
    for X, y in test_iter:
        X = X.as_in_context(ctx)
        y = y.as_in_context(ctx)
        y_hat = net(X)
        y_ = y_hat.argmax(axis=1)
        test_acc_sum += (y_ == y).sum().asscalar()
        test_n += y.size
        test_l_sum += loss(y_hat, y).sum().asscalar()
        for i in range(y.size):
            if y[i] == y_[i]:
                if y[i] == 1:
                    m[1][1] += 1
                else:
                    m[0][0] += 1
            else:
                if y[i] == 0:
                    m[0][1] += 1
                else:
                    m[1][0] += 1
    return m, test_acc_sum, test_n, test_l_sum


class MyLoss(Loss):
    def __init__(self, axis=-1, weight=None, batch_axis=0, **kwargs):
        super(MyLoss, self).__init__(weight, batch_axis, **kwargs)
        self._axis = axis

    def hybrid_forward(self, F, pred, label, sample_weight=None):
        p = F.softmax(pred, self._axis)
        pred = (1 - p) * F.log_softmax(pred, self._axis)
        loss = -F.pick(pred, label, axis=self._axis, keepdims=True)
        return F.mean(loss, axis=self._batch_axis, exclude=True)


def train(train_iter, test_iter, net, loss, trainer, num_epochs, batch_size, ctx):
    train_ls, test_ls = [], []
    for epoch in range(num_epochs):
        train_l_sum, n, train_acc_sum, test_acc_sum, start = 0.0, 0, 0.0, 0.0, time.time()
        for X, y in train_iter:
            X = X.as_in_context(ctx)
            y = y.as_in_context(ctx)
            with autograd.record():
                y_hat = net(X)
                y_ = y_hat.argmax(axis=1)
                l = loss(y_hat, y)
            l.backward()
            trainer.step(batch_size)
            train_l_sum += l.sum().asscalar()
            train_acc_sum += (y_ == y).sum().asscalar()
            n += y.size
        m, test_acc_sum, test_n, test_l_sum = confusion_matrix(test_iter, net, ctx, loss)
        train_ls.append(train_l_sum / n)
        test_ls.append(test_l_sum / test_n)
        print('epoch %d, loss %.4f, train_acc %.3f, test_acc %.3f, time %.1f sec, test_confusion_matrix is' % (
            epoch, (train_l_sum / n), (train_acc_sum / n), (test_acc_sum / test_n), time.time() - start), m)
    d2l.semilogy(range(1, num_epochs + 1), train_ls, 'epochs', 'loss', range(1, num_epochs + 1), test_ls,
                 ['train', 'test'])
