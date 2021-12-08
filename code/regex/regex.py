#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

print('Test: 010-12345')
m = re.match(r'^(\d{3})-(\d{3,8})$', '010-12345')
print(m.group(1), m.group(2))

t = '19:05:30'
print('Test:', t)
m = re.match(r'^(0[0-9]|1[0-9]|2[0-3]|[0-9])\:(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|[0-9])\:(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|[0-9])$', t)
print(m.groups())


print('{latitude} {longitude} {latitude}'.format(latitude=41.123, longitude=71.091, test=100))


geopoint = {'latitude': 41.123, 'longitude': 71.091, 'test01': 'a', 'test02': 100}
print('{latitude} {longitude}'.format(**geopoint))

print('{latitude} {longitude} {longitude}'.format(**geopoint))

print('{latitude} {longitude} {longitude} {test02}'.format(**geopoint))


sql = """
-- 1. 检查 IP库 开始和结束位置 总量是否等于4294967296  --
select dt, data_type, min(ip_end), max(ip_end), min(ip_begin), max(ip_begin), max(ip_end) - min(ip_begin) + 1,  sum(ip_end-ip_begin +1)
from dim_ip_address
where dt = '{day}' 
group by dt, data_type 

;

-- 2.  最近2天  记录数 和  IP数据量同比 --
select t1.dt, t1.data_type, t1.country, t1.num, t1.ip_sum,t2.dt, t2.data_type, t2.country, t2.num, t2.ip_sum,  t2.num - t1.num , t2.ip_sum - t1.ip_sum
from
  (select dt, data_type, country, count(*) num, sum(ip_end-ip_begin) ip_sum
  from dim_ip_address
  where dt = '{day}' 
  group by dt, data_type, country ) t1
left outer join
  (select dt, data_type, country,count(*) num, sum(ip_end-ip_begin) ip_sum
  from xyg_dim_ip_address
  where dt = '{day}'
  group by dt, data_type, country ) t2
on t1.country = t2.country and t1.data_type = t2.data_type
order by t1.dt  


;
"""

with open('a1.sql', 'r', encoding='utf8') as f1:
    with open('a2.sql', 'w', encoding='utf8') as f2:
        sql_str = re.sub(r"(\r\n|\n)*;$", "", f1.read().rstrip().format(day='2021-12-18'))
        print(sql_str, file=f2)
        print(re.sub(r"(\r\n|\n)*;$", "", sql.rstrip().format(**{'day': '2028-12-20'})))
