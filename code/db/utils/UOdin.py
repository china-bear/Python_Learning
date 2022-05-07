# -*- coding: UTF-8 -*-

import requests


class UOdin:
    ALARM_URL = 'http://xxxsend'
    ALARM_KEY = 'xxx'
    ALARM_SECRET = 'xxx'

    @staticmethod
    def send(alarm_term, title, app_content, content):
        r = requests.post(UOdin.ALARM_URL, auth=(UOdin.ALARM_KEY, UOdin.ALARM_SECRET), data={'teams': alarm_term, 'title': title, 'app_content': app_content, 'content': content})

        print(r.text)


if __name__ == '__main__':
    UOdin.send('mba_ba_alarm', '测试', '移动端测试内容', '邮件测试内容')
