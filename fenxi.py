import jieba
import os
import json
import sys
import time

def replace_str(str_example):
    return str(str_example).replace(' ', '').replace('\n', '')

data_dir = 'C:\\Users\\Administrator\\Desktop\\labeled'
entity_dir = 'C:\\Users\\Administrator\\PycharmProjects\\law_ai\\entity2id.txt'

if __name__ == '__main__':

    entity_dic = {}
    with open(entity_dir, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split('\t')
            entity_dic[line[0]] = line[0]


    data_path = 'cut_query/cut_bad_query.txt'
    with open(data_path, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
        cnt = 0
        querys = []
        query_cuts = []
        key_points = []
        for line in lines:
            if cnt % 2 == 0:
                querys.append(replace_str(line.replace('|', '')))
                tmp = replace_str(line).split('|')
                query_cuts.append(tmp)
            else:
                tmp = []
                words = line.split()
                for word in words:
                    tmp.append(word)
                key_points.append(tmp)
            cnt += 1

        query_to_keyword = {}
        query_to_keypoint = {}
        for query, query_cut, key_point in zip(querys, query_cuts, key_points):
            query_to_keyword[query] = query_cut
            query_to_keypoint[query] = key_point
            # print('查询：', query)
            # print('分词后：', query_cut)
            # print('关键点：', key_point)

    # 得到有log的bad query
    bad_query = {}
    data_path = 'bad_log_name'
    with open(data_path, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
            bad_query[line[1]] = line[1]

    files = os.listdir(data_dir)
    res = []
    query_cnt = 0
    for filename in files:
        # 找到标注文件
        if filename.find('label') >= 0:
            file_path = os.path.join(data_dir, filename)
            with open(file_path, mode='r', encoding='utf-8') as f:
                data = json.load(f)
                # 得到问题
                query = data['1']['query']
                query = str(query)
                query = replace_str(query)
                # 查看问题是否在bad query中

                if bad_query.get(query) is not None:
                    query_cnt += 1
                    # 根据query得到query的关键点和关键词
                    key_points = query_to_keypoint[query]
                    keywords = query_to_keyword[query]
                    print('【查询', query_cnt, '】', query)
                    print('【关键点】', key_points)
                    print('【关键词】', keywords)
                    for doc in data['1']['documents']:
                        # 循环所有的关键点和关键词
                        Content = data['1']['documents'][doc]['Content']
                        JudgeResult = data['1']['documents'][doc]['JudgeResult']
                        CourtViewPoint = data['1']['documents'][doc]['CourtViewPoint']
                        Title = data['1']['documents'][doc]['Title']
                        print('【案例标题】', Title)
                        print('============关键点==============')
                        for key_point in key_points:
                            if len(key_point) == 0:
                                continue
                            key_point_cnt = (len(Content) - len(Content.replace(key_point, ""))) // len(key_point)
                            key_point_cnt += (len(JudgeResult) - len(JudgeResult.replace(key_point, ""))) // len(key_point)
                            key_point_cnt += (len(CourtViewPoint) - len(CourtViewPoint.replace(key_point, ""))) // len(key_point)
                            key_point_cnt += (len(Title) - len(Title.replace(key_point, ""))) // len(key_point)
                            if entity_dic.get(key_point) is not None:
                                print('%s\t%s\t有' % (key_point_cnt, key_point))
                            else:
                                print('%s\t%s\t无' % (key_point_cnt, key_point))
                        print('============关键词==============')
                        for keyword in keywords:
                            if len(keyword) == 0:
                                continue
                            keyword_cnt = (len(Content) - len(Content.replace(keyword, ""))) // len(keyword)
                            keyword_cnt += (len(JudgeResult) - len(JudgeResult.replace(keyword, ""))) // len(keyword)
                            keyword_cnt += (len(CourtViewPoint) - len(CourtViewPoint.replace(keyword, ""))) // len(keyword)
                            keyword_cnt += (len(Title) - len(Title.replace(keyword, ""))) // len(keyword)
                            if entity_dic.get(keyword) is not None:
                                print('%s\t%s\t有' % (keyword_cnt, keyword))
                            else:
                                print('%s\t%s\t无' % (keyword_cnt, keyword))
