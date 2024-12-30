#! /usr/bin/env python

import hashlib
from urllib import request, parse
import json
import time


def getMD5(_data):
    m2 = hashlib.md5()
    m2.update(_data.encode('utf-8'))
    str_md5 = m2.hexdigest()
    return str_md5


def url_param(_body, _token):
    param = {}
    ts = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    param['time'] = ts
    base = _body + _token + ts
    sign_md5 = getMD5(base.encode("utf-8"))
    param['authorization'] = sign_md5
    return param


if __name__ == '__main__':

    ts = str(int(time.time()))
    print("ts: " + ts)
    data = {"data_list": [{
        "game_session": "CBgAA8JyfBuqS19Efq-n5tW4Vx3smqefolWeJj9REEsWhBo4vkc7n6Cns5jPYazmPOhgX-F_FfQuA",
        "timestamp": 17353205320,
        "strategy_id": "4",
        "exp_id": "wx7f3cbe05a268e325",
        "ad_pos_type": 1,
        "act_type": 1,
        "count": 1
    }]}

    token = "123"

    try:
        body = json.dumps(data)
        print(body)

        body_md5 = getMD5(body).lower()
        print("body_md5" + ": " + body_md5)

        auth = getMD5(body_md5 + token + ts)
        print("authorization" + ": " + auth)

        qq_url = "https://xxx/cgi-bin/gamewxagpartnerrtaapi/game360rtafeedback?time={_ts}&authorization={_authorization}".format(_ts=ts, _authorization=auth)
        print("url: " + qq_url)
        res = request.urlopen(request.Request(qq_url, body.encode('utf-8'), {'Content-Type': 'application/json'}))
        print(res.read())
    except Exception as e:
        print(Exception, ":", e)
