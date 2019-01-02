from mxnet import autograd, nd

x = nd.arange(4).reshape((4, 1))
print(x)

x.attach_grad()

with autograd.record():
    y = 2 * nd.dot(x.T, x)
    y.backward()
    print(x.grad)

def f(a):
    b = a* 2
    while b.norm().asscalar() < 1000:
        b = b * 2
    if b.sum().asscalar() < 1000:
        c = b
    else:
        c = 100 * b
    return c

a = nd.random.normal(shape=1)
a.attach_grad()
with autograd.record():
    c = f(a)
c.backward()
print(a.grad == c/a)