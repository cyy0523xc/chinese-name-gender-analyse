#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# @author cyy0523xc@gmail.com
#

import nltk
import random


def gender_features(name):
    '''这种特征简单，在测试集上的准确率约为81%'''
    return {
        "last_w": name[-1]
    }


def gender_features_last2(name):
    if len(name) < 3:
        return {
            "last_w": name[-1],
            "last2_w": 'None'
        }
    return {
        "last_w": name[-1],
        "last2_w": name[-2]
    }


def gender_features_last3(name):
    if len(name) < 3:
        return {
            "last_w": name[-1],
            "last2_w": 'None'
        }
    return {
        "last_w": name[-1],
        "last2_w": name[-2:]
    }


def gender_features_both(name):
    '''经过测试, 这种方法效果最好，在测试集上的准确度约有82%'''
    if len(name) < 3:
        return {
            "last_w": name[-1],
            "last2_w": 'None',
            "both": 'None'
        }
    return {
        "last_w": name[-1],
        "last2_w": name[-2],
        "both": name[-2:]
    }


def get_names(fn):
    with open(fn) as f:
        names = f.readlines()

    return [n.strip().decode('utf8') for n in names]


def train(names, gender_features, show_error=False):
    train_index = len(names) * 9 / 10   # 以1/10作为测试集
    features = [(gender_features(n), g) for (n, g) in names]
    train_set, test_set = features[:train_index], features[train_index:]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print "Train set: %f" % nltk.classify.accuracy(classifier, train_set)
    print "Test set: %f" % nltk.classify.accuracy(classifier, test_set)

    # 查看错误的数据
    if show_error:
        errors = []
        test_names = names[train_index:]
        for (n, g) in test_names:
            prev_g = classifier.classify(gender_features(n))
            if prev_g != g:
                errors.append((n, g))
        for item in errors:
            print u"%s, %s" % item


male_file = "./data/male.txt"
female_file = "./data/female.txt"

male_names = get_names(male_file)
female_names = get_names(female_file)

names = ([(n, 'm') for n in male_names if len(n) < 5] +
         [(n, 'f') for n in female_names if len(n) < 5])
random.shuffle(names)
print "names len = %d" % len(names)

print "*" * 30
print u"使用最后一个字作为特征："
train(names, gender_features)

print "*" * 30
print u"分别使用最后两个字作为特征："
train(names, gender_features_last2)

print "*" * 30
print u"分别使用最后两个字作为特征，同时将最后两个字组合作为特征："
train(names, gender_features_both)

print "*" * 30
print u"分别使用最后一个字作为特征，同时将最后两个字组合作为特征："
train(names, gender_features_last3)
