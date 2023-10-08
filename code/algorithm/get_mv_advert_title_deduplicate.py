# -*- coding: utf-8 -*-
import sys
import os
import re


def cleantxt(raw):
    fil = re.compile('[^0-9a-zA-Z\u4E00-\u9FA5]+')
    clean = fil.sub('', raw)
    return clean.lower()

def edit_dist_score(str1, str2):
    matrix = [[i + j for j in range(len(str2) + 1)] for i in range(len(str1) + 1)]
    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            if str1[i - 1] == str2[j - 1]:
                d = 0
            else:
                d = 1
            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + d)
    d_edit = matrix[len(str1)][len(str2)]
    max_len = max(len(str1), len(str2))
    return (max_len-d_edit)/max_len

def jaccard_score(s1, s2):
    inter = len(set(s1).intersection(set(s2)))
    union = len(set(s1).union(set(s2)))
    return inter/union

def is_sim(s1, s2, threshold_edit, threshold_jcd):
    s1 = cleantxt(s1)
    s2 = cleantxt(s2)
    if s1==s2:
        return True
    if jaccard_score(s1,s2)>threshold_jcd:
        return True
    if edit_dist_score(s1,s2)> threshold_edit:
        return True
    return False

'''
输入类型：string, dict
输入描述：一个账户内的计划类型下 按创意分组所有创意标题
输入格式：ad_advert_id, title, {
'ad_advert_id1': [title1, title2, ...],
'ad_advert_id2': [title1, title2, ...],
'ad_advert_id3': [title1, title2, ...],
}
 
示例：
title：苹果手机价格大全<京东>大牌数码产品,火爆热销中!
 
输出类型：string
输出描述：相识 创意ID和标题
输出格式
 {'ad_advert_id1': [title1, title2, ...],
'ad_advert_id2': [title1, title2, ...],
'ad_advert_id3': [title1, title2, ...], }
'''
def doc_sim(ad_advert_id, title, kv, threshold_edit=0.85, threshold_jcd=0.8, cnt_limit=None):
    ret = {}

    memory_sim = set()
    memory_nosim = set()

    for adid_b in kv:
        if cnt_limit and len(ret)>=cnt_limit:
            break
        if adid_b == ad_advert_id:
            continue
        for title_b in kv.get(adid_b, []):
            if title_b==title or (title, title_b) in memory_sim or (title_b, title) in memory_sim:
                ret.setdefault(adid_b, []).append(title_b)
                continue
            if (title, title_b) in memory_nosim or (title_b, title) in memory_nosim:
                continue
            if is_sim(title, title_b, threshold_edit, threshold_jcd):
                memory_sim.add((title, title_b))
                ret.setdefault(adid_b, []).append(title_b)
            else:
                memory_nosim.add((title, title_b))
    return ret


def convert(data):
    ret = {}
    for line in data.split("\003"):
        rs = line.split("\002")
        advert_id = rs[0]
        arr = rs[1].split("\001")
        ret[advert_id] = arr
    return ret


def cal_doc_num(d):
    rs = 0
    for key in d.keys():
        rs = rs + len(d[key])
    return rs


for line in sys.stdin:
    line = line.strip()
    (ad_user_id, ad_advert_id, advert_title, advert_title_num, data) = line.split("\t")
    advert_dup_title = {}
    advert_title_dup_num = -1
    try:
        advert_dup_title = doc_sim(ad_advert_id, advert_title, convert(data))
        advert_title_dup_num = cal_doc_num(advert_dup_title)
    except BaseException as e:
        advert_dup_title = {}
        advert_title_dup_num = -1
    print("\t".join([str(ad_user_id), str(ad_advert_id), str(advert_title), str(advert_title_num), str(advert_title_dup_num), str(advert_dup_title)]))
