#! /usr/bin/env python
import sys
import os
import urllib.request
import json

triton_imgemb_url = "http://gpudev02.adsys.zzzc2.qihoo.net:8020/v2/models/ensemble_r2d2_emb/versions/1/infer"


def getData(pic):
    pic_url = [pic]

    request_data = {
        "inputs": [{
            "name": "image",
            "shape": [len(pic_url), 1],
            "datatype": "BYTES",
            "data": pic_url
        }],
        "outputs": [{"name": "OUTPUT"}]
    }

    try:
        param = json.dumps(request_data)
        res = urllib.request.urlopen(urllib.request.Request(triton_imgemb_url, param.encode('utf-8'), {'Content-Type': 'application/json'}), timeout=3)
        # result = json.loads(res.read())
        return res.read()

    except Exception as e:
        print(Exception, ":", e)
        return ""


def extract_res(res):
    if len(res) > 0:
        try:
            result = json.loads(res)
            if 'error' in result:
                return ""
            else:
                return result['outputs'][0]['data']
        except Exception as e:
            print(Exception, ":", e)
            return ""
    else:
        return ""


url = "http://p0.qhimg.com/t01888ff3ea1dccac01.png"

extract_res(getData(url))

# for line in sys.stdin:
#     line = line.strip()
#     (pic_url,) = line.split('\t')
#     vector = extract_res(getData(pic_url))
#
#     print('\t'.join([str(pic_url), str(vector)]))
