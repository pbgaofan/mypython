#coding:utf-8
import string
import time
import json
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

#path='E:\mypython\\Walden.txt'

def frequence(path):
    with open(path,'r') as text:
        words=text.read().split()
        words_index=[raw_word.strip(string.punctuation).lower() for raw_word in words]
        words_set=set(words_index)
        words_count={word:words_index.count(word) for word in words_set}
        for word in words_set:
            print(word,words_count[word])

start=time.time()
frequence('E:\mypython\\Walden.txt')
end=time.time()
print('总耗时{}秒'.format(end-start))
