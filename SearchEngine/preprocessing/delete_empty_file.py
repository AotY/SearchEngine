#!/usr/bin/env python
# -*- coding: utf-8 -*-
# QingTao

import codecs
import os
dir_path = r'G:\556\Resource\answer'

#遍历文件， 建立索引
index = 0

for root, dirs, files in os.walk(dir_path, topdown=True):
    if len(files) > 0:
        for name in files:
            file_path = os.path.join(root, name)
            f = codecs.open(file_path, 'rb', 'gbk', errors='ignore')
            content = f.read(1024)
            f.close()
            if content is None or content == '':
                #删除文件
                os.remove(file_path)
