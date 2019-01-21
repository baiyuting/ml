"""
初始化模型
"""

from error_word.detect_error_model import get_one_word_model, get_two_words_model, get_three_words_model, \
    get_one_character_model, get_two_characters_model, get_three_characters_model

# 词模型
from error_word.detect_error_util import is_character_chinese, is_seg_chinese, contain_mood_word

one_word_model = get_one_word_model()
two_words_model = get_two_words_model()
three_words_model = get_three_words_model()
words_model = [one_word_model, two_words_model, three_words_model]

# 字模型
one_character_model = get_one_character_model()
two_characters_model = get_two_characters_model()
three_characters_model = get_three_characters_model()
characters_model = [one_character_model, two_characters_model, three_characters_model]

# 字词模型
word_character_model = [words_model, characters_model]


def R(segments, word_or_character):
    """
    计算 连续字词 的 共现频次
    :param segments:
    :param word_or_character: word 0| character 1
    :return:
    """
    model = word_character_model[word_or_character][len(segments) - 1]  # 获取对应的字词模型
    key = " ".join(segments)  # 获取查询对应模型的频次需要的 key 值
    if key not in model.keys():
        return 0
    else:
        return model[key]


def P_character_word(character):
    """
    todo 此处暂时做一个简化，只要没有出现在 单词模型中的，返回0，否则返回 1
    :param character:  长度为1的字符串 散串
    :return:
    """
    if character not in one_word_model.keys():  # 在单个词模型当中，没有这个单字词，认为它不能单独成词
        return 0
    else:
        return 1


def K_1(i, segments):
    """
    计算 单字成词 错误系数
    :param i:
    :param segments:
    :return:
    """
    K1 = 0
    if len(segments[i]) == 1 and is_character_chinese(segments[i]) and P_character_word(
            segments[i]) == 0:  # 如果是散串、汉字、单字成词概率为 0
        K1 += 1.5
    return K1


def word_scope(i, len, n_gram):
    """
     返回 词的返回 [begin,end]
     :param i
     :param len
     :param n_gram 2， 3 元词
    :return:
    """
    begin = i - (n_gram - 1)
    if begin < 0:
        begin = 0
    end = i + (n_gram - 1)
    if end > len - 1:
        end = len - 1
    return begin, end


def K_2(i, segments):
    """
    计算 三元词 接续模型 错误系数
    注意： segments[i] 必须为 散串
    :param i:
    :param segments:
    :return:
    """
    K2 = 0
    if len(segments[i]) != 1:  # 如果不是散串，直接返回结果
        return K2
    begin, end = word_scope(i, len(segments), 3)
    if end - begin + 1 < 3:  # 如果begin 和 end 之间不够 三个词，不能使用 三元词接续模型，直接返回结果
        return K2
    for index in range(begin, end + 1 - 2):  # [begin,end-2]
        words = [segments[index], segments[index + 1], segments[index + 2]]
        if not is_seg_chinese("".join(words)):
            continue
        r = R(words, 0)
        if r == 0:
            K2 += 0.2
        elif r >= 1:
            K2 -= 1.0
    return K2


def K_3(i, segments):
    """
    二元词 接续模型 错误系数
    :param i:
    :param segments:
    :return:
    """
    K3 = 0
    if len(segments[i]) != 1:  # 如果不是散串，直接返回结果
        return K3
    begin, end = word_scope(i, len(segments), 2)
    if end - begin + 1 < 2:
        return K3
    for index in range(begin, end + 1 - 1):
        words = [segments[index], segments[index + 1]]
        if not is_seg_chinese("".join(words)):
            continue
        r = R(words, 0)
        if r == 0:
            K3 += 0.5
        elif 1 <= r < 2:
            K3 += 0.2
        else:
            K3 -= 1.0
    return K3


def character_scope(c_i, w_len, s_len, n_gram):
    """
    字的范围 [begin, end]
    :param c_i:
    :param w_len:
    :param s_len:
    :param n_gram:
    :return:
    """
    begin = c_i - (n_gram - 1)
    if begin < 0:
        begin = 0
    end = (c_i + w_len - 1) + (n_gram - 1)
    if end > s_len - 1:
        end = s_len - 1
    return begin, end


def K_4(i, c_i, segments, text):
    """
    三元字 模型
    :param i:
    :param c_i:
    :param segments:
    :param text:
    :return:
    """
    K4 = 0
    if len(segments[i]) != 1:
        return K4
    begin, end = character_scope(c_i, len(segments[i]), len(text), 3)
    if end - begin + 1 < 3:
        return K4
    for index in range(begin, end + 1 - 2):  # [begin, end-2]
        chars = [text[index], text[index + 1], text[index + 2]]
        if not is_seg_chinese("".join(chars)):  # 不处理包含 非汉字 的情况
            continue
        if contain_mood_word("".join(chars)):  # 不处理包含 语气词 的情况
            continue
        r = R(chars, 1)
        if r == 0:
            K4 += 0.2
        elif r >= 1:
            K4 -= 1.0
    return K4


def K_5(i, c_i, segments, text):
    """
    二元字模型
    :param i:
    :param c_i:
    :param segments:
    :param text:
    :return:
    """
    K5 = 0
    if len(segments[i]) != 1:
        return K5
    begin, end = character_scope(c_i, len(segments[i]), len(text), 2)
    if end - begin + 1 < 2:
        return K5
    for index in range(begin, end + 1 - 1):  # [begin, end-1]
        chars = [text[index], text[index + 1]]
        if not is_seg_chinese("".join(chars)):
            continue
        r = R(chars, 1)
        if r == 0:
            K5 += 0.8
        elif 1 <= r < 3:
            K5 += 0.5
        elif r >= 3:
            K5 -= 1.0
    return K5


def detect_error(segments, text):
    """
    查错
    :param text:
    :param segments
    :return: 每一个 seg 检查结果
    """
    position_res = {}
    c_i = 0
    for i in range(len(segments)):
        error_i = False  # 默认这个位置是没有错的
        K1, K2, K3, K4, K5 = K_1(i, segments), K_2(i, segments), K_3(i, segments), K_4(i, c_i, segments, text), K_5(i,
                                                                                                                    c_i,
                                                                                                                    segments,
                                                                                                                    text)
        c_i += len(segments[i])
        # K1 = 0
        K2 = 0
        K3 = 0
        # K4 = 0
        # K5 = 0
        K = K1 + K2 + K3 + K4 + K5
        if K >= 1.0:
            error_i = True
        position_res[i] = error_i
    return position_res
