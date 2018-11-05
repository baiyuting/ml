from sklearn.feature_extraction.text import CountVectorizer  
from sklearn.feature_extraction.text import TfidfTransformer

tag_list = ['青年 吃货 唱歌',  
            '少年 游戏 叛逆',  
            '少年 吃货 足球'] 

vectorizer = CountVectorizer() #将文本中的词语转换为词频矩阵  
X = vectorizer.fit_transform(tag_list) #计算个词语出现的次数
print(X)
"""
{'唱歌': 2, '吃货': 1, '青年': 6, '足球': 5, '叛逆': 0, '少年': 3, '游戏': 4}
"""
word_dict = vectorizer.vocabulary_
print(word_dict)

print(vectorizer.get_feature_names())

transformer = TfidfTransformer()  
tfidf = transformer.fit_transform(X)  #将词频矩阵X统计成TF-IDF值  
print(tfidf.toarray())