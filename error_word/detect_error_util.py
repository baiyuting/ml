import re

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
    hanlp 分词，返回分词和词性
    :param text:
    :return:
    """
    startJVM(getDefaultJVMPath(), "-Djava.class.path=D:\hanlp\hanlp-1.7.0.jar;D:\hanlp", "-Xms1g",
             "-Xmx1g")  # 启动JVM，Linux需替换分号;为冒号:
    viterbi_segment = JPackage("com.hankcs.hanlp.seg.Viterbi").ViterbiSegment()
    s = viterbi_segment.seg(text)
    res = [item.word for item in s]
    res_pos = [str(item.nature) for item in s]
    shutdownJVM()
    return res, res_pos


def cut_pos_hanlp(text):
    """
    hanlp 词性获取
    :param text:
    :return:
    """
    startJVM(getDefaultJVMPath(), "-Djava.class.path=D:\hanlp\hanlp-1.7.0.jar;D:\hanlp", "-Xms1g",
             "-Xmx1g")  # 启动JVM，Linux需替换分号;为冒号:
    viterbi_segment = JPackage("com.hankcs.hanlp.seg.Viterbi").ViterbiSegment()
    s = viterbi_segment.seg(text)
    res = [str(item.nature) for item in s]
    shutdownJVM()
    return res


def get_exclamation():
    """
    获取感叹词-常用
    一般放在句首
    :return:
    """
    return '^(啊|哎|唉|嗨|咳|呵|嗬|嘿|哼|嚯|呃|嗯|喂|噢|嚄|哦|呀|咦|哟|呦|哎呀|啊呀|哎哟|啊哟|哈+)$'


def is_exclamation_word(word):
    """
    判断是否是感叹词
    :param word:
    :return:
    """
    return re.match(get_exclamation(), word) is not None


def get_mood_words():
    """
    获取语气词-常用
    来源于 https://baike.baidu.com/item/%E8%AF%AD%E6%B0%94%E8%AF%8D/1267117?fr=aladdin
    一般放在句末
    :return:
    """
    return "^[的了么呢吧吗嘛啊]$"


def is_mood_word(word):
    """
    是否是语气词
    :param word:
    :return:
    """
    return re.match(get_mood_words(), word) is not None


def contain_mood_word(seg):
    """
    判断句段中是否包含 语气词
    :param seg:
    :return:
    """
    for char in seg:
        if is_mood_word(char):
            return True
    return False


def contain_preposition_word(seg):
    """
    是否包含介词
    介词：
    临乎与为共冲到兜于即从以似假去让诸及往迆连迎道遵对导寻将当叫吃合同向和问如尽打执把投拦按捉洎给维缘在因惟就比照较方爿暨拿替望朝爰直由率被用繇齐至管自起趁践跟
    http://xh.5156edu.com/page/z3033m4876j18636.html
    :return:
    """
    for char in seg:
        if re.match("[临乎与为共冲到兜于即从以似假去让诸及往迆连迎道遵对导寻将当叫吃合同向和问如尽打执把投拦按捉洎给维缘在因惟就比照较方爿暨拿替望朝爰直由率被用繇齐至管自起趁践跟]", char):
            return True
    return False


def contain_auxiliary_verb_word(seg):
    """
    是否包含助动词
    当|得|该|该当|敢|敢于|会|可|可能|可以|肯|乐意|能|能够|让|容许|希望|想|要|应|应当|应该|愿|愿意|允许|自愿
    :param seg:
    :return:
    """
    for char in seg:
        if re.match("当|得|该|该当|敢|敢于|会|可|可能|可以|肯|乐意|能|能够|让|容许|希望|想|要|应|应当|应该|愿|愿意|允许|自愿", char):
            return True
    return False


def contain_vshi_word(seg):
    """
    是否包含 动词 是
    :param seg:
    :return:
    """
    return contain_certain_pattern_seg("是", seg)


def contain_certain_pattern_seg(pattern, seg):
    """
    文本中 字符 是否包含 特定格式 信息
    :param pattern:
    :param seg:
    :return:
    """
    for char in seg:
        if re.match(pattern, char):
            return True
    return False


def contain_locality_word(seg):
    """
    是否包含方位词
    上下前后左右东西南北中内外里间旁
    http://xh.5156edu.com/page/z9084m6671j19732.html
    :param seg:
    :return:
    """
    return contain_certain_pattern_seg("[上下前后左右东西南北中内外里间旁]", seg)


def is_seg_chinese(seg):
    """
    文本段 是否都是中文
    :param seg:
    :return:
    """
    for char in seg:
        if not is_character_chinese(char):
            return False
    return True


def is_character_chinese(char):
    """
    该字符是否是中文
    :param char:
    :return:
    """
    return u'\u4e00' <= char <= u'\u9fff'
