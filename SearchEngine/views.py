#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import pickle
from django.shortcuts import render, render_to_response

# Create your views here.
from SearchEngine.models.file import File
from SearchEngine.similarity.tfidf_sim_tool import query_sim, transform, get_path
from SearchEngine.similarity.tfidf_sim_tool import token
from django.template import RequestContext


def search(request):
    print 'request.method: ', request.method
    if request.method == "POST":
        keyword = request.POST.get('keyword-input')
        if keyword is None or keyword == '':
            index = request.POST.get('index')
            if index is not None:
                print 'index-------------', index
                # file_path = request.POST['path']
                index = request.POST['index']

                with codecs.open(get_path(int(index)), 'rb', 'gbk', errors='ignore') as f:
                    content = ''
                    for line in f:
                        content += line + '\n'
                    name = f.name.split('\\')[-1]

                return render(request, 'SearchEngine/display_content.html', {"name": name, "content": content})
        else:
            print "keyword-input=================", request.POST['keyword-input'].encode('utf-8')
            keyword = request.POST['keyword-input']
            last_query = keyword
            files = query(keyword)
            return render(request, 'SearchEngine/search_result.html', {"files": files, "last_query": last_query})

    else:
        return render(request, 'SearchEngine/search.html')


def search_result(request):
    if request.method == "POST":
        keyword = request.POST['keyword-input']
        last_query = keyword
        files = query(keyword)
        return render(request, 'SearchEngine/search_result.html', {"files": files, "last_query": last_query})


def query(keyword):
    # 分词，去停顿词, 向量化， 相识度计算
    query_word = token(keyword)
    vec_tfidf = transform(query_word)
    index_list = query_sim(vec_tfidf)
    files = []
    for index in index_list:
        file_path = get_path(index)
        if file_path is not None:
            # 加载文件
            with codecs.open(file_path, 'rb', 'gbk', errors='ignore') as f:
                file_name = f.name.split('\\')[-1]
                file_content = f.read(1024)
                file = File(file_name, file_content, index)
                files.append(file)
    return files


def display_content(request):
    if request.method == "POST":
        index = request.POST.get('index')
        if index is not None:
            print 'index-------------', index
            # file_path = request.POST['path']
            index = request.POST['index']

            with codecs.open(get_path(int(index)), 'rb', 'gbk', errors='ignore') as f:
                content = ''
                for line in f:
                    content += line
                name = f.name.split('\\')[-1]

            return render(request, 'SearchEngine/display_content.html', {"name": name, "content": content})
        else:
            return render(request, 'SearchEngine/display_content.html', {"name": '', "content": ''})