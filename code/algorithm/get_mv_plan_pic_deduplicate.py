# -*- coding: utf-8 -*-
import sys
import os
import numpy as np


def similarity(a, b, sep=':'):
    a = np.asarray(a.split(sep), dtype=np.float64)
    b = np.asarray(b.split(sep), dtype=np.float64)
    a_norm = np.linalg.norm(a)
    b_norm = np.linalg.norm(b)
    if a.shape != b.shape:
        return -1
    sim_score = np.dot(a, b.T) / (a_norm * b_norm)
    return sim_score


'''
输入类型：string, dict
输入描述：一个账户内的同尺寸下 按计划分组所有图片url及其embedding（向量）
输入格式：ad_plan_id, {
'ad_plan_id1': [[url1, embedding1], [url2, embedding2], ...],
'ad_plan_id2': [[url1, embedding1], [url2, embedding2], ...],
'ad_plan_id3': [[url1, embedding1], [url2, embedding2], ...],
}
示例：
url：http://p0.xxx.com/t01888ff3ea1dccac01.png
embedding（string）：-0.204647154:0.195074424:...:-0.290800512
 
输出：一个整数
'''


def pic_sim_num(ad_plan_id, kv, threshold=0.97):
    memory_sim = set()
    memory_nosim = set()

    n_sim = 0
    for img_a in kv.get(ad_plan_id, []):
        try:
            url_a, emb_a = img_a
        except:
            continue
        if not url_a or not emb_a:
            continue
        for planid_b in kv:
            if planid_b == ad_plan_id:
                continue
            flag = False
            for img_b in kv[planid_b]:
                try:
                    url_b, emb_b = img_b
                except:
                    continue
                if not url_b or not emb_b:
                    continue
                if url_a == url_b or (url_a, url_b) in memory_sim or (url_b, url_a) in memory_sim:
                    flag = True
                    break
                elif (url_a, url_b) in memory_nosim or (url_b, url_a) in memory_nosim:
                    continue
                score = similarity(emb_a, emb_b)
                if score > threshold:
                    memory_sim.add((url_a, url_b))
                    flag = True
                    break
                else:
                    memory_nosim.add((url_a, url_b))
            if flag:
                n_sim += 1
                break
    return n_sim


def convert(data):
    ret = {}
    for line in data.split("\003"):
        rs = line.split("\002")
        plan_id = rs[0]
        pic_vector = rs[1].split("\001")
        arr = []
        for i in range(0, len(pic_vector), 2):
            arr.append(pic_vector[i:i + 2])
        ret[plan_id] = arr
    return ret


for line in sys.stdin:
    line = line.strip()
    (ad_user_id, ad_plan_id, creative_size, img_num, data) = line.split("\t")
    img_dup_num = -1
    try:
        img_dup_num = pic_sim_num(ad_plan_id, convert(data))
    except BaseException as e:
        img_dup_num = -1
    print("\t".join([str(ad_user_id), str(ad_plan_id), str(creative_size), str(img_num), str(img_dup_num)]))
