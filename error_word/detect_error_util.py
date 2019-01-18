import jieba
from jpype import *


def cut_word_jieba(text):
    """
    jieba 分词
    :param text:
    :return:
    """
    return list(jieba.cut(text))


def cut_word_hanlp(text):
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
