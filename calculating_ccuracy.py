import os
import json
import numpy as np
import math

data_dir = 'C:\\Users\\Administrator\\Desktop\\labeled'


# def cal_mAP():
#     files = os.listdir(data_dir)
#     file_cnt = 0
#     AP = 0
#     for filename in files:
#         if filename.find('label') >= 0:
#             file_cnt += 1
#             file_path = os.path.join(data_dir, filename)
#             with open(file_path, mode='r', encoding='utf-8') as f:
#                 print(file_path)
#                 data = json.load(f)
#                 print(data)
#                 correct = 0
#                 res = []
#                 for doc in data['1']['documents']:
#                     if int(doc) > 10:
#                         break
#                     if data['1']['documents'][doc]['Label'] == '正确':
#                         correct += 1
#                         print(correct, doc)
#                         res.append(correct/int(doc))
#                 res = np.array(res)
#                 if math.isnan(res.mean()) is False:
#                     AP += res.mean()
#     return AP/file_cnt


# 计算前n个中正确的个数
def cal_pn(n):
    files = os.listdir(data_dir)
    file_cnt = 0
    res = []
    for filename in files:
        if filename.find('label') >= 0:
            file_cnt += 1
            file_path = os.path.join(data_dir, filename)
            with open(file_path, mode='r', encoding='utf-8') as f:
                # print(file_path)
                data = json.load(f)
                correct_case = 0
                for doc in data['1']['documents']:
                    if int(doc) > n:
                        break
                    if data['1']['documents'][doc]['Label'] == '正确' or data['1']['documents'][doc]['Label'] == '相关':
                        correct_case += 1
                res.append(correct_case/n)
    res = np.array(res)
    return res.mean()


def cal_mrr():
    files = os.listdir(data_dir)
    res = []
    for filename in files:
        if filename.find('label') >= 0:
            file_path = os.path.join(data_dir, filename)
            with open(file_path, mode='r', encoding='utf-8') as f:
                # print(file_path)
                data = json.load(f)
                flag = True
                for doc in data['1']['documents']:
                    if data['1']['documents'][doc]['Label'] == '正确' or data['1']['documents'][doc]['Label'] == '相关':
                        flag = False
                        res.append(1/int(doc))
                        break
                if flag:
                    res.append(0)
    res = np.array(res)
    return res.mean()


def cal_class_pn(class_name, n):
    # 加载问题
    query_file = 'queryFloder\\' + class_name + '.txt'
    query_dic = {}
    with open(query_file, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.replace(' ', '')
            line = line.replace('\n', '')
            query_dic[line] = line

    files = os.listdir(data_dir)
    res = []
    for filename in files:
        if filename.find('label') >= 0:
            file_path = os.path.join(data_dir, filename)
            with open(file_path, mode='r', encoding='utf-8') as f:
                # print(file_path)
                data = json.load(f)
                query = data['1']['query']
                query = str(query)
                query = query.replace(' ', '')
                query = query.replace('\n', '')
                if query_dic.get(query) is not None:
                    correct_case = 0
                    for doc in data['1']['documents']:
                        if int(doc) > n:
                            break
                        if data['1']['documents'][doc]['Label'] == '正确' or data['1']['documents'][doc]['Label'] == '相关':
                            correct_case += 1
                    res.append(correct_case/n)
    res = np.array(res)
    return res.mean()


def cal_class_mrr(class_name):
    query_file = 'queryFloder\\' + class_name + '.txt'
    query_dic = {}
    with open(query_file, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.replace(' ', '')
            line = line.replace('\n', '')
            query_dic[line] = line

    files = os.listdir(data_dir)
    res = []
    for filename in files:
        if filename.find('label') >= 0:
            file_path = os.path.join(data_dir, filename)
            with open(file_path, mode='r', encoding='utf-8') as f:
                # print(file_path)
                data = json.load(f)
                query = data['1']['query']
                query = str(query)
                query = query.replace(' ', '')
                query = query.replace('\n', '')
                if query_dic.get(query) is not None:
                    flag = True
                    for doc in data['1']['documents']:
                        if data['1']['documents'][doc]['Label'] == '正确' or data['1']['documents'][doc]['Label'] == '相关':
                            flag = False
                            res.append(1 / int(doc))
                            break
                    if flag:
                        res.append(0)
    res = np.array(res)
    return res.mean()


def cal_class_evaluation(class_name):
    pn = []
    pn.append(cal_class_pn(class_name, 1))
    pn.append(cal_class_pn(class_name, 10))
    mrr = cal_class_mrr(class_name)
    print(class_name)
    print('pn:', pn)
    print('mrr:', mrr)
    print('\n')


if __name__ == '__main__':
    # mAP = cal_mAP()

    pn = []
    pn.append(cal_pn(1))
    pn.append(cal_pn(10))
    print('pn:', pn)

    mrr = cal_mrr()
    print('mrr:', mrr)


    cal_class_evaluation('房地产')
    cal_class_evaluation('婚姻家事')
    cal_class_evaluation('基础设施')
    cal_class_evaluation('劳动纠纷')
    cal_class_evaluation('诉讼')
    cal_class_evaluation('投资并购')
    cal_class_evaluation('债权债务')
    cal_class_evaluation('知识产权')






    # print('mAP', mAP)