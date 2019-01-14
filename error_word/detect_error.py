import jieba


def P_character_word(character):
    """
    todo 待实现 一个字单独出现的概率
    :param character:  长度为1的字符串 散串
    :return:
    """
    pass


def K_1(i, segments):
    """
    计算 单字成词 错误系数
    :param i:
    :param segments:
    :return:
    """
    K1 = 0
    if len(segments[i]) == 1 and P_character_word(segments[i]) == 0:  # 如果是散串且 单字成词 概率为 0
        K1 += 1.5
    return K1


def R(segments):
    """
    todo 需要有熟语料
    计算 连续字词 的 共现频次
    :param segments:
    :return:
    """
    pass


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
        r = R([segments[index], segments[index + 1], segments[index + 2]])
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
        r = R([segments[index], segments[index + 1]])
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


def K_4(i, segments, text):
    """
    三元字 模型
    :param i:
    :param segments:
    :param text:
    :return:
    """
    K4 = 0
    if len(segments[i]) != 1:
        return K4
    begin, end = character_scope(text.index(segments[i]), len(segments[i]), len(text), 3)
    if end - begin + 1 < 3:
        return K4
    for index in range(begin, end + 1 - 2):  # [begin, end-2]
        r = R([text[index], text[index + 1], text[index + 2]])
        if r == 0:
            K4 += 0.2
        elif r >= 1:
            K4 -= 1.0
    return K4


def K_5(i, segments, text):
    """
    二元字模型
    :param i:
    :param segments:
    :param text:
    :return:
    """
    K5 = 0
    if len(segments[i]) != 1:
        return K5
    begin, end = character_scope(text.index(segments[i]), len(segments[i]), len(text), 2)
    if end - begin + 1 < 2:
        return K5
    for index in range(begin, end + 1 - 1):  # [begin, end-1]
        r = R([text[index], text[index + 1]])
        if r == 0:
            K5 += 0.8
        elif 1 <= r < 3:
            K5 += 0.5
        elif r >= 3:
            K5 -= 1.0
    return K5


def detect_error(text):
    position_res = {}
    segments = list(jieba.cut(text))  # 结巴分词
    for i in range(len(segments)):
        error_i = False  # 默认这个位置是没有错的
        K1, K2, K3, K4, K5 = K_1(i, segments), K_2(i, segments), K_3(i, segments), K_4(i, segments, text), K_5(i,
                                                                                                               segments,
                                                                                                               text)
        K = K1 + K2 + K3 + K4 + K5
        if K >= 1.5:
            error_i = True
        position_res[i] = error_i
    return position_res
