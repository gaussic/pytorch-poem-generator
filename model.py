#!/usr/bin/python
# -*- coding: utf-8 -*-

import torch.nn as nn
from torch.autograd import Variable


class RNNLM(nn.Module):
    """基于RNN的语言模型，包含一个encoder，一个rnn模块，一个decoder。"""

    def __init__(self, config):
        super(RNNLM, self).__init__()

        v_size = config.vocab_size
        em_dim = config.embedding_dim
        dropout = config.dropout

        self.rnn_type = rnn_type = config.rnn_type
        self.hi_dim = hi_dim = config.hidden_dim
        self.n_layers = n_layers = config.num_layers

        self.drop = nn.Dropout(dropout)
        self.encoder = nn.Embedding(v_size, em_dim)

        # rnn: RNN / LSTM / GRU
        self.rnn = getattr(nn, rnn_type)(em_dim, hi_dim, n_layers, dropout=dropout)
        self.decoder = nn.Linear(hi_dim, v_size)

        # tie_weights将encoder和decoder的参数绑定为同一参数。
        if config.tie_weights:
            if hi_dim != em_dim:  # 这两个维度必须相同
                raise ValueError('When using the tied flag, hi_dim must be equal to em_dim')
            self.decoder.weight = self.encoder.weight

        self.init_weights()  # 初始化权重

    def forward(self, inputs, hidden):
        seq_len = len(inputs)
        emb = self.drop(self.encoder(inputs).view(seq_len, 1, -1))
        output, hidden = self.rnn(emb, hidden)
        output = self.decoder(output.view(seq_len, -1))
        return output, hidden  # 复原

    def init_weights(self):
        """权重初始化，如果tie_weights，则encoder和decoder权重是相同的"""
        init_range = 0.1
        self.encoder.weight.data.uniform_(-init_range, init_range)
        self.decoder.weight.data.uniform_(-init_range, init_range)
        self.decoder.bias.data.fill_(0)

    def init_hidden(self):
        """初始化隐藏层"""
        weight = next(self.parameters()).data
        if self.rnn_type == 'LSTM':  # lstm：(h0, c0)
            return (Variable(weight.new(self.n_layers, 1, self.hi_dim).zero_()),
                    Variable(weight.new(self.n_layers, 1, self.hi_dim).zero_()))
        else:  # gru 和 rnn：h0
            return Variable(weight.new(self.n_layers, 1, self.hi_dim).zero_())
