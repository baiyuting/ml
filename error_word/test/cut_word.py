import jieba

import pycorrector
import re

# text = '少先队员因该为老人让坐'
f = open('文本.txt', "r", encoding="utf-8")
lines = f.readlines()
f.close()


def detect_sentence(text):
    """
    检查句子错误
    :param text:
    :return:
    """
    idx_errors = pycorrector.detect(text)
    characters = []
    for c in text:
        characters.append(c)
    for idx_error in idx_errors:
        end = idx_error[2]  # [词、位置、错误类型] [['因该', 4, 6, 2], ['坐', 10, 11, 3]]
        characters[end - 1] = characters[end - 1] + "（True）"
    text = "".join(characters)
    return text


ts = []
for line in lines:
    segs = re.split("[\.\?]", line)
    for seg in segs:
        punctuation_i = line.index(seg) + len(seg)
        punctuation = ""
        if punctuation_i < len(line):
            punctuation = line[punctuation_i]
        res = detect_sentence(seg) + punctuation
        ts.append(res)

text = "".join(ts)
f = open("文本-括号中是pycorrector修改的.txt", "w", encoding="utf-8")
f.writelines(text)
f.close()
