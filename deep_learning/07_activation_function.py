import gluonbook as gb
from mxnet import autograd, nd

def xyplot(x_vals, y_vals, name):
    gb.set_figsize(figsize=(5, 2.5))
    gb.plt.plot(x_vals.asnumpy(), y_vals.asnumpy())
    gb.plt.xlabel('x')
    gb.plt.ylabel(name + '(x)')
    gb.plt.show()

x = nd.arange(-8, 8, 0.1)
y = x.relu()
xyplot(x, y, 'relu')

x.attach_grad()
with autograd.record():
    y = x.relu()
y.backward()
xyplot(x, x.grad, 'grad of relu')



with autograd.record():
    y = x.sigmoid()
xyplot(x, y, 'sigmoid')

y.backward()
xyplot(x, x.grad, 'grad of sigmoid')


with autograd.record():
    y = x.tanh()
xyplot(x, y, 'tanh')

y.backward()
xyplot(x, x.grad, 'grad of tanh')