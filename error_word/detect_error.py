"""
初始化模型
"""

from error_word.detect_error_model import get_one_word_model, get_two_words_model, get_three_words_model, \
    get_one_character_model, get_two_characters_model, get_three_characters_model, get_two_pos_model, get_one_pos_model, \
    get_three_pos_model

# 词模型
from error_word.detect_error_util import is_character_chinese, is_seg_chinese, contain_mood_word, \
    contain_preposition_word, contain_auxiliary_verb_word, contain_locality_word, contain_vshi_word

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


def error_character_word(i, segments):
    """
    计算 单字成词 错误问题
    如果分词后，某个 字 落单，但是 单字不能成词，则表明有问题
    :param i:
    :param segments:
    :return:
    """
    error = 0
    if len(segments[i]) == 1 and is_character_chinese(segments[i]) and P_character_word(
            segments[i]) == 0:  # 如果是散串、汉字、单字成词概率为 0
        error = 1
    return error


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
    :param n_gram:
    :return:
    """
    count = [0 for _ in range(n_gram)]
    begin, end = i - (n_gram - 1), i + (n_gram - 1)
    for index in range(begin, end - n_gram + 2):  # [begin, end-n_gram+1] 或者 [begin, end-n_gram+2)
        if index < 0 or index + n_gram - 1 > len(segments) - 1:  # 超出范围，无法统计
            count[index - begin] = -1
        else:
            words = [segments[i] for i in range(index, index + n_gram)]
            position = index - begin
            if contain_vshi_word(words):
                count[position] = -1
            elif contain_mood_word(words):
                count[position] = -1
            elif is_seg_chinese(words):
                count[position] = R(words, 0)
            else:
                count[position] = -1
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
            K6 += 0.1
        else:
            K6 -= 0.5
    return K6


def two_pos_model_frequency(i, segments_pos):
    """
    二元词性模型 频次统计
    :param i:
    :param segments_pos:
    :return:
    """
    return pos_model_frequency(i, segments_pos, 2)


def three_pos_model_frequency(i, segments_pos):
    """
    三元词性模型 频次统计
    :param i:
    :param segments_pos:
    :return:
    """
    return pos_model_frequency(i, segments_pos, 3)


def contain_pos(pos):
    """
    该 词性 列表中的所有词性是否都在 one_pos_model词性模型 中存在
    :param pos:
    :return:
    """
    contain_p = True
    for p in pos:
        if p not in one_pos_model.keys():
            contain_p = False
            break
    return contain_p


def pos_model_frequency(i, segments_pos, n_gram):
    """
    n 元词性模型 频次统计
    :param i:
    :param segments_pos:
    :param n_gram:
    :return:
    """
    count = [0 for _ in range(n_gram)]
    begin, end = i - (n_gram - 1), i + (n_gram - 1)
    for j in range(begin, end - n_gram + 2):  # [begin, end-ngram+2)
        if j < 0 or j + n_gram - 1 > len(segments_pos) - 1:  # 如果出现超出范围的情况，该位置设为 -1
            count[j - begin] = -1
        else:
            pos = [segments_pos[z] for z in range(j, j + n_gram)]
            if contain_pos(pos):  # 如果该串的词性在现有词性模型中存在，则进行统计
                count[j - begin] = R(pos, 2)
            else:
                count[j - begin] = -1  # 否则没法统计，设为 -1
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
    针对散串
    :param i:
    :param c_i:
    :param segments:
    :param text:
    :param n_gram:
    :return:
    """
    count = [0 for _ in range(n_gram)]
    if len(segments[i]) > 1:  # 如果 不是 散串，不统计
        return [-1 for _ in range(n_gram)]
    begin, end = c_i - (n_gram - 1), c_i + len(segments[i]) - 1 + n_gram - 1
    for index in range(begin, end - (n_gram - 1) + 1):  # [begin, end-n_gram+1]
        count_i = index - begin
        if index < 0 or index + n_gram - 1 > len(text) - 1:
            count[count_i] = -1
        else:
            chars = [text[z] for z in range(index, index + n_gram)]
            # if contain_mood_word(chars):  # 如果包含语气词，不进行字频统计
            #     count[count_i] = -1
            # elif contain_preposition_word(chars):  # 包含介词，不进行字频统计
            #     count[count_i] = -1
            # elif contain_auxiliary_verb_word(chars):  # 包含 助动词，不进行字频统计
            #     count[count_i] = -1
            # elif contain_locality_word(chars):  # 包含方位词，不进行词频统计
            #     count[count_i] = -1
            # el
            if is_seg_chinese(chars):  # 只有是汉字的时候，才进行字频次统计
                count[count_i] = R(chars, 1)
            else:  # 含有非汉字，没法统计
                count[count_i] = -1
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
        if K >= 1.6:
            error_i = True
        position_res[i] = error_i
    return position_res


def get_frequency(i, c_i, segments, text):
    """
    二元字、三元字、二元词、三元词 的 频次
    :param i:
    :param c_i:
    :param segments:
    :param text:
    :return:
    """
    two_characters_frequency = two_characters_model_frequency(i, c_i, segments, text)
    three_characters_frequency = three_characters_model_frequency(i, c_i, segments, text)
    two_words_frequency = two_words_model_frequency(i, segments)
    three_words_frequency = three_words_model_frequency(i, segments)
    return [two_characters_frequency, three_characters_frequency, two_words_frequency, three_words_frequency]


def get_flat_frequency(i, c_i, segments, text):
    """
    获取 二元字、三元字、二元词、三元词 的 频次
    数据 扁平化，降到一个维度
    :param i:
    :param c_i:
    :param segments:
    :param text:
    :return:
    """
    res = []
    frequency = get_frequency(i, c_i, segments, text)
    for freq in frequency:
        res += freq
    return res


def multiply_array(a1, a2):
    """
    [a,b,c]
    [x,y,z]
    -> [a*x,b*y,c*z]
    :param a1:
    :param a2:
    :return:
    """
    res = []
    for i in range(len(a1)):
        res.append(a1[i] * a2[i])
    return res


def detect_error2(segments, segments_pos, text):
    """
    查错，第二种办法
    :param segments:
    :param segments_pos:
    :param text:
    :return:
    """
    position_res = {}
    c_i = 0
    for i in range(len(segments)):
        error_i = 0  # 默认这个位置是没有错的
        if error_character_word(i, segments):  # 单字成词概率为 0，判定为错
            error_i += 1
        if 0 in two_pos_model_frequency(i, segments_pos):  # 如果统计二元词性 频次 中有 0 的情况，判定为错，判断二元词性接续问题，严格看待
            error_i += 2
        two_characters_frequency = two_characters_model_frequency(i, c_i, segments, text)
        if 0 in two_characters_frequency:  # 添加 二元字 模型，统计二元字模型 中频次有 0 的情况，如果有，判定为错
            # if two_characters_frequency[0] == 0 and i > 0 and len(segments[i - 1]) > 1:  # 字 左边匹配为0，字左边的词 长度> 1
            #     two_characters_frequency[0] = -1  # 不用
            # if two_characters_frequency[1] == 0 and i < len(segments) - 1 and len(segments[i + 1]) > 1:  # 字左边的词 长度> 1
            #     two_characters_frequency[1] = -1  # 不用统计
            if 0 in two_characters_frequency:
                error_i += 4
        position_res[i] = error_i
        c_i += len(segments[i])  # 记录字的位置

    return position_res


def detect_error3(text):
    """
    查错3
    :param text:
    :return:
    """
    chars = list(text)
    length = len(chars)
    if length < 2:
        return {0: False}
    res = {}
    for i in range(length):
        error_i = False
        if i == 0:  # 文首
            if R(chars[0:2], 1) == 0 and is_seg_chinese(chars[0:2]):  # 如果是中文 且 频次为0
                error_i = True
        elif i == length - 1:  # 文尾
            if R(chars[-2:], 1) == 0 and is_seg_chinese(chars[-2:]):  # 如果是中文 且 频次为 0
                error_i = True
        else:  # 文中
            chars1 = chars[i - 1:i + 1]  # 前面的二元字
            chars2 = chars[i:i + 2]  # 后面的二元字
            error_i = judge_2_chars(chars1) or judge_2_chars(chars2)  # 两个 二元字 只要有一个有问题 就认为 有问题
        res[i] = error_i
    return res


def judge_2_chars(chars):
    """
    判断 二元字 是否是错误的
    :param chars:
    :param error_i:
    :return:
    """
    error_i = False
    # if is_seg_chinese(chars) and not contain_mood_word(chars) and \
    #         not contain_preposition_word(chars):  # 如果是中文、不是语气词、不是介词
    if is_seg_chinese(chars) and not contain_mood_word(chars) and not contain_preposition_word(chars) and not contain_auxiliary_verb_word(chars):
        if R(chars, 1) == 0:
            error_i = True
    return error_i


def test_detect_error():
    f = open('test/文本.txt', 'r', encoding='utf-8')
    lines = f.readlines()
    f.close()

    text = "".join(lines)

    segments = list(text)
    position_character_res = detect_error3(text)
    for i in range(len(segments)):
        if position_character_res[i]:
            segments[i] = segments[i] + "（" + str(position_character_res[i]) + "）"

    text = "".join(segments)
    f = open('test/文本-括号中是机器修改的.txt', 'w', encoding='utf-8')
    f.writelines(text)
    f.close()


if __name__ == '__main__':
    test_detect_error()
