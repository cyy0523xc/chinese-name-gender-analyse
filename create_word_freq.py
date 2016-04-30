#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# 生成字的频率分布
#
# @author cyy0523xc@gmail.com
#

from collections import Counter

############### 配置BEGIN #############

# 姓名与性别的文件都已经去重过了
male_file = './data/male.txt'
female_file = './data/female.txt'

# 保存的频率分布文件
freq_json_file = './output/name_word_freq.json'

# 判断训练结果的配置
# 通常情况下，错误判断都是比漏判严重的
miss_judge_score = 1    # 无法判断，一个姓名记1分
error_judge_score = 2   # 错误判断，一个姓名记2分

############### 配置END #############


def read_names(filename):
    '''从文件中读取姓名，去掉超过4个汉字的姓名'''
    f = open(filename, 'rb')
    lines = f.readlines()
    lines = (w.strip().decode('utf8') for w in lines)
    lines = [w for w in lines if len(w) < 5]
    return lines


def word_freq(names, position=-1):
    '''计算某个词的分布, 注意分子乘了100'''
    cnt = float(len(names))
    words = Counter(w[position] for w in names)
    words = {w: words[w] * 100 / cnt for w in words}
    return words

# 计算最后一个字的频率分布
male_names = read_names(male_file)
male_word_freq = word_freq(male_names)
female_names = read_names(female_file)
female_word_freq = word_freq(female_names)

# 最小占比（百分比），避免分母为0
len_male_names = len(male_names)
min_male_rate = 100.0 / len_male_names
len_female_names = len(female_names)
min_female_rate = 100.0 / len_female_names

significant_dict = {}
for w in male_word_freq:
    significant_dict[w] = (
        male_word_freq[w] / female_word_freq.get(w, min_female_rate),
        max(male_word_freq[w], female_word_freq.get(w, min_female_rate))
    )

for w in female_word_freq:
    if w in significant_dict:
        continue
    significant_dict[w] = (
        male_word_freq.get(w, min_male_rate) / female_word_freq[w],
        max(male_word_freq.get(w, min_male_rate), female_word_freq[w])
    )


# 保存频率分布
s = "\n".join("%s,%f,%f" % (w.encode('utf8'), significant_dict[w][0],
                            significant_dict[w][1])
              for w in significant_dict)
with open(freq_json_file, 'w+') as f:
    f.write(s)

print 'ok'
