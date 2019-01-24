import _thread
import re
import time

from error_word.detect_error_util import is_character_chinese


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


def get_pos_model(model_name):
    """
    获取词性模型
    :param model_name:
    :return:
    """
    with open(model_name, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    model = {}
    for line in lines:
        segs = line.split("\t")
        model[segs[0]] = int(segs[1])
    return model


def get_one_pos_model():
    """
    一元词性获取
    :return:
    """
    return get_pos_model("one_pos_model")


def get_two_pos_model():
    """
    二元词性获取
    :return:
    """
    return get_pos_model("two_pos_model")


def get_three_pos_model():
    """
    三元词性获取
    :return:
    """
    return get_pos_model("three_pos_model")


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


def two_characters_model():
    """
    使用 人民日报 和 wiki 两个语料
    二元字模型
    :return:
    """
    lines = get_wiki_corpus()
    lines += get_2014_corpus()
    two_character_count = {}
    for line in lines:
        line = line.rstrip()  # 去掉句子末尾的\n
        length = len(line)
        for i in range(length - 1):
            key = line[i] + ' ' + line[i + 1]
            if key not in two_character_count.keys():
                two_character_count[key] = 0
            two_character_count[key] += 1
    write_model("two_characters_model", two_character_count)


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


def parse_line(line):
    """
    解析 已经经过 分词和词性标注 的熟语料
    比如：人民日报 2014 标注语料
    人民网/nz 1月1日/t 讯/ng 据/p 《/w [纽约/nsf 时报/n]/nz 》/w 报道/v ，/w 美国/nsf 华尔街/nsf 股市/n 在/p 2013年/t 的/ude1 最后/f 一天/mq 继续/v 上涨/vn ，/w 和/cc [全球/n 股市/n]/nz 一样/uyy ，/w 都/d 以/p [最高/a 纪录/n]/nz 或/c 接近/v [最高/a 纪录/n]/nz 结束/v 本/rz 年/qt 的/ude1 交易/vn 。
    重点将其中
        [纽约/nsf 时报/n]/nz -> 纽约/nsf 时报/n\t纽约时报/nz
    返回 [人民网/nz,1月1日/t,讯/ng,据/p,《/w,纽约/nsf 时报/n\t纽约时报/nz,》/w,...]

    算法描述如下：
    每读一个 char
    如果是 [ 装入 bracket_stack
    如果是 ]， bracket_stack 中已有 [] 配对，弹出该对，
    如果是空格，如果 bracket_stack 为空
        弹出 char_stack 中 chars
            解析 chars
    如果不是[除了空格且bracket_stack为空的情况]
        装入 char_stack
    :param line:
    :return:
    """
    segs = []
    bracket_stack = []
    char_stack = []
    for (char, index) in zip(line, range(len(line))):
        if '[' == char and line[index:index + 3] != '[/w':  # 如果 [ 且不是 [/w 这种情况，添加入 bracket_stack 中
            bracket_stack.append(char)
        elif ']' == char and line[index: index + 3] != ']/w' and \
                len(bracket_stack) > 0 and bracket_stack[-1] == '[':  # 如果是 ] 且不是 ]/w 这种情况，查看是否与 bracket 中 [ 配对
            bracket_stack.pop()  # 弹出配对
            put = True
            temp_t = ['\t' if len(char_stack) > 0 else ""]
            for t in char_stack:
                if t == '/':
                    put = False
                elif t == " ":
                    put = True
                if put and t != " ":  # 不添加空格
                    temp_t.append(t)
            char_stack += temp_t
        elif (" " == char and len(bracket_stack) == 0) or \
                (index == len(line) - 1):  # 如果是空格 并且 如果 bracket_stack 为空 或者 已经跑到了文末，弹出 char_stack 中 chars
            if index == len(line) - 1:
                char_stack.append(char)
            seg = "".join(char_stack)  # [纽约/nsf 时报/n] 获取内容
            char_stack.clear()  # 清除 char_stack
            if len(seg) == 0:  # 如果出现连续空格的情况，使得 char_stack 中没有内容了，直接跳过
                continue
            segs.append(seg)
        else:  # 否则装入 char_stack 中
            char_stack.append(char)
    return segs


def increase_key_count(key, key_count={}):
    """
    key_count 是统计 key 数量的 {key, count}
    :param key:
    :param key_count:
    :return:
    """
    if key not in key_count.keys():
        key_count[key] = 1
    else:
        key_count[key] += 1


def get_2014_corpus():
    """
    获取2014人民日报 经过分区和标注过的熟语料
    :return:
    """
    with open("2014_corpus.txt", 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    return lines


def get_wiki_corpus():
    """
    获取 wiki 中文 百科 生语料
    :return:
    """
    with open("wiki/zh_wiki_00", 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    with open("wiki/zh_wiki_01", 'r', encoding='utf-8') as fp:
        lines2 = fp.readlines()
    return lines + lines2


def write_model(model_name, key_count):
    """
    写入模型
    :param model_name:
    :param key_count:
    :return:
    """
    temp_lines = []
    for key in key_count.keys():
        temp_line = key + "\t" + str(key_count[key]) + '\n'
        temp_lines.append(temp_line)
    write_text(model_name, temp_lines)


def write_text(file_name, lines):
    """
    写入文本信息
    :param file_name:
    :param lines:
    :return:
    """
    f = open(file_name, "w", encoding="utf-8")
    f.writelines(lines)
    f.close()


def one_pos_model():
    """
    一元词性 模型
    :param lines:
    :return:
    """
    lines = get_2014_corpus()
    pos_count = {}
    for line in lines:
        line = line.rstrip()
        segs = parse_line(line)
        for seg in segs:  # 纽约/nsf 时报/n\t纽约时报/nz
            temp = re.split("[ \t]", seg)
            for t in temp:
                if "/" not in t:
                    continue
                key = get_pos(t)
                increase_key_count(key, pos_count)
    write_model("one_pos_model", pos_count)


def get_pos(word_pos):
    """
    获取 词/词性 中的词性
    :param word_pos:
    :return:
    """
    pos = None
    for (t_ch, t_i) in zip(word_pos, range(len(word_pos))):
        if t_ch == '/' and t_i != 0 and t_i != len(word_pos) - 1:  # 找到中间位置的 /
            pos = word_pos[t_i + 1:]  # 词性
    return pos


def get_pos_list(word_pos_list):
    """
    给定 [word/pos, word/pos]， 返回 [pos, pos]
    过滤掉 其中不合格式的项，比如 [word/pos, word, word/pos]
    :param word_pos_list:
    :return:
    """
    pos = []
    for word_pos in word_pos_list:
        p = get_pos(word_pos)
        if p is None:
            continue
        pos.append(p)
    return pos


def count_word_pos(words, n_gram):
    """
    统计 [word/pos, word/pos] 中的词性
    :param words:
    :param n_gram:
    :return:
    """
    pos = get_pos_list(words)
    start = 0
    end = len(pos) - n_gram
    key_count = {}
    for index in range(start, end + 1):  # [start, end]
        key = " ".join(pos[index:index + n_gram])
        increase_key_count(key, key_count)
    return key_count


def get_seg_splits(seg):
    """
    获取 seg 按照 空格\t 分隔之后的结果 [[],[]]
    先按照 \t 分隔 纽约/nsf 时报/n\t纽约时报/nz -> [纽约/nsf 时报/n, 纽约时报/nz]
    再按照 空格 分隔 [纽约/nsf 时报/n, 纽约时报/nz] -> [[纽约/nsf, 时报/n], [纽约时报/nz]]
    :return:
    """
    temp_s = []
    temp = seg.split("\t")
    for t in temp:
        t_s = t.split()
        temp_s.append(t_s)
    return temp_s


def add_key_count(sum_key_count, key_count):
    """
    {"中":1, "和":2} {"中":3}
    ->{"中":4, "和":2}
    :param sum_key_count:
    :param key_count:
    :return:
    """
    for key in key_count:
        if key in sum_key_count.keys():
            sum_key_count[key] += key_count[key]
        else:
            sum_key_count[key] = key_count[key]


def count_seg_pos(segs, index, n_gram):
    """
    统计 segs[index] ... seg[index + n_gram  -1] 的 n_gram 元词性
    :param segs: seg 集合 其中segs[index]格式：
        纽约/nsf 时报/n\t纽约时报/nz 或者 纽约/nsf
    :param index:
    :param n_gram:
    :return:
    """
    res = [[]]
    for index in range(index, index + n_gram):
        ts = get_seg_splits(segs[index])  # [[纽约/nsf,时报/n], [纽约时报/nz]]
        for t in ts:
            for r in res:
                r += t
    sum_key_count = {}
    for r in res:
        temp = count_word_pos(r, n_gram)
        add_key_count(sum_key_count, temp)
    return sum_key_count


def two_pos_model():
    """
    二元词性模型
    :return:
    """
    pos_model("two_pos_model", 2)


def pos_model(model_name, n_gram):
    """
    n_gram 词性模型
    :param model_name: 存储的模型文件名称
    :param n_gram:
    :return:
    """
    lines = get_2014_corpus()
    sum_pos_count = {}
    for line in lines:
        segs = parse_line(line.rstrip())
        for index in range(len(segs) - n_gram + 1):
            pos_count = count_seg_pos(segs, index, n_gram)
            add_key_count(sum_pos_count, pos_count)
    write_model(model_name, sum_pos_count)


def three_pos_model():
    """
    三元词性模型
    :return:
    """
    pos_model("three_pos_model", 3)


import threading
import time


class myThread(threading.Thread):
    def __init__(self, url, path):
        threading.Thread.__init__(self)
        self.url = url
        self.path = path

    def run(self):
        print("hi")
        store_url_text(self.url, self.path)


def write_baidu_url_path():
    """
    百度百科 url， path 路径生成
    :return:
    """
    mycol = connect_mongodb()
    key_value = {}
    for x in mycol.find():
        url = "http://qt-ml.oss-cn-hangzhou.aliyuncs.com/" + x['oss_path']
        path = 'baidu/' + str(x['_id'])
        key_value[url] = path
    write_model("baidu_url_path", key_value)


def baidu_corpus():
    """
    百度百科 语料库 生成
    :return:
    """
    key_value = get_baidu_url_path("baidu_url_path")
    count = 0
    for key in key_value.keys():
        count += 1
        print(count, " is processing!!!")
        try:
            store_url_text(key, key_value[key].rstrip())
        except IOError:
            print(count, " is not stored")
    print("finished !!!")


def get_baidu_url_path(name):
    """
    从文件中获取 url - path 对
    :param name:
    :return:
    """
    with open(name, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    model = {}
    for line in lines:
        segs = line.split("\t")
        model[segs[0]] = segs[1]
    return model


def get_url_path_from_mongodb():
    """
    从 mongodb 中获取 url, path 对
    :return:
    """
    mycol = connect_mongodb()
    key_value = {}
    count = 0
    for x in mycol.find():
        url = "http://qt-ml.oss-cn-hangzhou.aliyuncs.com/" + x['oss_path']
        path = 'baidu/' + str(x['_id'])
        key_value[url] = path
        count += 1
        print(count)
    return key_value


def store_with_threads(key_value):
    """
    多线程存储
    :param key_value:
    :return:
    """
    count = 0
    threads = []
    for key in key_value.keys():
        t = threading.Thread(target=store_url_text, args=(key, key_value[key]))
        t.start()
        threads.append(t)
        count += 1
        print(count)
        if len(threads) % 500 == 0:
            for th in threads:
                th.join()
    for th in threads:
        th.join()


import urllib.request
from bs4 import BeautifulSoup


def store_url_text(url, filename):
    text = get_url_text(url)
    write_text(filename, text)


def get_url_text(url):
    """
    获取 url 中的文本内容
    :param url:
    :return:
    """
    return get_html_text(get_url_html(url))


def get_html_text(html):
    """
    获取 html 信息中的文本
    :param html:
    :return:
    """
    soup = BeautifulSoup(html, features="html.parser")
    return soup.find("div", "main-content").get_text()


def get_url_html(url):
    """
    通过 url 获取 文本 内容
    :param url:
    :return:
    """
    with urllib.request.urlopen(url) as response:
        html = response.read()
    return html


import pymongo


def connect_mongodb():
    """
    连接 mongodb，获取 百度百科 表 中记录
    :return:  百度百科表 集合
    """
    myclient = pymongo.MongoClient('mongodb://47.97.189.163:27017/')
    db = myclient['ml_entity']
    table = db['entities']
    return table
