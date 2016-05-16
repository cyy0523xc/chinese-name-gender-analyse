#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# @author cyy0523xc@gmail.com
#

from sklearn import tree
import random


def gender_features(name):
    return [name[-1].encode('utf8')]


def get_names(fn):
    with open(fn) as f:
        names = f.readlines()

    return [n.strip().decode('utf8') for n in names]


male_file = "./data/male.txt"
female_file = "./data/female.txt"

male_names = get_names(male_file)
female_names = get_names(female_file)

names = ([(n, 1) for n in male_names if len(n) < 5] +
         [(n, 0) for n in female_names if len(n) < 5])
random.shuffle(names)
print "names len = %d" % len(names)

index = len(names) * 9 / 10
features = [[gender_features(n[0])] for n in names[:index]]
labels = [n[1] for n in names[:index]]

clf = tree.DecisionTreeClassifier()
clf = clf.fit(features, labels)
count = [0, 0]
for name in names[index:]:
    print clf.predict([gender_features(name[0])])
