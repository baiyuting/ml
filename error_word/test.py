from error_word.detect_error import detect_error
import jieba
from jpype import *


def cut_words_jieba(text):
    """
    jieba 分词
    :param text:
    :return:
    """
    return list(jieba.cut(text))


def cut_words_hanlp(text):
    """
    hanlp 分词
    :param text:
    :return:
    """
    startJVM(getDefaultJVMPath(), "-Djava.class.path=D:\hanlp\hanlp-1.7.0.jar;D:\hanlp", "-Xms1g",
             "-Xmx1g")  # 启动JVM，Linux需替换分号;为冒号:
    viterbi_segment = JPackage("com.hankcs.hanlp.seg.Viterbi").ViterbiSegment()
    s = viterbi_segment.seg(text)
    res = [item.word for item in s]
    shutdownJVM()
    return res


def test():
    f = open('test/文本.txt', 'r', encoding='utf-8')
    lines = f.readlines()
    f.close()

    text = "".join(lines)
    segments = cut_words_hanlp(text)

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


if __name__ == '__main__':
    test()
