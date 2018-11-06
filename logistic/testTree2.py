import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.tree import DecisionTreeClassifier

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
tree_clf = DecisionTreeClassifier(max_depth=2)
tree_clf.fit(tf_idf, target_train)


def data_to_document(data_example):
    words = [list(jieba.cut(sent0)) for sent0 in data_example]
    docs = [" ".join(sent0) for sent0 in words]  # ['我 是 一个 好 青年', '使用 sklearn 提取 文本 的 tfidf 特征 青年 青年']
    return docs


sent_words = [list(jieba.cut(sent0)) for sent0 in data_test]
document = [" ".join(sent0) for sent0 in sent_words]  # ['我 是 一个 好 青年', '使用 sklearn 提取 文本 的 tfidf 特征 青年 青年']
X = vec.transform(document)
tf_idf = transformer.transform(X)
score = tree_clf.score(tf_idf, target_test)
print(score)  # 准确率

res = tree_clf.predict(transformer.transform(vec.transform(data_to_document(['我很开心']))))
print(res)
