#!/usr/bin/env python
# -*- coding: utf-8 -*-
# QingTao

from trace import pickle
# from multiprocessing import Process
import operator
from gensim import similarities
import time

# def load_model():
from SearchEngine.preprocessing.tokenizer import Tokenizer

tfidf_model = pickle.load(open(r'G:\556\Project\SearchEngine\SearchEngine\resource\tfidf_model.pkl', 'r'))
dictionary = pickle.load(open(r'G:\556\Project\SearchEngine\SearchEngine\resource\tfidf_dictionary.pkl', 'r'))
corpus_tfidf = pickle.load(open(r'G:\556\Project\SearchEngine\SearchEngine\resource\corpus_tfidf.pkl', 'r'))


dir_path = r''
stop_words = r'G:\556\Project\SearchEngine\SearchEngine\resource\stop_words.txt'
user_dict = r'G:\556\Project\SearchEngine\SearchEngine\resource\user_dict_less.txt'
tokener = Tokenizer(dir_path, stop_words, user_dict)

# 加载文件，展示
index_dict = pickle.load(open(r'G:\556\Project\SearchEngine\SearchEngine\resource\index_dict.pkl', 'r'))

def get_path(index):
    return index_dict.get(index)

def token(keyword):
    query_word = tokener.cut_sentence(keyword)
    return query_word


def transform(query_word):
    vec_bow = dictionary.doc2bow(query_word)
    vec_tfidf = tfidf_model[vec_bow]
    return vec_tfidf


def query_sim(vec_tfidf):
    index = similarities.MatrixSimilarity(corpus_tfidf)
    sims = index[vec_tfidf]
    similarity = list(sims)

    # 进行排序，选择前100个进行显示
    sim_dict = {}
    for i in range(0, len(similarity)):
        sim_dict[i] = similarity[i]
    # 取前一百个
    index_list = []
    sim_dict = sorted(sim_dict.items(), key=operator.itemgetter(1), reverse=True)[:100]
    for sim in sim_dict:
        print sim[0], ' --- ', sim[1]
        index_list.append(sim[0])
    return index_list


if __name__ == '__main__':
    start_time = time.time()
    query = u'文学 艺术 理论 建设 发展 应该 密切 关注 文学 艺术 实际 存在 状态 已然 可能 发生 变化 浅近 道理 大约 都 不会 怀疑'

    query = token(query)
    vec_idf = transform(query)
    print query_sim(vec_idf)
    print 'total time:    ', time.time() - start_time

    # tfidf_model = None
    # dictionary = None
    # corpus_tfidf = None
    #
    # p = Process(target=load_model, args=(tfidf_model, dictionary, corpus_tfidf))
    # p.start()
    # print tfidf_model == None
