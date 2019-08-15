#coding=utf-8

import io
import time
from src.input.utils import text_to_vec, rank
from src.modules.search import search
from src.models.deep_matching import match
from pymemcache.client import base
import json
client = base.Client(('localhost', 11211))


def retrieval(query, cause_no, mode=False, cause=False):

    start = time.time()
    query = query.replace(' ', '')
    documents = search(query, mode='fazhi', cause=cause)
    if mode:
        end = time.time()
        print 'search'
        print end - start

    vec_dic_init = text_to_vec({'query': query, 'documents': documents}, client)
    vec_dic_know = text_to_vec({'query': query, 'documents': documents}, client, prefix='graph_')
    if mode:
        end = time.time()
        print 'to_vec'
        print end - start
    
    scores_init = match(client, vec_dic_init, phrase=False)
    scores_know = match(client, vec_dic_know, phrase=False)
    scores = []
    for idx in range(len(documents)):
        scores.append((scores_init[idx] + scores_know[idx], scores_init[idx], scores_know[idx]))

    if mode:
        end = time.time()
        print 'match'
        print end - start

    results = rank(scores, documents, top_num=30)
    if mode:
        end = time.time()
        print 'rank'
        print end - start

    if mode:
        with io.open('output/mode_full_%d.txt'%cause_no, 'w', encoding='utf-8') as f:
            f.write(query.decode('utf-8'))
            f.write(u'\n')
            for score, sentence in results:
                f.write(u'#' * 100)
                f.write(u'\n')
                f.write(u'%f\t%f\t%f'%(score[0], score[1], score[2]))
                f.write(u'\n')
                f.write(sentence)
                f.write(u'\n')
    return [ele[1] for ele in results]
'''------------------------------------------------------------------------------------------'''
import os
def txt2list(txtPath):
    files = os.listdir(txtPath)
    txtList = []
    for fileName in files:
        if(os.path.splitext(fileName)[1] == '.txt'):
            file = io.open(os.path.join(txtPath,fileName),'r',encoding='utf-8')
            txtList.append(file.readlines())
            file.close()
    for i in range(len(txtList)):
        txtList[i] = [item.replace("\n",".") for item in txtList[i]]
        content = u''
        for item in txtList[i]:
            content+=item
        txtList[i]=content
    return txtList

def que2list(dataPath):
    queList = []
    file = io.open(dataPath,mode='r',encoding='utf-8')
    lines = file.readlines()
    for line in lines:
        queList.append(line)
    file.close()
    return queList

if __name__ == '__main__':
    # query = '公司法定代表人能否担任其他企业的董事 ？'
    # results = retrieval(query, 0, mode=True, cause=False)
    # exit()
    # ls = [
    # '公司股东认缴注册资本到期未实缴的法律后果？',
    # '公司债权人可否申请公司股东的认缴注册资本加速到期？',
    # '公司实际经营范围与营业执照上的经营范围有较大差距的法律后果？',
    # '股东能否以未办理产权登记的房屋出资？',
    # '由于施工图尚未确定，建设单位按照已完成工程量向施工单位先行支付部分工程款，是否违反法律规定？',
    # '施工单位未经建设单位同意擅自更换项目负责人，是否需要承担违约责任？',
    # '承包人支付给发包人的质量保证金的性质是借款还是工程带资款？',
    # '在工程总承包合同中，承包人的工作范围包括设计、施工、采购等工作，相应费用通常也会被约定在一个固定总价中，那么此时工程总承包人是否可以及应该如何行使优先受偿权？',
    # '请问离婚了，男方不愿意给抚养费，已经有三个月了。我可以起诉吗',
    # '离婚一年了!但是离婚协议书的共同欠款未处理!共同债务共五万，各承担一半!但是没有日期，这个债务怎么去处理？',
    # '夫妻一方私自将房屋卖给第三人并办理了过户登记，第三人能否取得该房产？',
    # '一方婚前所有的房屋因城市更新回迁所得到的房产，属于夫妻共同财产吗？',
    # '公司克扣离职员工工资如何处理呢？夫妻一方私自将房屋卖给第三人并办理了过户登记，第三人能否取得该房产？',
    # '公司规定试用期内因员工个人原因离职的，不发放工资并要求签署协议，那么协议合法吗？',
    # '入职一年零两个月，工作上没有过失性过错，年假也一天没休过，突然被辞退，只提前两天通知我，之前签过劳动合同，但是没有公司法人签字和盖章，请问我能得到多少个月基本工资的赔偿？',
    # '未取得房地产企业开发资质证书即进行房地产开发的法律后果？',
    # '以房抵款合同是否有效？',
    # '搬迁补偿协议的搬迁人有权直接就被搬迁人之前签署的房屋租赁合同起诉吗？',
    # '权利人是否可以把回迁房屋登记至其他人名下？',
    # '你好，我想问一下，我们帮甲方公司出了展台设计方案，后甲方公司未经我方允许让其他公司把我们的设计方案做了简单修改后搭建，请问这种情况我应该怎么维权？',
    # '我们公司的场景图和机器，被人拍摄照片并发布，宣称是他们的场景和图片。这种行为是否侵权违法？',
    # '我们一个同行，盗用我们公司的网站排版，盗用图片，两个网站相似度在80%，而且是在一样的行业。想问下如何维权，如何留证据？',
    # '请问，视觉中国图片版权公司今日与我司联系，并被告知我司2011年企业微博上的图片侵权，需索赔1500元/张的版权，共计100多张；我想问一下这个时间有没有过诉讼期？其公司有没有权利随意定价自己的版权图片？'
    # ]
    # by yaguang
    # ls = txt2list("data/txtFloder")
    ls = ['网络借贷中，平台宣传的借款利息与实际利息不符，借款人应如何维权？',
          '注册的商标被他人用来做门头广告，如何维权？']

    # by jiabao
    # floder = 'data/queryFloder'
    # files = os.listdir(floder)
    # 问题个数
    query_cnt = 0
    # for file in files:
        # ls = que2list(os.path.join(floder,file))
        # all_results = []
    for i, query in enumerate(ls):
        if len(query) == 1 and query == '\n':
            continue
        if len(query) < 1:
            continue
        try:
            print(query)
        except UnicodeEncodeError:
            print query.encode('utf-8')
        # 找出一个查询的所有结果
        results = retrieval(query, i, mode=True, cause=False)
        # all_results.append((query, results))
        # 一个query的三十个答案
        results = (query, results)
        dic = {}
        # for idx, result in enumerate(all_results):
        # for result in results:
        dic[1] = {}
        #     # dic[idx+1]['query'] = result[0].decode('utf-8')
        dic[1]['query'] = results[0].decode('utf-8')
        tmp = {}
        # for j, doc in enumerate(result[1]):
        for j, doc in enumerate(results[1]):

            tmp[j+1] = {}
            ls = doc.split('|||')
            title = ls[0]
            Cause = ls[1]
            CourtViewPoint = ls[2]
            JudgeResult = ls[3]
            Content = ls[4]

            # tmp['Title'] = title
            # tmp['Cause'] = Cause
            # tmp['CourtViewPoint'] = CourtViewPoint
            # tmp['JudgeResult'] = JudgeResult
            # tmp['Content'] = Content

            tmp[j+1]['Title'] = title
            tmp[j+1]['Cause'] = Cause
            tmp[j+1]['CourtViewPoint'] = CourtViewPoint
            tmp[j+1]['JudgeResult'] = JudgeResult
            tmp[j+1]['Content'] = Content
        dic[1]['documents'] = tmp

        outputfloder = 'output/results'
        filename = str(query_cnt)
        filename += '.json'
        outputFile = os.path.join(outputfloder,filename)
        with io.open(outputFile, 'w', encoding='utf-8') as f:
            jsondata= json.dumps(dic, ensure_ascii=False,indent=4)
            f.write(jsondata)
        query_cnt += 1
        # for r in results:
        #     print r
