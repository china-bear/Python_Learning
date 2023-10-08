# -*- coding: utf-8 -*-
import re
import sys
import os


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
输入描述：一个账户内的计划类型下 按计划分组所有创意标题
输入格式：ad_plan_id, {
'ad_plan_id1': [title1, title2, ...],
'ad_plan_id2': [title1, title2, ...],
'ad_plan_id3': [title1, title2, ...],
}
 
示例：
title：苹果手机价格大全<京东>大牌数码产品,火爆热销中!
 
输出：
一个整数
'''
def doc_sim_num(ad_plan_id, kv, threshold_edit=0.85, threshold_jcd=0.8):
    memory_nosim = set()
    memory_sim = set()
    n_sim = 0
    for doca in kv.get(ad_plan_id, []):
        for planid_b in kv:
            if planid_b == ad_plan_id:
                continue
            flag = False
            for docb in kv[planid_b]:
                if doca==docb or (doca,docb) in memory_sim or (docb,doca) in memory_sim:
                    flag = True
                    break
                if (doca,docb) in memory_nosim or (docb,doca) in memory_nosim:
                    continue
                if is_sim(doca, docb, threshold_edit, threshold_jcd):
                    memory_sim.add((doca,docb))
                    flag = True
                    break
                else:
                    memory_nosim.add((doca,docb))
            if flag:
                n_sim += 1
                break
    return n_sim


def convert(data):
    ret = {}
    for line in data.split("\003"):
        rs = line.split("\002")
        plan_id = rs[0]
        arr = rs[1].split("\001")
        ret[plan_id] = arr
    return ret


for line in sys.stdin:
    line = line.strip()
    (ad_user_id, ad_plan_id, advert_title_num, data) = line.split("\t")
    advert_title_dup_num = -1
    try:
        advert_title_dup_num = doc_sim_num(ad_plan_id, convert(data))
    except BaseException as e:
        advert_title_dup_num = -1
    print("\t".join([str(ad_user_id), str(ad_plan_id), str(advert_title_num), str(advert_title_dup_num)]))
