import os
import time
import datetime
from gensim.models import Word2Vec
import gensim
import json
import shutil
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')


# 取每个文件的每个案例中的四个字段进行训练
def get_voc():
    # 模型名字
    print('加载模型：', datetime.date.today(), time.strftime("%H:%M:%S"))
    model_name = 'win5_min_count5_workers10_sg0.model'
    model = Word2Vec.load(model_name)
    print('加载完成：', datetime.date.today(), time.strftime("%H:%M:%S"))

    vocs = model.wv.vocab

    with open('low_fre_word', mode='a', encoding='utf-8') as f:
        cnt = 0
        cnt_word = ''
        for voc in vocs:
            if model.wv.vocab[voc].count <= 10:
                cnt_word += str((voc, model.wv.vocab[voc].count)) + '\n'
                cnt += 1
                if cnt == 10000:
                    f.write(cnt_word)
                    cnt_word = ''
                    cnt = 0
        if cnt > 0:
            f.write(cnt_word)


if __name__ == '__main__':
    get_voc()
