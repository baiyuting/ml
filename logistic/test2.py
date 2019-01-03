import mxnet.ndarray as nd

y_true = nd.array([0, 1, 1, 0])
y_pred = nd.array([1, 1, 0, 0])
l = y_true == 1
l2 = y_pred == 1
l3 = y_true == y_pred
print(l)
print(l2)
print(l3)

if l3[3] == 1:
    print('hi')

l3[3] += 1
print(l3[3])

print('number is %f, confusion_matrix is ' % (2), l3)
