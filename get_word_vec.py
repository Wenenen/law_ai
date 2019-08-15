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

    with open('voc2vec_30', mode='a', encoding='utf-8') as f:
        cnt = 0
        voc2vec = ''
        for voc in vocs:
            if model.wv.vocab[voc].count >= 30:
                voc2vec += (str((voc, model.wv.get_vector(voc))) + '\n')
                cnt += 1
                if cnt == 10000:
                    f.write(voc2vec)
                    voc2vec = ''
                    cnt = 0
        if cnt > 0:
            f.write(voc2vec)

    # model.wv.get_vector(word=)


if __name__ == '__main__':
    get_voc()
