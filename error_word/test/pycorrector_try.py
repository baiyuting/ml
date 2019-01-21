import re

import pycorrector


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
    一般放在句末
    :return:
    """
    return "^[的了呢吧吗啊]$"


def is_mood_word(word):
    """
    是否是语气词
    :param word:
    :return:
    """
    return re.match(get_mood_words(), word) is not None


def is_character_end_of_string(i, char, str):
    """
    字符是否在字符串尾
    :param i:
    :param char:
    :param str:
    :return:
    """
    length = len(str)
    return char == str[length - 1] and i == length - 1


def is_character_start_of_string(i, char, str):
    """
    字符是否在字符串首
    :param i:
    :param char:
    :param str:
    :return:
    """
    return i == 0 and char == str[0]


def handle_mood_words(errors, sen):
    """
       处理语气词问题
       经过观察，在句段中：
           如果语气词出现在句末或者句中，pycorrector 容易将它检查为错误，需要去除掉
       :param errors: [['因该', 4, 6, 2], ['坐', 10, 11, 3]] [词、位置、错误类型]
       :param sen:
       :return:
       """
    res = []
    for error in errors:
        if is_mood_word(error[0]) and \
                (error[2] == len(sen) or
                 re.match("^[,\?\.]$", sen[error[2]]) is not None or
                 error[2] < len(sen)):  # 如果是情感词，并且情感词在句子末尾或者居中
            continue
        res.append(error)
    return res


def handle_exclamation_words(errors, sen):
    """
    处理感叹词问题
    经过观察，在句段中：
        如果感叹词出现在句首，pycorrector 容易将它检查为错误，需要去除掉
    :param errors: [['因该', 4, 6, 2], ['坐', 10, 11, 3]] [词、位置、错误类型]
    :param sen:
    :return:
    """
    res = []
    for error in errors:
        if is_exclamation_word(error[0]) and error[1] == 0:  # 如果是感叹词，并且感叹词在句首
            continue
        res.append(error)
    return res


def handle_punctuation(errors, sen):
    """
    处理标点问题
    经过观察，标点符号后面 使用 pycorrector 容易判定为错，过滤掉
    :param errors: [['因该', 4, 6, 2], ['坐', 10, 11, 3]] [词、位置、错误类型]
    :param sen:
    :return:
    """
    res = []
    for error in errors:
        if re.match("^[,\?\.]$", error[0]) is not None:  # 不判断 标点错误
            continue
        res.append(error)
    return res


def detect_sentence(text):
    """
    检查句子错误 该句子已经按照 .? 分割
    :param text:
    :return:
    """
    errors = pycorrector.detect(text)  # 使用 pycorrector 查错，返回 [词、位置、错误类型] [['因该', 4, 6, 2], ['坐', 10, 11, 3]]
    errors = handle_mood_words(errors, text)  # 处理语气词
    errors = handle_exclamation_words(errors, text)  # 处理感叹词
    errors = handle_punctuation(errors, text)  # 处理标点问题
    characters = list(text)  # 字符串转数组
    for idx_error in errors:
        end = idx_error[2]
        characters[end - 1] = characters[end - 1] + "（True）"
    return "".join(characters)


def test():
    """
    测试中
    :return:
    """
    f = open('文本.txt', "r", encoding="utf-8")
    lines = f.readlines()
    f.close()

    ts = []
    for line in lines:
        segs = re.split("[\.\?]", line)  # 句子级别的查错
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


if __name__ == '__main__':
    test()
