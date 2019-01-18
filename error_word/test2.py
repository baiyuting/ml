import jieba

from error_word.detect_error import detect_error
from error_word.detect_error_util import cut_word_hanlp

sen = "谢谢大家欢迎关注.嗯,嗯,嗯"
segments = cut_word_hanlp(sen)
print(detect_error(segments, sen))
print(segments)
