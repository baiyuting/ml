# -*- coding: UTF-8 -*-
import urllib
from urllib.parse import urlencode

import requests
import time
import json
import hashlib
import base64

import jieba

import re

import jieba.posseg as pseg

URL = "http://ltpapi.xfyun.cn/v1/sdp"
APPID = "5c1234b7"
API_KEY = "f39a239a8d5ab76fe7da9cd655599a0f"


def getHeader():
    curTime = str(int(time.time()))
    paramBase64 = 'ew0KICAgICJ0eXBlIjogImRlcGVuZGVudCINCn0='
    m2 = hashlib.md5()
    m2.update((API_KEY + curTime + paramBase64).encode(encoding='UTF-8'))
    checkSum = m2.hexdigest()
    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    return header


def get_header(app_id, api_key):
    curTime = str(int(time.time()))
    paramBase64 = 'ew0KICAgICJ0eXBlIjogImRlcGVuZGVudCINCn0='
    m2 = hashlib.md5()
    m2.update((api_key + curTime + paramBase64).encode(encoding='UTF-8'))
    checkSum = m2.hexdigest()
    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': app_id,
        'X-CheckSum': checkSum,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    return header


# 语义依存树 借口调用
def semantic_dependency_tree(text):
    body = urlencode({'text': text})
    r = requests.post(URL, headers=getHeader(), data=body)
    result = json.loads(r.content)
    return result


# 科大讯飞分词
def word_split(text):
    body = urlencode({'text': text})
    r = requests.post("http://ltpapi.xfyun.cn/v1/cws", headers=get_header(), data=body)
    result = json.loads(r.content)
    return result


# 是否需要过滤敏感词 使用 语义依存树
def filter_sensitive_word_with_semantic_dependency_tree(sen_word, text):
    # 语义依存树 接口调用
    result = semantic_dependency_tree(text)
    # jieba 分词 和 词性 分析
    cuts = list(pseg.cut(text))
    # 判断敏感词为 名词 且 分词完全正确，再进行 下一步
    cut_n = False
    for c in cuts:
        if sen_word == c.word and c.flag == 'n':
            cut_n = True
    if cut_n and result['code'] == '0' and len(result['data']['sdp']) > 0:
        temp = result['data']['sdp']
        for i in range(len(temp)):
            if temp[i]['parent'] == -1 and i < len(cuts) and cuts[i].word == sen_word:  # 分词中，语义分析为根节点，但是是名词
                return True
    return False


# 整段文本 与 敏感词 匹配，找到 敏感词 所在的 所有句子，只有所有的 句子都可以 过滤的时候，才可以过滤，只要有一个句子显示 该敏感词不能 过滤，我们就不会过滤
def filter_sensitive_word_with_semantic_dependency_tree_paragraph(sen_word, paragraph):
    sentences = re.split('[,.!?。]', paragraph)  # 按照 , 分成短文本
    for sen in sentences:
        if sen_word in sen and not filter_sensitive_word_with_semantic_dependency_tree(sen_word, sen):  # 敏感词 所在 的所有句子
            return False
    return True


def main():
    with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/material/material1_pure_else.json', 'r',
              encoding='utf-8') as f:
        data = json.load(f)
        f.close()

    dependency = []
    dependency_else = []

    for item in data:
        hits = item['risks'][0]['hit']
        hit_filter = True  # 是否过滤掉 该 item 下面 所有 敏感词
        for hit in hits:
            if not filter_sensitive_word_with_semantic_dependency_tree_paragraph(hit, item['text']):
                hit_filter = False
                break
        if hit_filter:
            dependency.append(item)
        else:
            dependency_else.append(item)

    with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/material/material1_pure_else_dependency.json', 'w',
              encoding='utf-8') as f:
        json.dump(dependency, f, ensure_ascii=False)
        f.close()
    with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/material/material1_pure_else_dependency_else.json',
              'w',
              encoding='utf-8') as f:
        json.dump(dependency_else, f, ensure_ascii=False)
        f.close()
    return


def test():
    ss = '计划突袭驻扎在幽州的下属兼证的朝廷的奋武将军公孙瓒.结果,由于902兵马大道出动.在他手下的官员就有人出去.给这个公孙瓒去咸宁了.在刘瑜的军事行动保密工作可谓是差到家了.然后再进行交战之后,' \
         '由于有出于维护自己体面和官升得考虑声称自己要干掉的目标,只有公孙在一个人.并且还禁止手下兵马纵火工程破坏邻居.这些看起来会增加声望和操作,在实际战场上不仅无法实现,而且还会严重束缚军事的首要,结果,' \
         '就是流于大军围攻公孙瓒困守继承的几千人,却久攻不下.最后,公孙瓒出动敢死队数百人乘风火攻.由于的10万大军竟然就这样土崩瓦解了.这流于战败后呢,' \
         '又不善于收拢部队北逃居庸县去求耳熟.这次换到公孙瓒优势兵力攻城了.结果,这公孙瓒比流于那个利索多了,人家三天就拿下了,具有限.由于全家为陀螺,随后,他在次年被公孙瓒炸弹所有的政治价值之后,' \
         '就被公司在内杀了.在公元193年这一场关系到刘瑜身家性命和事业成败的幽州大决战中刘瑜的兵力啊,又是之巨大.但是战术指挥之拙劣,把握战机支持论足以证明他的军事能力非常低下.当然,' \
         '这场失败也有一部分原因是他的手枪战术小能手兼职幽洲骑兵天王的公孙瓒,他的个人能力也比着刘瑜要强太多了.由于的这种缺乏军事能力和知识结构性的这种缺陷,跟之前这个大锤所讨论过的刘表是一模一样的 '
    sen_word = '炸弹'
    # if filter_sensitive_word_with_semantic_dependency_tree(sen_word, ss):
    #     print(True)
    # else:
    #     print(False)
    sentence = '由于全家为陀螺,随后,他在次年被公孙瓒炸弹所有的政治价值之后,就被公司在内杀了'
    print(word_split(sentence))


if __name__ == '__main__':
    main()
