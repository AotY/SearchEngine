#!/usr/bin/env python
# -*-coding:utf-8-*-
# QingTao


import codecs


# 把搜狗词库 加上词频 默认为5把。。。
def write_word_frequency(dict_path, store_path):
    # 把txt文件里面的词存储成一个数组

    save_file = codecs.open(store_path, 'w', encoding='utf-8')
    with codecs.open(dict_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip()
            if len(line) < 4:
                save_file.write("%s" % line + " 5")
                save_file.write('\n')

    save_file.close()


if __name__ == "__main__":
    write_word_frequency(u'./../resource/user_dict.txt',
                         u'./../resource/user_dict_less.txt')
