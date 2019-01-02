def test1():
    # 1. 打开文件，得到文件句柄并赋值给一个变量
    f = open(
        'D:/BaiduNetdiskDownload/sgns.target.word-word.dynwin5.thr10.neg5.dim300.iter5/sgns.target.word-word.dynwin5'
        '.thr10.neg5.dim300.iter5', 'r', encoding='utf-8')  # 默认打开模式就为r

    f1 = open('D:/BaiduNetdiskDownload/sgns.target.word-word.dynwin5.thr10.neg5.dim300.iter5/test', 'w',
              encoding='utf-8')

    line = f.readline()
    print(line)

    dic = {}

    lines = f.readlines()
    print(len(lines))
    for l in lines:
        ss = l.split()
        if ss[0] not in dic.keys():
            dic[ss[0]] = 1
        else:
            lines.remove(l)
    print(len(lines))
    f1.writelines(lines)

    f1.close()

    f.close()


def test2():
    f1 = open('D:/BaiduNetdiskDownload/sgns.target.word-word.dynwin5.thr10.neg5.dim300.iter5/test', 'r',
              encoding='utf-8')

    f2 = open('D:/BaiduNetdiskDownload/sgns.target.word-word.dynwin5.thr10.neg5.dim300.iter5/test2', 'w',
              encoding='utf-8')

    lines = f1.readlines()
    f2.writelines(lines[0:20000])
    f2.close()

    f1.close()


if __name__ == '__main__':
    test2()
