#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib
from urllib import request, parse


def getMD5(data):
    m2 = hashlib.md5()
    m2.update(data)
    str_md5 = m2.hexdigest()
    return str_md5.upper()


data_list = parse.urlencode(
    {"data_list": [{
        "game_session": "g1",
        "timestamp": 123,
        "strategy_id": "s1",
        "exp_id": "e1",
        "ad_pos_type": 1,
        "act_type": 1,
        "count": 1
    }]}
)

req = request.Request('https://game.xxx.qq.com/cgi-bin/gamewxagpartnerrtaapi/game360rtafeedback')
req.add_header('Origin', 'https://passport.weibo.cn')
req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
req.add_header('Referer', 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F%3Fjumpfrom%3Dweibocom')

with request.urlopen(req, data=data_list.encode('utf-8')) as f:
    print('Status:', f.status, f.reason)
    for k, v in f.getheaders():
        print('%s: %s' % (k, v))
    print('Data:', f.read().decode('utf-8'))
