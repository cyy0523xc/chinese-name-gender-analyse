#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# 从中文姓名里分析性别
#

import re
import logging
import chardet
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
logging.basicConfig(filename='/tmp/test.log', level=logging.DEBUG)

# 名字常用字, 注意这两个字符串不能有重复的字
girl_name_words = u'宁璇玉伊妍琴咏钗香媛枝娜贞萱欢馥碧锦琬纯莉芳玲涵娴然莹瑞羽琼线菁融蕊珍华姑蓓青燕晶黛岚凝凡韵绣莺悦爽雯念绿洁佳菀眉美璐端澜君娟娣纨含霭芬妮琳莲芸霞鹃珊菊轩晓寒瑗静飘惜惠璧彩影艳菲婷叶盼沁梅霄薇淑月云舒芝茜素琦缨枫环花露鸾雁桂雅翠蓉秋苑妹毓霜荔莎勤筠姣彤巧聪园可英兰柳瑶竹艺瑾仪娅嘉萍斐霓茗颖洛亚思喜真怡宠欣红娥琰梦倩馨紫昭冬宜爱冰育丹丽秀婉瓶婕柔珠荣滢凤慧雪希姬凰女婵荷银虹卿妈姗筱敏微诗琪'
boy_name_words = u'伟刚勇毅俊峰强军平东文辉力明永健世广义兴良海山仁波宁贵福生龙元全国胜学祥才发利清飞彬富顺信子杰涛昌成康星光天达安岩林有坚和彪博诚先敬震振壮会思豪心邦承乐绍功松厚庆磊民友裕河哲江超浩亮政谦亨固轮翰朗伯宏言若鸣朋斌梁栋维启克伦翔旭皓晨辰士建家致炎德行时泰盛雄琛钧冠策腾弘志武中榕奇鹏楠泽风茂航伍亘好休亦次守旭宇吉兆仰向至共仲舟再存先争光冲丞列寺旬灰旨朱任艮百同伊州安印全牟朽圳江汛竹如仿合西竹曲夷夙灯伎伉羽后名回因多耳帆雷'

girl_name_words = {key: 1 for key in list(girl_name_words)}
boy_name_words = {key: 1 for key in list(boy_name_words)}

# 性别值
GENDER_GIRL = 0
GENDER_BOY = 1
GENDER_UNKNOW = 2

gender_title = [u"女", u"男", u"未知"]

chinese = ur"([\u4e00-\u9fa5]+)"
pattern = re.compile(chinese)


def name2gender(name, default=GENDER_UNKNOW):
    def _cal_name2gender(name, default):
        # 格式化名字
        name = name.split(' ')
        name = name[0].strip()
        if not name:
            #logging.debug('a')
            return GENDER_UNKNOW
        #__test = chardet.detect(name)
        #logging.debug(__test['encoding'])
        name = pattern.findall(name)
        if not name:
            #logging.debug('b')
            return GENDER_UNKNOW
        name = name[0]

        name_len = len(name)
        if name_len < 2 or name_len > 4:
            #logging.debug('c')
            return GENDER_UNKNOW

        if name_len == 2:
            return _check_word_gender(name[1])

        first = _check_word_gender(name[name_len-2])
        last = _check_word_gender(name[name_len-1])
        if first == last:
            return first
        if first == GENDER_UNKNOW:
            return last
        if last == GENDER_UNKNOW:
            return first
        return default

    def _check_word_gender(word):
        if word in girl_name_words:
            #logging.debug('---> GIRL')
            return GENDER_GIRL
        if word in boy_name_words:
            #logging.debug('---> BOY')
            return GENDER_BOY
        return GENDER_UNKNOW

    gender = _cal_name2gender(name, default)
    #logging.debug("==> %s ==> %d" % (name, gender))
    return gender_title[gender]
