import sys
import urllib.request
import json
import time

triton_imgemb_url = "http://xxx.adsys.xx.xx.net"


def get_data(pic):
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
        res = urllib.request.urlopen(urllib.request.Request(triton_imgemb_url, param.encode('utf-8'), {'Content-Type': 'application/json'}), timeout=6)
        return res.read()

    except Exception as e:
        #print(Exception, ":", e)
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
            #print(Exception, ":", e)
            return ""
    else:
        return ""


for line in sys.stdin:
    line = line.strip()
    (pic_url,) = line.split('\t')
    vector = extract_res(get_data(pic_url))
    if vector == '':
        for x in range(3):
            time.sleep(1)
            vector = extract_res(get_data(pic_url))
            if vector != '':
                break
    print('\t'.join([str(pic_url), str(vector)]))
