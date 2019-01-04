import mxnet as mx
from mxnet import nd
from mxnet.gluon import nn

print(mx.cpu(), mx.gpu())

x = nd.array([1, 2, 3])
print(x)

print(x.context)

a = nd.array([1, 2, 3], ctx=mx.gpu())
print(a)

B = nd.random.uniform(shape=(2, 3), ctx=mx.gpu())
print(B)

y = x.copyto(mx.gpu())
print(y)

z = x.as_in_context(mx.gpu())
print(z)

print(y.as_in_context(mx.gpu()) is y)
print(y.copyto(mx.gpu()) is y)

print((z + 2).exp() * y)

net = nn.Sequential()
net.add(nn.Dense(1))
net.initialize(ctx=mx.gpu())
print(net(y))

print(net[0].weight.data())
