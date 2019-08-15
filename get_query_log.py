import os


def replace_str(str_example):
    return str(str_example).replace(' ', '').replace('\n', '')


def get_log(flag):
    # 加载字典
    query_dir = 'log'
    files = os.listdir(query_dir)
    query_dic = {}
    for filename in files:
        file_path = os.path.join(query_dir, filename)
        with open(file_path, mode='r', encoding='utf-8') as f:
            lines = f.readlines()
            title = lines[0]
            title = replace_str(title)
            query_dic[title] = filename.replace('.txt', '')

    res = []
    query = ''
    output_path = ''
    if flag == 0:
        query = 'good_bad_query/bad_query'
        output_path = 'bad_log_name'
    else:
        query = 'good_bad_query/good_query'
        output_path = 'good_log_name'

    with open(query, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = replace_str(line)
            if query_dic.get(line) is not None:
                res.append((query_dic[line], line.replace(' ', '')))
    with open(output_path, mode='a', encoding='utf-8') as f:
        for re in res:
            tmp = ''
            for r in re:
                tmp += r + ' '
            f.write(tmp + '\n')


if __name__ == '__main__':
    get_log(0)