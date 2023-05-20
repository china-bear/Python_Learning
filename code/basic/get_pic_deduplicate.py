# -*- coding: utf-8 -*-
import sys
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


def get_input(data):
    kv = {}
    for url_emb in data:
        url, emb = url_emb
        kv.setdefault(url, emb)
    return kv


# ****************************************************
# platform: pc or mob
# data: [[url1, emb1], [url2, emb2] ...]
# emb: 0.11:0.22:0.121...
# ****************************************************
def compute(platform, data):
   
    if platform.lower() == 'pc':
        threshold = 0.98
    elif platform.lower() == 'mob':
        threshold = 0.97
    else:
        raise Exception("invalid platform!", platform)

    kv_url2emb = get_input(data)
    
    data = list(kv_url2emb.values())
    
    deduplicate_set = set()
    compare_set = set()
    deduplicate_set.add(data[0])
    compare_set.add(data[0])
    memory = {}
    for s in data[1:]:
        flag = False
        for cmp_s in compare_set:
            if s<cmp_s:
                key = s+"\001"+cmp_s
            else:
                key = cmp_s+"\001"+s
            sim = memory.get(key, -1)
            if sim<0:
                sim = similarity(s, cmp_s)
            if sim > threshold:
                flag = True
                break
        if flag==False:
            deduplicate_set.add(s)
        compare_set.add(s)
    return len(deduplicate_set)


def convert(data):
    data = data.split("\001")
    ret = list()
    for i in range(0,len(data), 2):
        ret.append(data[i:i+2])

    return ret


if __name__ == '__main__':
    datafile = sys.argv[1]
    with open(datafile, mode='r') as inFile:
    # Read all data from file. data = inFile.read()
        for line in inFile:
            (ad_user_id,ad_plan_id,ad_plan_device,ad_group_id,ad_picture_type,ad_picture_num,platform,data) = line.strip().split('\t')
            duplicate_picture_num = compute(platform, convert(data))
            print('\t'.join([str(ad_user_id),str(ad_plan_id),str(ad_plan_device),str(ad_group_id),str(ad_picture_num),str(duplicate_picture_num)]))


