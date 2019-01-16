import jieba

import pycorrector

# text = '少先队员因该为老人让坐'
f = open('文本.txt', "r", encoding="utf-8")
lines = f.readlines()
f.close()

text = "".join(lines)
idx_errors = pycorrector.detect(text)
characters = []
for c in text:
    characters.append(c)

for idx_error in idx_errors:
    end = idx_error[2]  # [词、位置、错误类型] [['因该', 4, 6, 2], ['坐', 10, 11, 3]]
    characters[end - 1] = characters[end - 1] + "（True）"

text = "".join(characters)
f = open("文本-括号中是pycorrector修改的.txt", "w", encoding="utf-8")
f.writelines(text)
f.close()
