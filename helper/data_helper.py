#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
该脚本帮助清洗来自chinese-poetry的唐诗json文件。

https://github.com/chinese-poetry/chinese-poetry

对justdark/pytorch-poetry-gen中的dataHandler.py进行修改，

https://github.com/justdark/pytorch-poetry-gen/blob/master/dataHandler.py

加入了繁体字转换为简体字的功能。
"""

import os
import re
import json


def sentence_parse(para):
    """数据清洗"""
    result = re.sub("（.*）", "", para)
    result = re.sub("「.*」", "", result)
    result = re.sub("〖.*〗", "", result)
    result = re.sub("{.*}", "", result)
    result = re.sub("《.*》", "", result)
    result = re.sub("［.*］", "", result)
    result = re.sub("[\].*\[]", "", result)
    result = re.sub("[0-9A-Za-z\-（/□○●「」Ｂ\ue829]", "", result)
    result = re.sub("[；！：？]", "。", result)
    result = re.sub("。。", "。", result)

    return result


def handle_json(filename):
    """处理一个json文件"""
    poetry_list = []
    data = json.loads(open(filename, 'r', encoding='utf-8').read())
    for poetry in data:
        try:
            para = sentence_parse(''.join(poetry['paragraphs']))
            if len(para) >= 10 and len(para) <= 100:  # 只取长度10～100的诗
                poetry_list.append(para)
        except:
            pass
    return poetry_list


def read_conver_words(filename):
    """读取繁简字体转换表"""
    tr_to_cn = {}
    with open('tr-han.txt', 'r', encoding='utf-8') as f:
        for line in f:
            key, value = line.strip().split()
            tr_to_cn[key] = value
    return tr_to_cn


def convert_tr_to_cn(sentence, tr_to_cn):
    """繁简转换"""
    han_s = ''
    for x in sentence:
        if x in tr_to_cn:
            x = tr_to_cn[x]
        han_s += x
    return han_s


def process_poem(data_dir, save_dir, prefix='poet.tang'):
    """处理所有唐诗"""
    data = []
    for filename in os.listdir(data_dir):
        if filename.startswith(prefix):
            data.extend(handle_json(os.path.join(data_dir, filename)))
    print('Total poems:', len(data))

    tr_to_cn = read_conver_words('tr-han.txt')
    with open(save_dir, 'w', encoding='utf-8') as f:
        for poem in data:
            poem = convert_tr_to_cn(poem, tr_to_cn)
            f.write(poem + '\n')


process_poem('../data/json', '../data/poem.tang.txt')
