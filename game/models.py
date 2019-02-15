# -*- coding: utf-8 -*-
# @Time    : 2018/3/21 下午10:28
# @Author  : zeali
# @Email   : zealiemai@gmail.com
# @File    : core.py.py
# @Software: PyCharm
import re
import string
import random
import uuid
import json
import requests
import time
import logging
from datetime import datetime
from bs4 import BeautifulSoup


class MindReader():
    last_question = ''
    def __init__(self, ai_user=None, ai_session_id=None, sender_id=None, cookieid=None, dialog_index=-1,last_question={}):
        self.ai_user = ai_user
        self.sender_id = sender_id
        self.cookieid = cookieid
        self.ai_session_id = ai_session_id
        self.dialog_index = dialog_index
        self.last_question = last_question
        self.cpid = ''
        self.salt = ''
        self.ARRAffinity = ''

        if dialog_index == -1:
            self.sender_id = str(uuid.uuid4())
            self.init_client()

    def gan_headers(self):
        data = {
            "Content-Type": "application/json",
            "Host": "webapps.msxiaobing.com",
            "Accept-Language": "'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:58.0) Gecko/20100101 Firefox/58.0",
            "Referer": "http://webapps.msxiaobing.com/mindreader",
            "X-Requested-With": "XMLHttpRequest",
            "Cookie": "cpid=%s;salt=%s;ARRAffinity=%s;ai_user=%s;cookieid=%s;ai_session_id=%s"
                      % (self.cpid, self.salt, self.ARRAffinity, self.ai_user, self.cookieid, self.ai_session_id)
        }

        return data

    def gan_post_data(self, text_key=0):

        text_map = (
            (0, u'玩'),
            (1, u'开始'),
            (2, u'是'),
            (3, u'否'),
            (4, u'不知道'),
            (5, u'再来一局'),
        )
        data = {"SenderId": self.sender_id, "Content": {"Text": dict(text_map)[text_key], "Image": ""}}
        if text_key == 0:
            data['Content']['Metadata'] = {"Q20H5Enter": "true"}
        return data

    def gan_id(self):
        return ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)
                       for _ in range(5)
                       )

    def gan_ai_user(self):
        ai_user_id = self.gan_id()
        year = str(time.strftime("%Y"))
        month = str(int(time.strftime("%m")))
        day = str(int(time.strftime("%d")))

        expires_time = year + "-" + month + "-" + day + str(time.strftime("T%H:%M:%S.")) + \
                       str(int(str(datetime.utcnow().microsecond)[3:6]) / 1e3)[2:5] + \
                       u'Z'

        self.ai_user = ai_user_id + '|' + expires_time

    def cmd_play(self):
        self.init_client()
        res_parser = self.start()
        while self.dialog_index < 17 and res_parser.get('text'):
            choice_range = ['y', 'n', 'u']
            now_choice = raw_input('Input your answer for yes/no/uncertain? [y/n/u]:').lower()
            if now_choice in choice_range:
                choice_map = (
                    ('y', 2),
                    ('n', 3),
                    ('u', 4),
                )
                self.choice(dict(choice_map).get(now_choice))
            else:
                print 'Please input in the range for y/n/u'


    def gan_ai_session(self):
        """生成session"""
        nowTime = str(int(time.time() * 1000))
        ai_session_id = self.gan_id()
        self.ai_session_id = ai_session_id + '|' + nowTime + '|' + nowTime

    def play(self,is_refresh_cookieid=True):
        url = 'http://webapps.msxiaobing.com/simplechat/getresponse?workflow=Q20'
        res = requests.post(url=url, headers=self.gan_headers(), json=self.gan_post_data())
        if is_refresh_cookieid:
            self.cookieid = res.cookies.get(name='cookieid')
        return self.dialogue_parser(res._content)

    def get_wechat_authorize(self):
        url = 'http://webapps.msxiaobing.com/api/wechatAuthorize/signature?url=http://webapps.msxiaobing.com/MindReader'
        res = requests.get(url=url, headers=self.gan_headers())

    def init_client(self):
        self.dialog_index = 0
        url = 'http://webapps.msxiaobing.com/MindReader'
        res = requests.get(url)
        self.cpid = res.cookies.get(name='cpid')
        self.salt = res.cookies.get(name='salt')
        self.ARRAffinity = res.cookies.get(name='ARRAffinity')
        self.get_wechat_authorize()
        self.gan_ai_session()
        self.gan_ai_user()
        self.play()

    def refresh_client(self):
        self.dialog_index = 0
        url = 'http://webapps.msxiaobing.com/MindReader'
        self.gan_ai_session()
        requests.get(url, headers=self.gan_headers())
        self.get_wechat_authorize()
        self.play(is_refresh_cookieid=False)

    def dialogue_parser(self, return_data):
        soup = BeautifulSoup(return_data, "html.parser")
        json_content = json.loads(soup.find(id='xb_responses')['data-json'])
        data = ''
        image_url = ''

        logging.debug('response_json:' + str(json_content))
        for i in range(len(json_content)):
            text = json_content[i]['Content']['Text']
            data += text if text else ''

            if json_content[i]['Content']['ImageUrl']:
                image_url = re.sub(r'http://', "https://", json_content[i]['Content']['ImageUrl'])

        logging.debug(str(self.dialog_index) + '.Question:' + data)
        question  = {'text': data, 'image': image_url}
        if self.dialog_index>0:
            self.last_question = question
        return question

    def choice(self, decision=2):
        url = 'http://webapps.msxiaobing.com/simplechat/getresponse?workflow=Q20'
        res = requests.post(url=url, headers=self.gan_headers(), json=self.gan_post_data(decision))
        self.dialog_index = self.dialog_index + 1
        return self.dialogue_parser(res._content)

    def start(self):
        self.dialog_index = 0
        url = 'http://webapps.msxiaobing.com/simplechat/getresponse?workflow=Q20'
        res = requests.post(url=url, headers=self.gan_headers(), json=self.gan_post_data(1))
        return self.dialogue_parser(res._content)

    def choice_yes(self):
        return self.choice(decision=2)

    def choice_no(self):
        return self.choice(decision=3)

    def choice_uncertainty(self):
        return self.choice(decision=4)

    def choice_again(self):
        return self.choice(decision=5)

    def get_hot_people(self):
        """获取用户正在猜的,热门人物"""
        pass

    def commit_guess_people(self):
        pass

