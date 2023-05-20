import requests,sys,json
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import time

def base64toEmb(url):

    request_data = {
        "inputs": [{
            "name": "image",
            "shape": [len(url), 1],
            "datatype": "BYTES",
            "data": url
        }],
        "outputs": [{"name": "OUTPUT"}]
    }

    res = requests.post(url=triton_imgemb_url, json=request_data).json()
    if "outputs" not in res:
        return np.asarray([0])
    emb = np.asarray(res["outputs"][0]["data"])
    return emb.reshape(len(url), 768)

def main(args):

    urls = args[0]
    outp = args[1]

    with open(outp, mode='w') as out_:
        for imgurl in urls:
            emb = base64toEmb([imgurl])[0]
            out_.write(','.join(list(map(lambda x:str(x),emb))))


if __name__ == '__main__':
    triton_imgemb_url = "http://gpudev02.adsys.zzzc2.qihoo.net:8020/v2/models/ensemble_r2d2_emb/versions/1/infer"
    inurl = sys.argv[1] #url文件
    outpath = sys.argv[2] #数据保存目录
    ps = 30 #并发数
    urls = [ line.strip() for line in open(inurl)]
    nums = len(urls) / ps + 1
    args = [[ urls[i*nums:(i+1)*nums], outpath+"/res_"+str(i)] for i in range(ps)]

    start = time.time()
    with ProcessPoolExecutor(ps) as pool:
        pool.map(main, args)
    print(time.time()-start)
