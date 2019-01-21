# coding:utf-8
import json
import re

from jpype import *


def test():
    startJVM(getDefaultJVMPath(), "-Djava.class.path=D:\hanlp\hanlp-1.7.0.jar;D:\hanlp", "-Xms1g",
             "-Xmx1g")  # 启动JVM，Linux需替换分号;为冒号:
    HanLP = JClass('com.hankcs.hanlp.HanLP')

    # 命名实体识别与词性标注
    NLPTokenizer = JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')

    viterbi_segment = JPackage("com.hankcs.hanlp.seg.Viterbi").ViterbiSegment()

    with open('D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/material/material5_pure_else.json', 'r',
              encoding='utf-8') as f:
        data = json.load(f)
        f.close()

    name_entity = []
    name_entity_else = []
    for item in data:
        sentences = re.split('[.!?。]', item['text'])
        is_useless = True
        hits = []  # 敏感词准备
        for item_risk in item['risks']:
            hits += item_risk['hit']
        temp_sentences = []  # 敏感词所在的句子准备
        for sen in sentences:
            for hit in hits:
                if hit in sen:
                    temp_sentences.append(sen)
        for temp_sen in temp_sentences:  # 对于每一个句子
            for hit in hits:
                if not useless(hit, temp_sen, viterbi_segment):  # 只要有一个 敏感词 不是无用的，就不过滤
                    is_useless = False
        if is_useless:
            name_entity.append(item)
        else:
            name_entity_else.append(item)
    with open(
            'D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/material/material5_pure_else_name_entity.json',
            'w',
            encoding='utf-8') as f:
        json.dump(name_entity, f, ensure_ascii=False)
        f.close()
    with open(
            'D:/20181101_审核内容情感分析/export_feedback_audit_2018-11-06/material/material5_pure_else_name_entity_else.json',
            'w',
            encoding='utf-8') as f:
        json.dump(name_entity_else, f, ensure_ascii=False)
        f.close()
    shutdownJVM()


# 判断 sen 中的 敏感词 是不是 无用的
def useless(hit, sen, viterbi_segment):
    if hit in sen:  # 敏感词 为人名
        sp = viterbi_segment.seg(sen)
        for sp_i in sp:
            if hit in sp_i.word and len(hit) < len(sp_i.word) and re.match(r'^nr(\w?)$',
                                                                           str(sp_i.nature)):  # 如果是敏感词是人名的一部分
                return True
    return False


if __name__ == '__main__':
    test()
