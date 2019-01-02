# coding:utf-8

import json
import re

from jpype import *
from jpype._jclass import _javaNew


def find_root_word(sentence, hanlp):
    res = hanlp.parseDependency(sentence)
    # 找出核心词
    for w in res.word:
        if w.HEAD.ID == 0:
            return w
    return -1


def is_center_word_verb(sentence, hanlp):
    if len(sentence) > 50:
        return True
    if len(sentence) <= 10:
        return True
    w = find_root_word(sentence, hanlp)
    if w != -1 and re.match(r'^[vVadicn](\w?)$', w.CPOSTAG):
        return True
    return False


def test2():
    startJVM(getDefaultJVMPath(), "-Djava.class.path=D:\hanlp\hanlp-1.7.0.jar;D:\hanlp", "-Xms1g",
             "-Xmx1g")  # 启动JVM，Linux需替换分号;为冒号:
    HanLP = JClass('com.hankcs.hanlp.HanLP')
    print(HanLP.parseDependency('又试图用炸药炸开石门失败后沮丧至极'))
    print(is_center_word_verb('又试图用炸药炸开石门失败后沮丧至极', HanLP))
    shutdownJVM()


def test3():
    startJVM(getDefaultJVMPath(), "-Djava.class.path=D:\hanlp\hanlp-1.7.0.jar;D:\hanlp", "-Xms1g",
             "-Xmx1g")  # 启动JVM，Linux需替换分号;为冒号:
    HanLP = JClass('com.hankcs.hanlp.dependency.nnparser.NeuralNetworkDependencyParser')
    print(HanLP.compute('又试图用炸药炸开石门失败后沮丧至极'))
    # print(is_center_word_verb('又试图用炸药炸开石门失败后沮丧至极', HanLP))
    shutdownJVM()

def test():
    startJVM(getDefaultJVMPath(), "-Djava.class.path=D:\hanlp\hanlp-1.7.0.jar;D:\hanlp", "-Xms1g",
             "-Xmx1g")  # 启动JVM，Linux需替换分号;为冒号:
    HanLP = JClass('com.hankcs.hanlp.HanLP')
    with open(
            'D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/material/material5_pure_else_name_entity_else.json',
            'r',
            encoding='utf-8') as f:
        data = json.load(f)
        f.close()
    syntactic = []
    syntactic_else = []
    for item in data:
        sentences = re.split('[.!?。]', item['text'])
        temp_sentences = []
        hits = item['risks'][0]['hit']
        for sen in sentences:
            for hit in hits:
                if hit in sen:
                    temp_sentences.append(sen)
        is_verb = False
        for temp_sen in temp_sentences:
            if is_center_word_verb(temp_sen, HanLP):  # 如果中心词是动词或者形容词或者句子过长，都认为是正常
                is_verb = True
        if not is_verb:
            syntactic.append(item)
        else:
            syntactic_else.append(item)
    with open(
            'D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/material'
            '/material5_pure_else_name_entity_else_syntactic.json',
            'w',
            encoding='utf-8') as f:
        json.dump(syntactic, f, ensure_ascii=False)
        f.close()
    with open(
            'D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/material'
            '/material5_pure_else_name_entity_else_syntactic_else.json',
            'w',
            encoding='utf-8') as f:
        json.dump(syntactic_else, f, ensure_ascii=False)
        f.close()
    shutdownJVM()


if __name__ == '__main__':
    test()
