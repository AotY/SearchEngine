#!/usr/bin/env python
# -*- coding: utf-8 -*-
# QingTao

#每个文件夹取100篇文章
import codecs
import os
from shutil import copyfile

dir_path = r'G:\556\Resource\answer'
SYSTEM_SEPARATOR = '\\'

if dir_path is not None and os.path.isdir(dir_path):
    dir_name = dir_path.split(SYSTEM_SEPARATOR)[-1]
    small_dir = dir_path.replace(dir_name, 'small_' + dir_name)
    if not os.path.exists(small_dir):
        os.mkdir(small_dir)

print 'small_dir === ', small_dir

for root, dirs, files in os.walk(dir_path, topdown=True):
    if len(files) > 0:
        for name in files[:100]:
            file_path = os.path.join(root, name)
            copyfile(file_path, os.path.join(small_dir, name))
