# two_characters_model()

# print(cut_word_hanlp("他就是把酿造出来的酒着呢"))

# print(connect_mongodb())
# baidu_corpus()
# write_baidu_url_path()

# two_characters_model_gentle()

a = -1
for i in range(130000, 7890000):
    if a == -1:
        a = i
    if i % 394500 == 0:
        print("python baidu_corpus.py", a, i, 'log_baidu_' + str(a) + "_" + str(i))
        a = -1
i=7890000
print("python baidu_corpus.py", a, i, 'log_baidu_' + str(a) + "_" + str(i))