import tensorflow as tf

# 创建图
x = tf.Variable(3, name="x")
y = tf.Variable(4, name='y')
f = x * x * y + y + 2

# 运行
# sess = tf.Session()
# # sess.run(x.initializer)
# # sess.run(y.initializer)
# # result = sess.run(f)
# # print(result)
# # sess.close()

# 运行方法二
# with tf.Session() as sess:
#     x.initializer.run()
#     y.initializer.run()
#     result = f.eval()
# print(result)

# 运行方法三
init = tf.global_variables_initializer()
with tf.Session() as sess:
    init.run()
    result = f.eval()
print(result)

# 运行方法四
# init = tf.global_variables_initializer()
# sess = tf.InteractiveSession()
# init.run()
# result = f.eval()
# print(result)
# sess.close()

# 创建节点会放到默认图中
# x1 = tf.Variable(1)
# print(x1.graph is tf.get_default_graph())

# 判断该图是否是默认图
# graph = tf.Graph()
# with graph.as_default():
#     x2 = tf.Variable(2)
#     print(x2.graph is tf.get_default_graph())
# print(x2.graph is tf.get_default_graph())

# 计算节点的值
# w = tf.constant(3)
# x = w + 2
# y = x + 5
# z = x * 3
# with tf.Session() as sess:
#     print(y.eval())
#     print(z.eval())

# 计算节点的值 优化
w = tf.constant(3)
x = w + 2
y = x + 5
z = x * 3
with tf.Session() as sess:
    y_val, z_val = sess.run([y, z]) # 这样不需要两次计算 w 和 x 节点
    print(y.eval())
    print(z.eval())


