#!/usr/bin/python
# -*- coding: UTF-8 -*-
#


import csv
from libs import get_word_freq
from name_to_gender import name2gender, GENDER_BOY, GENDER_GIRL, GENDER_UNKNOW

test_file = './data/test.csv'
base = 1.8
rebase = 1.0 / base

freq = get_word_freq()
#print [freq[a] for a in freq]

delimiter = ','
total_cnt = 0
missing_cnt = 0
error_cnt = 0
all_missing = 0
missing_cnt2 = 0
error_cnt2 = 0
with open(test_file, 'rb') as csv_file:
    fieldnames = csv_file.next().strip().split(delimiter)

    reader = csv.DictReader(csv_file, delimiter=delimiter,
                            fieldnames=fieldnames)
    for row in reader:
        name = row['name'].decode('utf8')
        name_len = len(name)
        if name_len > 4:
            continue
        w = name[-1]
        prev = ''  # 预测的值
        gender = row['gender'].decode('utf8')
        total_cnt += 1
        if w in freq and freq[w][1] > 0.04:     # 超过千分之一才会使用
            #print freq[w]
            if freq[w][0] > base:
                prev = u"男"
            elif freq[w][0] < rebase:
                prev = u"女"
        else:
            all_missing += 1
        if prev == gender:
            continue
        if prev == '':
            missing_cnt += 1
        else:
            error_cnt += 1
        #print u"%s: %s ==> %s" % (name, gender, prev)

        default = GENDER_UNKNOW
        if w in freq:
            if freq[w][0] < 1:
                default = GENDER_GIRL
            else:
                default = GENDER_BOY
        prev = name2gender(name, default=default)
        if prev == gender:
            continue
        if prev == u'未知':
            missing_cnt2 += 1
        else:
            error_cnt2 += 1
        print u"%s: %s ==> %s" % (name, gender, prev)

print "T: %d, %d, missing_rate: %f, error_rate: %f" % (total_cnt, all_missing,
                                                   float(missing_cnt) / total_cnt,
                                                   float(error_cnt) / total_cnt,
                                                   )
print "missing_rate2: %f, error_rate2: %f" % (float(missing_cnt2) / total_cnt,
                                              float(error_cnt2) / total_cnt,
                                              )
