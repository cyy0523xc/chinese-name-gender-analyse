#!/usr/bin/python
# -*- coding: UTF-8 -*-
#

freq_json_file = './output/name_word_freq.json'


def get_word_freq():
    with open(freq_json_file) as f:
        lines = f.readlines()

    freq = [l.strip().split(',') for l in lines]
    return {w[0].decode('utf8'): (float(w[1]), float(w[2])) for w in freq}
