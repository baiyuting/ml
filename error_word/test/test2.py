import jieba
from error_word.detect_error_util import cut_word_hanlp

sen = "好再重复一遍,三个微信公众号,一个是四品带刀故事,一个是前泵,而第三个是疯狂奖学金.谢谢大家欢迎关注.嗯,嗯,嗯"
print(cut_word_hanlp(sen))
