import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

# 接下来根据输入的词向量 集合开始 分类，此处引入 logistic 回归
from sklearn.linear_model import LogisticRegression

sentences = ['我是一个好青年', '使用sklearn提取文本的tfidf特征青年青年']
y = [1, 0]
log_reg = LogisticRegression()

sent_words = [list(jieba.cut(sent0)) for sent0 in
              sentences]  # [['我', '是', '一个', '好', '青年'], ['使用', 'sklearn', '提取', '文本', '的', 'tfidf', '特征', '青年', '青年']]
document = [" ".join(sent0) for sent0 in sent_words]  # ['我 是 一个 好 青年', '使用 sklearn 提取 文本 的 tfidf 特征 青年 青年']

vectorizer = CountVectorizer()  # 将文本中的词语转换为词频矩阵
X = vectorizer.fit_transform(document)  # 计算个词语出现的次数
print(X)

vocabulary = vectorizer.vocabulary_
print(vocabulary)
print(vectorizer.get_feature_names())

transformer = TfidfTransformer()
tfidf = transformer.fit_transform(X)  # 将词频矩阵X统计成TF-IDF值
vectors = tfidf.toarray()  # 词向量 集合
print(vectors)
log_reg.fit(vectors, y)

"""输入测试话语集合，使用训练模型做出预测"""
temps = ['使用sklearn提取文本的tfidf特征青年']
sent_words = [list(jieba.cut(sent0)) for sent0 in
              temps]  # [['我', '是', '一个', '好', '青年'], ['使用', 'sklearn', '提取', '文本', '的', 'tfidf', '特征', '青年', '青年']]
document = [" ".join(sent0) for sent0 in sent_words]  # ['我 是 一个 好 青年', '使用 sklearn 提取 文本 的 tfidf 特征 青年 青年']
X2 = vectorizer.transform(document)
print(X2)
tfidf = transformer.transform(X2)  # 调用训练好的 transformer 将 X 转化 为 相应的向量集合
print(tfidf.toarray())
y = log_reg.predict(tfidf.toarray())
print(y)

"""测试训练集标签"""
y_ = [0]
count = 0
for i in range(len(y)):
    if y[i] != y_[i]:
        count += 1
print(count / len(y))  # 错误率
