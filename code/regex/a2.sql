-- 1. 检查 IP库 开始和结束位置 总量是否等于4294967296  --
select dt, data_type, min(ip_end), max(ip_end), min(ip_begin), max(ip_begin), max(ip_end) - min(ip_begin) + 1,  sum(ip_end-ip_begin +1)
from dim_ip_address
where dt = '2021-12-18'
group by dt, data_type
;

-- 2.  最近2天  记录数 和  IP数据量同比 --
select t1.dt, t1.data_type, t1.country, t1.num, t1.ip_sum,t2.dt, t2.data_type, t2.country, t2.num, t2.ip_sum,  t2.num - t1.num , t2.ip_sum - t1.ip_sum
from
(select dt, data_type, country, count(*) num, sum(ip_end-ip_begin) ip_sum
from dim_ip_address
where dt = '2021-12-18'
group by dt, data_type, country ) t1
left outer join
(select dt, data_type, country,count(*) num, sum(ip_end-ip_begin) ip_sum
from xyg_dim_ip_address
where dt = '2021-12-18'
group by dt, data_type, country ) t2
on t1.country = t2.country and t1.data_type = t2.data_type
order by t1.dt
