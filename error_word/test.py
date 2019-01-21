from error_word.detect_error import detect_error,detect_error2
from error_word.detect_error_util import cut_word_hanlp, cut_pos_hanlp


def test():
    f = open('test/文本.txt', 'r', encoding='utf-8')
    lines = f.readlines()
    f.close()

    text = "".join(lines)
    segments, segments_pos = cut_word_hanlp(text)

    print(segments)
    position_res = detect_error(segments, segments_pos, text)
    print(position_res)

    for i in range(len(segments)):
        if position_res[i]:  # 有问题的情况下
            segments[i] = segments[i] + "（" + str(position_res[i]) + "）"

    text = "".join(segments)
    f = open('test/文本-括号中是机器修改的.txt', 'w', encoding='utf-8')
    f.writelines(text)
    f.close()


if __name__ == '__main__':
    test()
