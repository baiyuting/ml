"""
初始化模型
"""

from error_word.detect_error_model import get_one_word_model, get_two_words_model, get_three_words_model, \
    get_one_character_model, get_two_characters_model, get_three_characters_model, get_two_pos_model, get_one_pos_model, \
    get_three_pos_model

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

# 词性模型
one_pos_model = get_one_pos_model()
two_pos_model = get_two_pos_model()
three_pos_model = get_three_pos_model()
pos_model = [one_pos_model, two_pos_model, three_pos_model]

# 字词模型
word_character_model = [words_model, characters_model, pos_model]


def R(segments, word_or_character_or_pos):
    """
    计算 连续字词 的 共现频次
    :param segments:
    :param word_or_character: word 0| character 1 | pos 2
    :return:
    """
    model = word_character_model[word_or_character_or_pos][len(segments) - 1]  # 获取对应的字词模型
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


def two_words_model_frequency(i, segments):
    """
    二元词 接续模型 频次统计 [f1,f2]
    :param i:
    :param segments:
    :return:
    """
    return word_model_frequency(i, segments, 2)


def three_words_model_frequency(i, segments):
    """
    三元词 接续模型 频次统计 [f1,f2,f3]
    :param i:
    :param segments:
    :return:
    """
    return word_model_frequency(i, segments, 3)


def word_model_frequency(i, segments, n_gram):
    """
    通用 单词接续模型 频次 统计
    :param i:
    :param segments:
    :return:
    """
    count = [0 for _ in range(n_gram)]
    begin, end = word_scope(i, len(segments), n_gram)
    for index in range(begin, end - n_gram + 2):  # [begin, end-n_gram+1] 或者 [begin, end-n_gram+2)
        words = [segments[i] for i in range(index, index + n_gram)]
        count[index] = R(words, 0)
    return count


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


def K_6(i, segments, segments_pos):
    """
    二元词性模型
    :param i:
    :param segments:
    :param segments_pos:
    :return:
    """
    K6 = 0
    if len(segments[i]) != 1:  # 如果不是散串，直接返回结果
        return K6
    begin, end = word_scope(i, len(segments_pos), 2)
    if end - begin + 1 < 2:
        return K6
    for index in range(begin, end + 1 - 1):
        pos = [segments_pos[index], segments_pos[index + 1]]
        r = R(pos, 2)
        if r == 0:  # 只要有错，认为有问题
            K6 += 1
        else:
            K6 -= 1
    return K6


def two_pos_model_frequency(i, segments_pos):
    """
    二元词性模型 频次统计
    :param i:
    :param segments:
    :param segments_pos:
    :return:
    """
    return pos_model_frequency(i, segments_pos, 2)


def pos_model_frequency(i, segments_pos, n_gram):
    """
    n 元词性模型 频次统计
    :param i:
    :param segments_pos:
    :param n_gram:
    :return:
    """
    count = [0 for _ in range(n_gram)]
    begin, end = word_scope(i, len(segments_pos), n_gram)
    if end - begin < (n_gram - 1):
        return count
    for index in range(begin, end - n_gram + 2):  # [begin, end-ngram+2)
        pos = [segments_pos[i] for i in range(begin, begin + n_gram)]
        count[index] = R(pos, 2)
    return count


def two_characters_model_frequency(i, c_i, segments, text):
    """
    二元字模型 频次 统计 [f1,f2]
    :param i:
    :param c_i:
    :param segments:
    :param text:
    :return: [x,x]
    """
    return character_model_frequency(i, c_i, segments, text, 2)


def three_characters_model_frequency(i, c_i, segments, text):
    """
    三元字模型 频次 统计 [f1,f2,f3]
    :param i:
    :param c_i:
    :param segments:
    :param text:
    :return:
    """
    return character_model_frequency(i, c_i, segments, text, 3)


def character_model_frequency(i, c_i, segments, text, n_gram):
    """
    通用的 字模型 频次统计
    :param i:
    :param c_i:
    :param segments:
    :param text:
    :param n_gram:
    :return:
    """
    count = [0 for _ in range(n_gram)]
    begin, end = character_scope(c_i, len(segments[i]), len(text), n_gram)
    for index in range(begin, end - (n_gram - 1) + 1):  # [begin, end-n_gram+1]
        chars = [text[i] for i in range(index, index + n_gram)]
        count[index] = R(chars, 1)
    return count


def detect_error(segments, segments_pos, text):
    """
    查错
    :param text:
    :param segments
    :param segments_pos
    :return: 每一个 seg 检查结果
    """
    position_res = {}
    c_i = 0
    for i in range(len(segments)):
        error_i = False  # 默认这个位置是没有错的
        K1, K2, K3, K4, K5, K6 = K_1(i, segments), \
                                 K_2(i, segments), K_3(i, segments), \
                                 K_4(i, c_i, segments, text), K_5(i, c_i, segments, text), \
                                 K_6(i, segments, segments_pos)

        c_i += len(segments[i])
        # K1 = 0
        # K2 = 0
        # K3 = 0
        # K4 = 0
        # K5 = 0
        K = K1 + K2 + K3 + K4 + K5 + K6
        if K >= 1.0:
            error_i = True
        position_res[i] = error_i
    return position_res
