import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

# 接下来根据输入的词向量 集合开始 分类，此处引入 logistic 回归
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

data = ['我是一个好青年', '使用sklearn提取文本的tfidf特征青年青年开心', '使用sklearn提取文本的tfidf特征青年', '我很开心', '我是一个好青年']
target = [1, 0, 0, 1, 1]

data_train, data_test, target_train, target_test = train_test_split(data, target, test_size=0.4, random_state=42)

sent_words = [list(jieba.cut(sent0)) for sent0 in data_train]
document = [" ".join(sent0) for sent0 in sent_words]  # ['我 是 一个 好 青年', '使用 sklearn 提取 文本 的 tfidf 特征 青年 青年']

vec = CountVectorizer()  # 将文本中的词语转换为词频矩阵
X = vec.fit_transform(document)  # 计算个词语出现的次数

transformer = TfidfTransformer()
tf_idf = transformer.fit_transform(X)  # 将词频矩阵X统计成TF-IDF值
vectors = tf_idf.toarray()  # 词向量 集合
log_reg = LogisticRegression()
log_reg.fit(vectors, target_train)

sent_words = [list(jieba.cut(sent0)) for sent0 in data_test]
document = [" ".join(sent0) for sent0 in sent_words]  # ['我 是 一个 好 青年', '使用 sklearn 提取 文本 的 tfidf 特征 青年 青年']
X = vec.transform(document)
tf_idf = transformer.transform(X)
score = log_reg.score(tf_idf.toarray(), target_test)
print(score)
