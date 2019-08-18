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


def replace_str(str_example):
    return str(str_example).replace(' ', '').replace('\n', '')


def cal_query_pn(n):
    # 加载字典
    query_dir = 'queryFloder'
    files = os.listdir(query_dir)
    query_dic = {}
    for filename in files:
        file_path = os.path.join(query_dir, filename)
        with open(file_path, mode='r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                line = replace_str(line)
                query_dic[line] = filename.replace('.txt', '')

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
                res.append(('%.6f' % (correct_case / n), query_dic[replace_str(str(data['1']['query']))], replace_str(str(data['1']['query']))))
    res.sort(reverse=True)
    with open('p' + str(n) + '_output', mode='a', encoding='utf-8') as f:
        for re in res:
            f.write(str(re) + '\n')


def cal_query_mrr():
    # 加载字典
    query_dir = 'queryFloder'
    files = os.listdir(query_dir)
    query_dic = {}
    for filename in files:
        file_path = os.path.join(query_dir, filename)
        with open(file_path, mode='r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                line = replace_str(line)
                query_dic[line] = filename.replace('.txt', '')

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
                        res.append(('%.6f' % (1 / int(doc)), query_dic[replace_str(str(data['1']['query']))], replace_str(str(data['1']['query']))))
                        break
                if flag:
                    res.append(('%.6f' % 0, query_dic[replace_str(str(data['1']['query']))], replace_str(str(data['1']['query']))))
    res.sort(reverse=True)
    with open('mrr_output', mode='a', encoding='utf-8') as f:
        for re in res:
            f.write(str(re) + '\n')

def get_bad_or_good_query(flag, n):
    # 加载字典
    query_dir = 'queryFloder'
    files = os.listdir(query_dir)
    query_dic = {}
    for filename in files:
        file_path = os.path.join(query_dir, filename)
        with open(file_path, mode='r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                line = replace_str(line)
                query_dic[line] = filename.replace('.txt', '')

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
                if flag == 0:       # bad query
                    if correct_case == 0:
                        res.append(replace_str(str(data['1']['query'])))
                elif flag == 1:     # good query
                    if correct_case == n:
                        res.append(replace_str(str(data['1']['query'])))
    if flag == 0:
        with open('bad_query', mode='a', encoding='utf-8') as f:
            for re in res:
                f.write(str(re) + '\n')
    elif flag == 1:
        with open('good_query', mode='a', encoding='utf-8') as f:
            for re in res:
                f.write(str(re) + '\n')

def cal_top_n_correct(class_name, n):
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
    correct_query = 0
    query_cnt = 0
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
                    query_cnt += 1
                    for doc in data['1']['documents']:
                        if int(doc) > n:
                            break
                        if data['1']['documents'][doc]['Label'] == '正确' or data['1']['documents'][doc][
                            'Label'] == '相关':
                            correct_query += 1
                            break
    res = correct_query/query_cnt
    return class_name, n, res


if __name__ == '__main__':
    # mAP = cal_mAP()

    # pn = []
    # pn.append(cal_pn(1))
    # pn.append(cal_pn(10))
    # print('pn:', pn)
    #
    # mrr = cal_mrr()
    # print('mrr:', mrr)
    #
    # cal_class_evaluation('房地产')
    # cal_class_evaluation('婚姻家事')
    # cal_class_evaluation('基础设施')
    # cal_class_evaluation('劳动纠纷')
    # cal_class_evaluation('诉讼')
    # cal_class_evaluation('投资并购')
    # cal_class_evaluation('债权债务')
    # cal_class_evaluation('知识产权')

    # 按问题直接排序
    # cal_query_pn(1)
    # cal_query_pn(10)
    # cal_query_mrr()
    # bad = 0
    # good = 1
    # get_bad_or_good_query(bad, 10)
    # get_bad_or_good_query(good, 10)
    querys = ['房地产', '婚姻家事', '基础设施', '劳动纠纷', '诉讼', '投资并购', '债权债务', '知识产权']
    topn = [1, 5, 10]
    for query in querys:
        for n in topn:
            class_name, top, score = cal_top_n_correct(query, n)
            print(class_name, top, '%.6f' % score)


    # print('mAP', mAP)