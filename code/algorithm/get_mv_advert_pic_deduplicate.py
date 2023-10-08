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
    sim_score = np.dot(a, b.T)/(a_norm * b_norm)
    return sim_score

'''
输入类型：string, dict
输入描述：一个账户内的同尺寸下 按创意分组所有图片url及其embedding（向量）
输入格式：ad_advert_id, url, embedding, {
'ad_advert_id1': [[url1, embedding1], [url2, embedding2], ...],
'ad_advert_id2': [[url1, embedding1], [url2, embedding2], ...],
'ad_advert_id3': [[url1, embedding1], [url2, embedding2], ...],
}
示例：
url：http://p0.xxx.com/t01888ff3ea1dccac01.png
embedding（string）：-0.204647154:0.195074424:...:-0.290800512
 
输出
输出类型：string
输出描述：相识 创意ID和 图片URL
输出格式
{
'ad_advert_id1': [url1,url2,  ...],
 
'ad_advert_id2': [url1,url2,  ...],
'ad_advert_id3': [url1,url2,  ...],
}
'''

def pic_sim(ad_advert_id, url, embedding, kv, score_threshold=0.97, cnt_limit=None):
    ret = {}
    memory_sim = set()
    memory_nosim = set()

    for adid_b in kv:
        if cnt_limit and len(ret)>=cnt_limit:
            break
        if adid_b == ad_advert_id:
            continue
        for img_b in kv.get(adid_b, []):
            try:
                url_b, emb_b = img_b
            except:
                continue
            if not url_b or not emb_b:
                continue
            if url_b==url or (url, url_b) in memory_sim or (url_b, url) in memory_sim:
                ret.setdefault(adid_b, []).append(url_b)
                continue
            if (url, url_b) in memory_nosim or (url_b, url) in memory_nosim:
                continue
            if similarity(embedding, emb_b) > score_threshold:
                memory_sim.add((url, url_b))
                ret.setdefault(adid_b, []).append(url_b)
            else:
                memory_nosim.add((url, url_b))
    return ret


def convert(data):
    ret = {}
    for line in data.split("\003"):
        rs = line.split("\002")
        ad_advert_id = rs[0]
        pic_vector = rs[1].split("\001")
        arr = []
        for i in range(0, len(pic_vector), 2):
            arr.append(pic_vector[i:i + 2])
        ret[ad_advert_id] = arr
    return ret


def cal_img_num(d):
    rs = 0
    for key in d.keys():
        rs = rs + len(d[key])
    return rs


for line in sys.stdin:
    line = line.strip()
    (ad_user_id, ad_advert_id, creative_size, img_url, pic_vector, img_num, data) = line.split("\t")
    img_dup_url = {}
    img_dup_num = -1
    try:
        img_dup_url = pic_sim(ad_advert_id, img_url, pic_vector, convert(data))
        img_dup_num = cal_img_num(img_dup_url)
    except BaseException as e:
        img_dup_url = {}
        img_dup_num = -1
    print("\t".join([str(ad_user_id), str(ad_advert_id), str(creative_size), str(img_url), str(img_num), str(img_dup_num), str(img_dup_url)]))
