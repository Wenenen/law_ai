import os
import time
import datetime
from gensim.models import Word2Vec
import gensim
import json
import shutil

INF = 10000000000

train_output_file = 'train_output_file.txt'

data_path = '/mnt/disk/segmented_data'

# 取每个文件的每个案例中的四个字段进行训练
def train():

    # 保存最好的模型
    # best_model_loss = INF

    # 上一次训练损失
    last_loss = INF

    # 模型名字
    model_name = 'win5_min_count5_workers28_sg0.model'

    # 加载模型日志
    with open(train_output_file, mode='a', encoding='utf-8') as f:
        log = '加载模型 {} {}\n'.format(datetime.date.today(), time.strftime("%H:%M:%S"))
        f.write(log)

    # 加载模型
    model = Word2Vec.load(model_name)

    # 开始训练日志
    with open(train_output_file, mode='a', encoding='utf-8') as f:
        log = '开始训练 {} {}\n'.format(datetime.date.today(), time.strftime("%H:%M:%S"))
        f.write(log)

    for epoch in range(100):

        # 已经处理的文件数量
        file_cnt = 0

        # 已经处理的案例数量
        case_cnt = 0

        # 单epoch的总loss
        total_loss = 0

        for root, dir_list, file_list in os.walk(data_path):

            # 遍历所有文件
            for file_name in file_list:

                # 遍历文件数量
                file_cnt += 1

                # 文件路径
                file_path = os.path.join(root, file_name)

                # 读取文件训练模型
                with open(file_path) as data:
                    lines = data.readlines()

                    sentences = []

                    # 遍历所有案例
                    for line in lines:

                        # 加载一个案例
                        case = json.loads(line)

                        # 跳过index那一行
                        if case.keys() == 1:
                            continue

                        case_cnt += 1

                        if case.get('Content') is not None:
                            tmp = case.get('Content').split(' ')
                            sentences.append(tmp)

                        if case.get('JudgeResult') is not None:
                            tmp = case.get('JudgeResult').split(' ')
                            sentences.append(tmp)

                        if case.get('Dispute') is not None:
                            tmp = case.get('Dispute').split(' ')
                            sentences.append(tmp)

                        if case.get('CourtViewpoint') is not None:
                            tmp = case.get('CourtViewpoint').split(' ')
                            sentences.append(tmp)

                    # 继续训练模型
                    model.train(sentences=sentences,
                                epochs=10,
                                compute_loss=True,
                                total_examples=model.corpus_count)

                    # 单个文件loss
                    file_loss = model.get_latest_training_loss()

                    # 所有文件loss
                    total_loss = total_loss + file_loss

                    # 保存模型,每训练完30000个文件，保存一次模型
                    if file_cnt == 30000:

                        # 保存模型日志
                        with open(train_output_file, mode='a', encoding='utf-8') as f:
                            log = '保存模型中 {} {}\n'.format(datetime.date.today(), time.strftime("%H:%M:%S"))
                            f.write(log)

                        # 保存模型
                        model.save(model_name)

                        # 保存模型日志
                        with open(train_output_file, mode='a', encoding='utf-8') as f:
                            log = '保存完成 {} {}\n'.format(datetime.date.today(), time.strftime("%H:%M:%S"))
                            f.write(log)

                    # 每个文件的loss日志
                    if file_cnt % 100 == 0:
                        with open(train_output_file, mode='a', encoding='utf-8') as f:
                            log = "epoch: {}, file_cnt: {}, file loss: {}, total loss: {}, time: {} {}\n" \
                                .format(epoch, file_cnt, file_loss, total_loss, datetime.date.today(),
                                        time.strftime("%H:%M:%S"))
                            f.write(log)

        # 保存模型日志
        with open(train_output_file, mode='a', encoding='utf-8') as f:
            log = '保存模型中 {} {}\n'.format(datetime.date.today(), time.strftime("%H:%M:%S"))
            f.write(log)

        # 保存模型
        model.save(model_name)

        # 保存模型日志
        with open(train_output_file, mode='a', encoding='utf-8') as f:
            log = '保存完成 {} {}\n'.format(datetime.date.today(), time.strftime("%H:%M:%S"))
            f.write(log)

        # 平均loss
        average_loss = total_loss / file_cnt

        # # 记录最好模型
        # if average_loss < best_model_loss:
        #
        #     # 更新模型loss
        #     best_model_loss = average_loss
        #
        #     # 模型名字
        #     training_model_name = '{}'.format(epoch) + model_name
        #
        #     # 当前路径
        #     current_dir = os.getcwd()
        #
        #     # 训练模型路径
        #     model_path = os.path.join(current_dir, model_name)
        #
        #     # 最好模型路径
        #     best_model_path = os.path.join(current_dir, training_model_name)
        #
        #     # 复制一份最好模型
        #     shutil.copy(model_path, best_model_path)
        #
        #     # 写日志
        #     best_str = "best_model_name: {}, average_loss: {}, time: {} {}"\
        #         .format(training_model_name, best_model_loss, datetime.date.today(), time.strftime("%H:%M:%S"))
        #     print(best_str)
        #     with open('/data/law_ai/best_model.txt', 'a') as best_model:
        #         best_model.write(best_str + '\n')
        #         best_model.close()

        # 过程中每轮的日志
        with open(train_output_file, mode='a', encoding='utf-8') as f:
            epoch_loss_str = "epoch: {}, average_loss: {}, time: {} {}\n" \
                .format(epoch, average_loss, datetime.date.today(), time.strftime("%H:%M:%S"))
            f.write(epoch_loss_str)

        # 训练停止条件
        if abs(last_loss - average_loss) < 100:
            return

        # 更新last_loss
        last_loss = average_loss


if __name__ == '__main__':

    # 开始训练模型日志
    with open(train_output_file, mode='w', encoding='utf-8') as f:
        log = '开始训练 {} {}\n'.format(datetime.date.today(), time.strftime("%H:%M:%S"))
        f.write(log)

    train()

    # 结束训练模型日志
    with open(train_output_file, mode='a', encoding='utf-8') as f:
        log = '结束训练 {} {}\n'.format(datetime.date.today(), time.strftime("%H:%M:%S"))
        f.write(log)