import os
import time
import datetime
from gensim.models import Word2Vec
import gensim
import json
import shutil

INF = 10000000000

output_file = 'train_output_workers10'

# 取每个文件的每个案例中的四个字段进行训练
def train():

    data_path = '/mnt/disk/segmented_data'
    # data_path = '/data/law_ai/test_worker'
    # 保存最好的模型
    # best_model_loss = INF

    # 上一次训练损失
    last_loss = INF

    # 模型名字
    model_name = 'win5_min_count5_workers10_sg0.model'
    # model_name = 'test.model'

    # 加载模型
    with open(output_file, mode='a', encoding='utf-8') as train_output:
        log = '加载模型 {} {}\n'.format(datetime.date.today(), time.strftime("%H:%M:%S"))
        train_output.write(log)

    model = Word2Vec.load(model_name)

    with open(output_file, mode='a', encoding='utf-8') as train_output:
        log = '加载完成 {} {}\n'.format(datetime.date.today(), time.strftime("%H:%M:%S"))
        train_output.write(log)

    for epoch in range(100):

        # 已经处理的文件数量
        file_cnt = 0

        # 已经处理的案例数量
        # case_cnt = 0

        total_loss = 0

        for root, dir_list, file_list in os.walk(data_path):

            # 遍历所有文件
            for file_name in file_list:

                # 遍历文件数量
                file_cnt += 1

                # 文件路径
                file_path = os.path.join(root, file_name)

                # 读取一个文件
                with open(file_path) as datafile:
                    lines = datafile.readlines()

                    sentences = []

                    # 遍历所有案例
                    for line in lines:

                        # 加载一个案例
                        case = json.loads(line)

                        # 跳过index那一行
                        if case.keys() == 1:
                            continue

                        # case_cnt += 1

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
                                epochs=5,
                                compute_loss=True,
                                total_examples=model.corpus_count)

                    # 单个文件loss
                    file_loss = model.get_latest_training_loss()

                    if file_cnt == 30000:
                        with open(output_file, mode='a', encoding='utf-8') as train_output:
                            log = '保存模型 {} {}\n'.format(datetime.date.today(), time.strftime("%H:%M:%S"))
                            train_output.write(log)

                        model.save(model_name)

                        with open(output_file, mode='a', encoding='utf-8') as train_output:
                            log = '保存完成 {} {}\n'.format(datetime.date.today(), time.strftime("%H:%M:%S"))
                            train_output.write(log)

                    # 所有文件loss
                    total_loss = total_loss + file_loss
                    
                    if file_cnt % 100 == 0:
                        # 输出每个文件的loss等
                        with open(output_file, mode='a', encoding='utf-8') as train_output:
                            log = "epoch: {}, file_cnt: {}, file loss: {}, total loss: {}, time: {} {}\n" \
                                .format(epoch, file_cnt, file_loss, total_loss, datetime.date.today(),
                                        time.strftime("%H:%M:%S"))
                            train_output.write(log)

        # 训练完所有文件也保存一次
        with open(output_file, mode='a', encoding='utf-8') as train_output:
            log = "保存模型 {} {}\n" .format(datetime.date.today(), time.strftime("%H:%M:%S"))
            train_output.write(log)
        model.save(model_name)
        with open(output_file, mode='a', encoding='utf-8') as train_output:
            log = "保存完成 {} {}\n" .format(datetime.date.today(), time.strftime("%H:%M:%S"))
            train_output.write(log)
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
        with open('/data/law_ai/epoch_loss.txt', mode='a') as epoch_loss:
            epoch_loss_str = "epoch: {}, average_loss: {}, time: {} {}" \
                .format(epoch, average_loss, datetime.date.today(), time.strftime("%H:%M:%S"))
            epoch_loss.write(epoch_loss_str + '\n')

        # 训练停止条件
        if abs(last_loss - average_loss) < 50:
            return

        # 更新last_loss
        last_loss = average_loss


if __name__ == '__main__':

    with open(output_file, mode='w', encoding='utf-8') as train_output:
        log = "开始训练 {} {}\n".format(datetime.date.today(), time.strftime("%H:%M:%S"))
        train_output.write(log)

    train()

    with open(output_file, mode='a', encoding='utf-8') as train_output:
        log = "训练结束 {} {}\n".format(datetime.date.today(), time.strftime("%H:%M:%S"))
        train_output.write(log)
