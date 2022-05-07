# -*- coding: UTF-8 -*-

import logging

import requests


class UDone(object):
    @staticmethod
    def create(group, project, job, done):
        url = "http://xxxx/done/create/{GROUPURL}/{PROJECTURL}/{JOBURL}/{DONEFILENAME}".format(
            GROUPURL=group,
            PROJECTURL=project,
            JOBURL=job,
            DONEFILENAME=done,
        )

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

        try:
            # params 接收一个字典或者字符串的查询参数，字典类型自动转换为url编码，不需要urlencode()
            response = requests.get(url, headers=headers)

            status = response.text
        except BaseException as e:
            logging.error('Create done by curl failed [{_url}]'.format(_url=url))
            raise

        return status

    @staticmethod
    def check(_host, _group, _project, _job, _done, _date):

        if _project == 'hdp-ads-dw':
            url = "http://{_host}/done/select?tbName={_done}&doneSuffix={_date}&doneGroup={_project}&token=01c6cda6528953efe032a738a16b2621".format(
                _host=_host,
                _group=_group,
                _project=_project,
                _job=_job,
                _done=_done,
                _date=_date,
            )
        else:
            url = "http://{_host}/done/retrieves/{_group}/{_project}/{_job}/{_done}_{_date}".format(
                _host=_host,
                _group=_group,
                _project=_project,
                _job=_job,
                _done=_done,
                _date=_date,
            )

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

        try:
            # params 接收一个字典或者字符串的查询参数，字典类型自动转换为url编码，不需要urlencode()
            response = requests.get(url, headers=headers)

            status = response.text

            print('检查Done标记：【{_status}】=【{_url}】'.format(_status=status, _url=url))
        except BaseException as e:
            logging.error('check done by curl failed [{_url}]'.format(_url=url))
            raise e

        return status

    @staticmethod
    def delete(group, project, job, done):
        url = "http://xxx/done/delete/{GROUPURL}/{PROJECTURL}/{JOBURL}/{DONEFILENAME}".format(
            GROUPURL=group,
            PROJECTURL=project,
            JOBURL=job,
            DONEFILENAME=done,
        )

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

        try:
            # params 接收一个字典或者字符串的查询参数，字典类型自动转换为url编码，不需要urlencode()
            response = requests.get(url, headers=headers)

            status = response.text
        except BaseException as e:
            logging.error('delete done by curl failed [{_url}]'.format(_url=url))
            raise e

        return status
