import jieba
import os
import sys
import time

if __name__ == '__main__':
    with open('../good_bad_query/good_query', mode='r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            words = jieba.cut(line)
            words = "|".join(words)
            with open('cut_good_query', mode='a', encoding='utf-8') as outfile:
                outfile.write(words)


    # words = jieba.cut('绿本房买卖合同的效力？')
    # for word in words:
    #     print(word)