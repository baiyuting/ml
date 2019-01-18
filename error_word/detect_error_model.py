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


def get_one_word_model():
    """
    一元词模型获取
    :return:
    """
    with open("one_word_model", 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    one_word_count = {}
    for line in lines:
        segs = line.split()
        one_word_count[segs[0]] = int(segs[1])
    return one_word_count


def get_two_words_model():
    """
    二元词模型获取
    :return:
    """
    with open("two_words_model", 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    model = {}
    for line in lines:
        segs = line.split("\t")
        model[segs[0]] = int(segs[1])
    return model


def get_three_words_model():
    """
    三元词模型获取
    :return:
    """
    with open("three_words_model", 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    model = {}
    for line in lines:
        segs = line.split("\t")
        model[segs[0]] = int(segs[1])
    return model


def get_one_character_model():
    """
    一元字模型获取
    :return:
    """
    with open("one_character_model", 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    model = {}
    for line in lines:
        segs = line.split()
        model[segs[0]] = int(segs[1])
    return model


def get_two_characters_model():
    """
    二元字模型获取
    :return:
    """
    with open("two_characters_model", 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    model = {}
    for line in lines:
        segs = line.split("\t")
        model[segs[0]] = int(segs[1])
    return model


def get_three_characters_model():
    """
    三元字模型获取
    :return:
    """
    with open("three_characters_model", 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    model = {}
    for line in lines:
        segs = line.split("\t")
        model[segs[0]] = int(segs[1])
    return model


def one_word_model(lines):
    """
    people2014_words.txt
    一元词模型
    :return:
    """
    word_count = {}
    for line in lines:
        words = line.split()
        for word in words:
            if word not in word_count.keys():
                word_count[word] = 0
            word_count[word] += 1
    temp_lines = []
    for word in word_count.keys():
        temp_line = word + " " + str(word_count[word]) + '\n'
        temp_lines.append(temp_line)
    f = open("one_word_model", "w", encoding="utf-8")
    f.writelines(temp_lines)
    f.close()


def two_words_model(lines):
    """
    people2014_words.txt
    二元词模型
    :return:
    """
    two_words_count = {}
    for line in lines:
        words = line.split()
        length = len(words)
        for i in range(length - 1):
            key = words[i] + ' ' + words[i + 1]
            if key not in two_words_count.keys():
                two_words_count[key] = 0
            two_words_count[key] += 1
    temp_lines = []
    for key in two_words_count.keys():
        temp_line = key + '\t' + str(two_words_count[key]) + '\n'
        temp_lines.append(temp_line)
    f = open('two_words_model', 'w', encoding='utf-8')
    f.writelines(temp_lines)
    f.close()


def three_words_model(lines):
    """
    people2014_words.txt
    三元词模型
    :return:
    """
    three_words_count = {}
    for line in lines:
        words = line.split()
        length = len(words)
        for i in range(length - 2):
            key = words[i] + ' ' + words[i + 1] + ' ' + words[i + 2]
            if key not in three_words_count.keys():
                three_words_count[key] = 0
            three_words_count[key] += 1
    temp_lines = []
    for key in three_words_count.keys():
        temp_line = key + '\t' + str(three_words_count[key]) + '\n'
        temp_lines.append(temp_line)
    f = open('three_words_model', 'w', encoding='utf-8')
    f.writelines(temp_lines)
    f.close()


def people_words_characters(lines):
    """
    people2014_words.txt -> people2014_characters.txt
    people2014_words.txt 2014年人民日报 分过词
    people2014_characters.txt 2014年人民日报 没有分过词
    :param lines:
    :return:
    """
    temp_lines = []
    for line in lines:
        line = line.replace(" ", "")
        temp_lines.append(line)
    f = open('people2014_characters.txt', 'w', encoding='utf-8')
    f.writelines(temp_lines)
    f.close()


def one_character_model(lines):
    """
    people2014_characters.txt
    一元字模型
    :return:
    """
    one_character_count = {}
    for line in lines:
        line = line.rstrip()  # 去掉句子末尾的\n
        for c in line:
            if c not in one_character_count.keys():
                one_character_count[c] = 0
            one_character_count[c] += 1
    temp_lines = []
    for key in one_character_count.keys():
        temp_line = key + " " + str(one_character_count[key]) + '\n'
        temp_lines.append(temp_line)
    f = open("one_character_model", "w", encoding="utf-8")
    f.writelines(temp_lines)
    f.close()


def two_characters_model(lines):
    """
    people2014_characters.txt
    二元字模型
    :return:
    """
    two_character_count = {}
    for line in lines:
        line = line.rstrip()  # 去掉句子末尾的\n
        length = len(line)
        for i in range(length - 1):
            key = line[i] + ' ' + line[i + 1]
            if key not in two_character_count.keys():
                two_character_count[key] = 0
            two_character_count[key] += 1
    temp_lines = []
    for key in two_character_count.keys():
        temp_line = key + "\t" + str(two_character_count[key]) + '\n'
        temp_lines.append(temp_line)
    f = open("two_characters_model", "w", encoding="utf-8")
    f.writelines(temp_lines)
    f.close()


def three_characters_model(lines):
    """
    people2014_characters.txt
    三元字模型
    :return:
    """
    three_character_count = {}
    for line in lines:
        line = line.rstrip()  # 去掉句子末尾的\n
        length = len(line)
        for i in range(length - 2):
            key = line[i] + ' ' + line[i + 1] + ' ' + line[i + 2]
            if key not in three_character_count.keys():
                three_character_count[key] = 0
            three_character_count[key] += 1
    temp_lines = []
    for key in three_character_count.keys():
        temp_line = key + "\t" + str(three_character_count[key]) + '\n'
        temp_lines.append(temp_line)
    f = open("three_characters_model", "w", encoding="utf-8")
    f.writelines(temp_lines)
    f.close()
