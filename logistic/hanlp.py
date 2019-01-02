# coding:utf-8
'''
Created on 2017-11-21

@author: 刘帅
'''

from jpype import *
from jpype._jclass import _javaNew

startJVM(getDefaultJVMPath(), "-Djava.class.path=D:\hanlp\hanlp-1.7.0.jar;D:\hanlp", "-Xms1g",
         "-Xmx1g")  # 启动JVM，Linux需替换分号;为冒号:

# 命名实体识别与词性标注
NLPTokenizer = JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')

# viterbi_segment = JClass('com.hankcs.hanlp.seg.Viterbi.ViterbiSegment')

viterbi_segment = JPackage("com.hankcs.hanlp.seg.Viterbi").ViterbiSegment()


java.lang.System.out.println("Hello World")

s = NLPTokenizer.segment('陈云学习了佛法')
print(s)  # nr

s = viterbi_segment.seg('他也利用这个瓦哈比派的意识形态吧')
print(s)



shutdownJVM()
