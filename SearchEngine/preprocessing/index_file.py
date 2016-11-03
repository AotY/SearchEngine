#!/usr/bin/env python
# -*- coding: utf-8 -*-
# QingTao
import codecs
import os
from trace import pickle
dir_path = r'G:\556\Resource\small_answer'

#遍历文件， 建立索引
index = 0
# tokener_f = codecs.open(r'./../resource/index.txt', 'w', encoding='utf-8')
index_dict = {}

for root, dirs, files in os.walk(dir_path, topdown=True):
    if len(files) > 0:
        for name in files:
            file_path = os.path.join(root, name)
            # print(os.path.join(root, name))
            index_dict[index] = file_path
            index += 1

print index_dict[1]

pickle.dump(index_dict, open(r'./../resource/index_dict.pkl', 'w'))
index_dict = pickle.load(open(r'./../resource/index_dict.pkl', 'r'))
print index_dict[1]
# with open(index_dict[1]) as f:
#     for line in f:
#         print line
