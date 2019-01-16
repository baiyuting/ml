from error_word.detect_error import detect_error
import jieba

f = open('test/文本.txt', 'r', encoding='utf-8')
lines = f.readlines()
f.close()

text = "".join(lines)
segments = list(jieba.cut(text))

print(segments)
position_res = detect_error(segments, text)
print(position_res)

for i in range(len(segments)):
    if position_res[i]:  # 有问题的情况下
        segments[i] = segments[i] + "（" + str(position_res[i]) + "）"

text = "".join(segments)
f = open('test/文本-括号中是机器修改的.txt', 'w', encoding='utf-8')
f.writelines(text)
f.close()
