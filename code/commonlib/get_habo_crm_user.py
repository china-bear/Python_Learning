#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import time
import datetime
import hashlib
import urllib
import requests
import urllib.parse
#reload(sys)
#sys.setdefaultencoding('utf-8')


def downloadFile_http(url,filename,app_tag,app_key):
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    times = 1
    while True:
        try:
            header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
            param_list =  url_param(app_tag,app_key)
            r = requests.get(url,params=param_list,headers=header, stream = True)
            print(r.url)
            print(r.encoding)
            r.raise_for_status()
            with open(filename,"wb") as df:
                for chunk in r.iter_content(chunk_size = 1024):
                    if chunk:
                        df.write(chunk)
            break
        except requests.exceptions.ConnectionError:
            times = times + 1
            print('ConnectionError -- please wait 180 seconds')
            time.sleep(180)
        except requests.exceptions.ConnectTimeout:
            times = times + 1
            print('ConnectTimeout -- please wait 180 seconds')
            time.sleep(180) 
        except requests.exceptions.ChunkedEncodingError:
            times = times + 1 
            print('ChunkedEncodingError -- please wait 180 seconds')
            time.sleep(180)
        except requests.exceptions.HTTPError as err:
            times = times + 1
            print(err)
            print('HHTTPError  -- please wait 180 seconds')
            time.sleep(180)
        except Exception as err:
            times = times + 1
            print('An Unknow Error Happened -- Please wait 180 seconds')
            time.sleep(180)
        if times >20:
            print('Connection max times')
            return times

def getMD5 (str):
    m2 = hashlib.md5()
    m2.update(str)
    str_md5 = m2.hexdigest()
    return str_md5.upper()

def url_param(app_tag,app_key):
    data_param = {}
    data_param['appTag'] = app_tag
    ts = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    data_param['timestamp'] = ts
    #parameter_str = urllib.urlencode(data_param)
    parameter_str = urllib.parse.urlencode(data_param)
    parameter_list = parameter_str.split('&')
    parameter_list.sort()
    data_str = '&'.join(parameter_list)
    base = app_key + data_str + app_key
    print ('base====' + base)
    sign_md5 = getMD5(base.encode("utf-8"))
    data_param['sign'] = sign_md5
    return data_param

def runCmd(cmd):
    print(cmd)
    return(os.system(cmd))


if  __name__ == '__main__':
    if len(sys.argv) !=4:
        print('param num:', len(sys.argv))
        sys.exit(1)

    app_tag = sys.argv[1]
    app_key = sys.argv[2]
    tb_name = sys.argv[3]

    url = 'http://api.xx.xx.cn/s3/fileContent'
    hadoop_bin = "/usr/bin/hadoop/software/hadoop/bin/hadoop"
    #day = time.strftime('%Y%m%d',time.localtime())
    day =(datetime.datetime.now()- datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    down_dir = "/home/xxx/habo_crm_info/%s/%s/" %(tb_name,day)
    down_file = "%s%s" %(down_dir,app_tag)
    hdfs_dir = "hdfs://xxx:9000/home/hdp-ads-audit/dubhe_data/hive/%s/" %(tb_name)
    #hdfs_dir = "hdfs://namenode.safe.lycc.qihoo.net:9000/home/hdp-ads-audit/user/xiongyouguo/"
    is_ok = "%s%s/_SUCCESS" %(hdfs_dir,day)
   
    if downloadFile_http(url,down_file,app_tag,app_key) is None:
        print("download file is ok")
        cmd = "%s fs -put -f %s %s" %(hadoop_bin,down_dir,hdfs_dir)
        if runCmd(cmd):
            print("hdfs file put fail")
        else:
            print("hdfs file put success")
            cmd = "%s fs -touchz %s" %(hadoop_bin,is_ok)
            if not runCmd(cmd):
                print("HDFS SUCCESS file  ok")
            else:
                print("hadoop SUCCESS file fail")
    else:
        print("download file fail")
