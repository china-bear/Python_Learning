#!/bin/bash

#version: 2.0 2018-08-30

if [ "$1" == "night" ];then
  if [ "$2" != ""  ];then
    dt=`date -d "$2 -1 day" +%Y-%m-%d`
  else
    dt=`date -d "-1 day" +%Y-%m-%d`
  fi
else
  if [ "$2" != ""  ];then
    dt=`date -d "$2" +%Y-%m-%d`
  else
    dt=`date -d "-1 day" +%Y-%m-%d`
  fi
fi

# 命令
HIVE_CMD="/usr/bin/hadoop/software/apache-hive-1.2.1U3-bin/bin/hive"
MYSQL_CMD="/usr/bin/mysql"

# 配置参数

source_host=xxx
source_port=3301
source_username=user1
source_password=xxx
source_database=xxx
source_table=solution
target_table=ods_bool_solution

basepath=$(cd `dirname $0`; pwd)

echo "------------------------------------------------------------------------------------------------"
echo "-- 检查分区数据【SELECT COUNT(1) FROM galileo.report_end_flag WHERE date = '${tomorrow}' AND report_type = 'report_mvadx_dsp_total_later2' AND status = 1】"
echo "------------------------------------------------------------------------------------------------"
check_done=0
check_num=0
while [[ ${check_done} -lt 1 ]] && [[ ${check_num} -le 120 ]]
do
check_done=`${MYSQL_CMD} -h${source_host} -P${source_port} -u${source_username} -p${source_password} -D${source_database} -A -N -e "SELECT COUNT(1) FROM galileo.report_end_flag WHERE date =  date_add('${day}', interval 1 day) AND report_type = 'report_mvadx_dsp_total_later2' AND status = 1;"`

if [[ ${check_done} -lt 1 ]] || [[ ${check_done} == '' ]];then
  echo "check_done = ${check_done}"
  sleep 5m
fi
let check_num++

echo "已检测 ${check_num} 次, 检测中... "

if [[ ${check_num} -gt 120 ]];then
  echo "------------------------------------------------------------------------------------------------"
  echo "-- 检查分区数据 失败"
  echo "------------------------------------------------------------------------------------------------"
  exit 1
fi
done
echo "------------------------------------------------------------------------------------------------"
echo "-- 检查分区数据 OK"
echo "------------------------------------------------------------------------------------------------"


/usr/local/bin/python2.7 ${basepath}/../DeleteDone.py --group=ad --project=mba --job=dw --done=${target_table} --date=${dt}

# 目录
LOCAL_PATH=/data/download/mba/${source_database}/${source_table}_${dt}.txt

${MYSQL_CMD} -h${source_host} -P${source_port} -u${source_username} -p${source_password} -D${source_database} -A -N << EOF > ${LOCAL_PATH}
SELECT id,name,disabled,IFNULL(convert_price, 0.000),IFNULL(convert_id, 0),IFNULL(dormerFlag, 0),ocpc_stage FROM ${source_database}.${source_table};
EOF

if [ $? != 0 ]; then
    echo "--------------------------------------------------------------------------------"
    echo "[`date +"%Y-%m-%d %H:%M.%S"`] [error] 同步${source_database}.${source_table}数据到本地磁盘目录${LOCAL_PATH}失败。"
    echo "--------------------------------------------------------------------------------"
    exit 1
fi

echo "--------------------------------------------------------------------------------"
echo "[`date +"%Y-%m-%d %H:%M.%S"`] [info] 同步${source_database}.${source_table}数据到本地磁盘目录${LOCAL_PATH}成功。"
echo "--------------------------------------------------------------------------------"

${HIVE_CMD} << EOF
use xxx;
LOAD DATA LOCAL INPATH '${LOCAL_PATH}'
OVERWRITE INTO TABLE ${target_table} PARTITION (dt = '${dt}');
EOF

if [ $? != 0 ]; then
    echo "--------------------------------------------------------------------------------"
    echo "[`date +"%Y-%m-%d %H:%M.%S"`] [error] 加载表${target_table}分区(dt = '${dt}')失败。"
    echo "--------------------------------------------------------------------------------"
    exit 1
fi

echo "--------------------------------------------------------------------------------"
echo "[`date +"%Y-%m-%d %H:%M.%S"`] [info] 加载表${target_table}分区(dt = '${dt}')成功。"
echo "--------------------------------------------------------------------------------"

/usr/local/bin/python2.7 ${basepath}/../CreateDone.py --group=ad --project=mba --job=dw --done=${target_table} --date=${dt}