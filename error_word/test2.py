import re

from error_word.detect_error_model import one_pos_model, parse_line, two_pos_model, pos_model, three_pos_model


def test():
    line = "伙伴们/nz ，快/a 动起来/nz ！！！"
    segs = parse_line(line)
    print(segs)


# one_pos_model()


def test2():
    for i in range(1,-1):
        print(i)


if __name__ == '__main__':
    # pos_model("three_pos_model", 3)
    # three_pos_model()
    test2()
