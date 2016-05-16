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


# 名字常用字, 注意这两个字符串不能有重复的字
female_name_words = u'宁璇玉伊妍琴咏钗香媛枝娜贞萱欢馥碧锦琬纯莉芳玲涵娴然莹瑞羽琼线菁融蕊珍华姑蓓青燕晶黛岚凝凡韵绣莺悦爽雯念绿洁佳菀眉美璐端澜君娟娣纨含霭芬妮琳莲芸霞鹃珊菊轩晓寒瑗静飘惜惠璧彩影艳菲婷叶盼沁梅霄薇淑月云舒芝茜素琦缨枫环花露鸾雁桂雅翠蓉秋苑妹毓霜荔莎勤筠姣彤巧聪园可英兰柳瑶竹艺瑾仪娅嘉萍斐霓茗颖洛亚思喜真怡宠欣红娥琰梦倩馨紫昭冬宜爱冰育丹丽秀婉瓶婕柔珠荣滢凤慧雪希姬凰女婵荷银虹卿妈姗筱敏微诗琪'
male_name_words = u'伟刚勇毅俊峰强军平东文辉力明永健世广义兴良海山仁波宁贵福生龙元全国胜学祥才发利清飞彬富顺信子杰涛昌成康星光天达安岩林有坚和彪博诚先敬震振壮会思豪心邦承乐绍功松厚庆磊民友裕河哲江超浩亮政谦亨固轮翰朗伯宏言若鸣朋斌梁栋维启克伦翔旭皓晨辰士建家致炎德行时泰盛雄琛钧冠策腾弘志武中榕奇鹏楠泽风茂航伍亘好休亦次守旭宇吉兆仰向至共仲舟再存先争光冲丞列寺旬灰旨朱任艮百同伊州安印全牟朽圳江汛竹如仿合西竹曲夷夙灯伎伉羽后名回因多耳帆雷'

train_index = len(names) * 9 / 10   # 以1/10作为测试集
features = [(gender_features(n), g) for (n, g) in names]
train_set, test_set = features[:train_index], features[train_index:]
classifier = nltk.NaiveBayesClassifier.train(train_set)

print '*' * 30
print u'女性常用字'
for w in list(female_name_words):
    prev_g = classifier.classify({'last_w': w})
    if prev_g != 'f':
        print w

print '*' * 30
print u'男性常用字'
for w in list(male_name_words):
    prev_g = classifier.classify({'last_w': w})
    if prev_g != 'm':
        print w
