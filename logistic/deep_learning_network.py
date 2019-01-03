from collections import Counter

import gluonbook as gb
import mxnet
from imblearn.over_sampling import SMOTE, RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from mxnet import gluon, init
from mxnet.contrib.text.embedding import CustomEmbedding
from mxnet.gluon import data as gdata, loss as gloss
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

from mxnet import ndarray as nd

from logistic.deep_learning_network_util import BiRNN, get_vocab, preprocess, read_total_data, get_confusion_matrix, \
    train

total_data = read_total_data()

train_data, test_data = train_test_split(total_data)

# 下采样
random_under_sampler = RandomUnderSampler()
train_data, temp = random_under_sampler.fit_resample(train_data, list(item[1] for item in train_data))

# 上采样
# random_over_sampler = RandomOverSampler()
# train_data, temp = random_over_sampler.fit_resample(train_data, list(item[1] for item in train_data))
print(Counter(temp))

vocab = get_vocab(train_data)

batch_size = 64
train_set = gdata.ArrayDataset(*preprocess(train_data, vocab))
test_set = gdata.ArrayDataset(*preprocess(test_data, vocab))
train_iter = gdata.DataLoader(train_set, batch_size, shuffle=True)
test_iter = gdata.DataLoader(test_set, batch_size)

embed_size, num_hiddens, num_layers, ctx = 300, 30, 1, gb.try_all_gpus()
net = BiRNN(vocab, embed_size, num_hiddens, num_layers)
net.initialize(init.Xavier(), ctx=ctx)

glove_embedding = CustomEmbedding(pretrained_file_path='D:/BaiduNetdiskDownload/sgns.target.word-word.dynwin5.thr10'
                                                       '.neg5.dim300.iter5/test2', vocabulary=vocab)
net.embedding.weight.set_data(glove_embedding.idx_to_vec)
net.embedding.collect_params().setattr('grad_req', 'null')

lr, num_epochs = 0.01, 5
trainer = gluon.Trainer(net.collect_params(), 'adam', {'learning_rate': lr})
loss = gloss.SoftmaxCrossEntropyLoss()
train(train_iter, test_iter, net, loss, trainer, num_epochs, batch_size)


