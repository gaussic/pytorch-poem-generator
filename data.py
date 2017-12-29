#!/usr/bin/python
# -*- coding: utf-8 -*-

import os





def open_file(filename, mode='r'):
    return open(filename, mode=mode, encoding='utf-8', errors='ignore')


class Corpus(object):
    """
    文本预处理，获取词汇表，并将字符串文本转换为数字序列。
    """

    def __init__(self, train_dir, vocab_dir):
        assert os.path.exists(train_dir), 'File %s does not exist.' % train_dir

        if not os.path.exists(vocab_dir):
            words = list(set(list(open_file(train_dir).read().replace('\n', ''))))
            open_file(vocab_dir, 'w').write('\n'.join(sorted(words)) + '\n')

        words = open_file(vocab_dir).read().strip().split('\n')
        word_to_id = dict(zip(words, range(len(words))))

        data = []
        with open_file(train_dir) as f:
            for line in f:
                poem = [word_to_id[x] for x in line.strip() if x in word_to_id]
                data.append(poem)

        self.words = words
        self.word_to_id = word_to_id
        self.data = data

    def __repr__(self):
        return "Corpus length: %d, Vocabulary size: %d" % (len(self.data), len(self.words))