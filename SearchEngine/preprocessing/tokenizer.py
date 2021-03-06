#!/usr/bin/env python
# -*-coding:utf-8-*-
# QingTao
from __future__ import division
import codecs
import os

import jieba
import jieba.posseg as pseg
import re

from pybloom import BloomFilter

# from Preprocess.Preprocessing.DB import db_tools
import sys

# reload(sys)  # Reload does the trick!
# sys.setdefaultencoding('utf-8')

SYSTEM_SEPARATOR = r'/'

class Tokenizer(object):
    def __init__(self, dir_path, stop_word_path, user_dict_path):

        self.user_dict_path = user_dict_path

        self.stop_word_path = stop_word_path
        self.bloomFilter = BloomFilter(capacity=10000, error_rate=0.0001)

        # 分句正则
        self.phrasing_re = re.compile(ur'([^,!?:;~，。！？：；～]*'
                                      ur'[,|.|!|?|:|;|~|，|。|！|？|：|；|～]+)',
                                      re.VERBOSE | re.IGNORECASE | re.UNICODE)

        self.phrasing_re_2 = re.compile(ur'([^!?;。！？；～]*'
                                        ur'[|.|!|?|;|~|。|！|？|；|～]+)',
                                        re.VERBOSE | re.IGNORECASE | re.UNICODE)

        # 结巴分词进行初始化 (加载词典等等）
        self.init_jieba()

        # 加载停顿词库
        self.load_stop_word()

        if dir_path is not None and os.path.isdir(dir_path):
            self.dir_path = dir_path
            dir_name = dir_path.split(SYSTEM_SEPARATOR)[-1]
            self.token_dir = dir_path.replace(dir_name, 'token_' + dir_name)
            if not os.path.exists(self.token_dir):
                os.mkdir(self.token_dir)

    # 结巴分词进行初始化
    def init_jieba(self):
        # 加载用户词典
        jieba.load_userdict(self.user_dict_path)
        # jieba.add_word(r'(\d+)-(\d+)-(\d+)')
        pass

    def start(self):
        # self.load_stop_word() #加载停顿词库
        self.load_dir(self.dir_path, self.token_dir)
        return self.token_dir

    # 加载停顿词
    def load_stop_word(self):
        with codecs.open(self.stop_word_path, 'rb', encoding='utf-8') as f:
            for line in f:
                self.bloomFilter.add(line.rstrip())

    def load_dir(self, dir_path, new_dir_path):
        file_list = os.listdir(dir_path)
        for file_name in file_list:
            if os.path.isdir(os.path.join(dir_path, file_name)):
                new_dir_path = os.path.join(self.token_dir, file_name)
                if not os.path.exists(new_dir_path):
                    os.mkdir(new_dir_path)
                self.load_dir(os.path.join(dir_path, file_name), new_dir_path)  # 递归遍历
            else:
                file_path = os.path.join(dir_path, file_name)
                new_path = os.path.join(new_dir_path, file_name)
                self.token_file(file_path, new_path)
                # self.token_file2(file_path, new_path)

    def token_file2(self, file_path, save_path):
        save_f = codecs.open(save_path, 'w')
        with codecs.open(file_path, 'r') as f:
            for line in f:
                if len(line) >= 5:
                    no_stop_list = self.cut_sentence(line)
                    save_f.write(" ".join(no_stop_list))
                    # save_f.write('\n')
        save_f.close()

    def token_file(self, file_path, new_path):
        # 分词 ， 除去stop_words , 根据词性选择
        sentense = ""
        # with codecs.open(file_path, 'r', encoding='utf-8') as f:
        with codecs.open(file_path, 'rb', 'gbk', errors='ignore') as f:
            for line in f:
                if not line.startswith(u'【'):
                    line = ''.join(line.split())
                    sentense += line

        no_stop_list = self.cut_sentence(sentense)
        tokener_f = codecs.open(new_path, 'w', encoding='utf-8')
        tokener_f.write(" ".join(no_stop_list))

        # words = pseg.cut("".join(no_stop_list))
        # remove_posseg = "c e h k o p u ud ug uj ul uv uz y".split()
        # # 词性 ， 保存
        # posseg_abs_f = codecs.open(new_path, 'w', encoding='utf-8')
        # for word in no_stop_list:
        #     word = "".join(word.split())
            # if word != "" and len(word) > 1 and flag not in remove_posseg:
        #     posseg_abs_f.write('%s ' % word)
        #
        # posseg_abs_f.close()
        # f.close()

    # 进行分词
    def cut_sentence(self, sentense):
        # # 精确模式 HMM 参数用来控制是否使用 HMM 模型  于未登录词，采用了基于汉字成词能力的 HMM 模型，使用了 Viterbi 算法
        seg_list = jieba.cut(sentense, cut_all=False, HMM=True)
        no_stop_list = self.remove_stop(seg_list)
        return no_stop_list

    # 获取词性
    def posseg_cut(self, document):
        pos_data = jieba.posseg.cut(document)
        pos_list = []
        for w in pos_data:
            pos_list.append((w.word, w.flag))  # make every word and tag as a tuple and add them to a list
        return pos_list

    # 进行分句 ， 进行情感打分
    def phrasing_document(self, document):
        # phrasing_re = re.compile(ur'([^,.!?:;~，。！？：；～]*[,|.|!|?|:|;|~|，|。|！|？|：|；|～])' , re.VERBOSE | re.IGNORECASE|re.UNICODE)
        sen_s = self.phrasing_re.findall(document)
        return sen_s

    def phrasing_document_2(self, document):
        sen_s = self.phrasing_re_2.findall(document)
        return sen_s

    # 去除停顿词
    def remove_stop(self, seg_list):
        return [word for word in seg_list if word not in self.bloomFilter]


if __name__ == "__main__":

    dir_path = r'G:/556/Resource/small_answer'
    stop_words = r'./../resource/stop_words.txt'
    user_dict = r'./../resource/user_dict_less.txt'
    tokener = Tokenizer(dir_path, stop_words, user_dict)
    tokener.start()