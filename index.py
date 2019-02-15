#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import logging
import sys
import random

from core.bot import CoreBot
from dueros.directive.Display.Hint import Hint
from game.models import MindReader
from game.schemas import question_schema, launch_schema

logging.getLogger().setLevel(logging.INFO)

reload(sys)
sys.setdefaultencoding('utf8')


class SkillBot(CoreBot):
    image_gif = [
        'http://dbp-resource.gz.bcebos.com/8a4c3c25-b6a7-d08d-8cf8-35a0f5fb6bc7/rOnmrxKcKqKeAv4LoEPurncB42lLLwrs.gif_s400x0.gif?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-07-26T12%3A57%3A15Z%2F-1%2F%2F56fed725570b95ae58bacd5e08ad3e17f1fa26db35b9db6e6a9156b9ed1b6a3c',
        'http://dbp-resource.gz.bcebos.com/8a4c3c25-b6a7-d08d-8cf8-35a0f5fb6bc7/9dFbkaQK9NQVOlOaPfDnZMhxGWKrGAo4.gif_s400x0.gif?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-07-26T12%3A55%3A55Z%2F-1%2F%2F143f126fa4dd5d2d78236da56b1d2ea8e409209189d3d416b8b5d4cf4cf88171',
        'http://dbp-resource.gz.bcebos.com/8a4c3c25-b6a7-d08d-8cf8-35a0f5fb6bc7/XwszqFd4oLReJJpp6RHA4W4MnXVno9w8.gif_s400x0.gif?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-07-26T12%3A55%3A55Z%2F-1%2F%2F5b1270b7e1d05e268d357bc6ecf2f26edcfe6b43e395ad3bba3447824a2b74d2',
        'http://dbp-resource.gz.bcebos.com/8a4c3c25-b6a7-d08d-8cf8-35a0f5fb6bc7/3X7AisL6nsyd51raysns8F7IsfHiVpki.gif_s400x0.gif?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-07-26T12%3A55%3A55Z%2F-1%2F%2F75346f195f27dfbe093f3173718d7e3200ab5d264c3b105ae40c2aac16bd8ac8',
        'http://dbp-resource.gz.bcebos.com/8a4c3c25-b6a7-d08d-8cf8-35a0f5fb6bc7/xmKrBW06k7M6XrWx8xs8zzJZfBxrKrln.gif_s400x0.gif?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-07-26T12%3A55%3A55Z%2F-1%2F%2F5bb142cc379fe467ccc1192e65418164d6168801518346e9666822a71816ad06',
        'http://dbp-resource.gz.bcebos.com/8a4c3c25-b6a7-d08d-8cf8-35a0f5fb6bc7/aZ3S6062oc3KLBfm0S3hh6BwgGgwgGg7.gif?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-10-27T14%3A06%3A21Z%2F-1%2F%2F38e2fddadac451b1c5d2f3b92fa26ee7cd2410e75b08c0ab5d81f6b1a7043968',
        'http://dbp-resource.gz.bcebos.com/8a4c3c25-b6a7-d08d-8cf8-35a0f5fb6bc7/dFziRdNHuvUg67Zq7mkcBBPSEkXChg31.gif?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-10-27T14%3A06%3A56Z%2F-1%2F%2Fdfd6d4036a8591e4f2212ae1204f1662f7a79d007afe0161077e5d04770142b3',
        'http://dbp-resource.gz.bcebos.com/8a4c3c25-b6a7-d08d-8cf8-35a0f5fb6bc7/reErKLc6wIN7joH2DzNj0hPTFkapPerg.gif?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-10-27T14%3A07%3A34Z%2F-1%2F%2Fdb2d1cbb94645772ae2d533395be7aa51a523df0a131c398844ab73f7cbb70fd',
        'http://dbp-resource.gz.bcebos.com/8a4c3c25-b6a7-d08d-8cf8-35a0f5fb6bc7/iUP1tvR9r5mq5nmM5Pv9IcLfOA3CjNnU.gif?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-10-27T14%3A08%3A03Z%2F-1%2F%2F437387c14b04e5182ca75d14024b72e8bbaeabe8548685ff0a0aae2b17bee585',
        'http://dbp-resource.gz.bcebos.com/8a4c3c25-b6a7-d08d-8cf8-35a0f5fb6bc7/MYciKNMNn6VDgQZ8lANwN2TL4twSFAvu.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-10-27T14%3A08%3A36Z%2F-1%2F%2F72f24c3cc2171ede74e6e7024692920318d20e1b8bd9613ca10340617d85c4b0',
        'http://dbp-resource.gz.bcebos.com/8a4c3c25-b6a7-d08d-8cf8-35a0f5fb6bc7/e4425e2cb1304985c146b91c9c5b002d.gif?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-10-29T14%3A00%3A47Z%2F-1%2F%2F172ac4b13101ee1a81114b51a1ccd0ecf56b55b0a554757af8c216bb08bd3075',
        'http://dbp-resource.gz.bcebos.com/8a4c3c25-b6a7-d08d-8cf8-35a0f5fb6bc7/f712e8b132430ddc7454183e60d5c553.gif?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-10-29T14%3A00%3A47Z%2F-1%2F%2F5e5985f881ac5832f9ef4d265f75fdeb2a043499a0c23d8ca52b59914256a445',
        'http://dbp-resource.gz.bcebos.com/8a4c3c25-b6a7-d08d-8cf8-35a0f5fb6bc7/1bd2ce4ad7d1bccb64007f66854f2a0a.gif?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-10-29T14%3A00%3A47Z%2F-1%2F%2Fb1f4e282493d16b42e3cbe04b7ab2bb75b090236e212fae2400bd909e33db644',
        'http://dbp-resource.gz.bcebos.com/8a4c3c25-b6a7-d08d-8cf8-35a0f5fb6bc7/8897b04c926db19535a0c1d52ee46648.gif?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-10-29T14%3A00%3A47Z%2F-1%2F%2F3fb42034306e839303fb5cb805840885bc4020a34986c1b246101e4e89e1006b',
        'http://dbp-resource.gz.bcebos.com/8a4c3c25-b6a7-d08d-8cf8-35a0f5fb6bc7/31e98edc6f9e319bed7b40f752e9b907.gif?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-10-29T14%3A00%3A47Z%2F-1%2F%2F66b0507e5d7b3fee2a415b65cbe93a80a20b71bc2083308aecf21038f7664115'

    ]
    __states__ = [
        (-1000, 'CLOSED'),
        (0, 'INITIALIZING'),
        (100, 'LAUNCH'),  # 已唤醒
        (200, 'PLAYING'),  # 游戏中
        (1000, 'FINISH'),  # 完成
    ]
    __transitions__ = [
        {
            'intent': 'launch',
            'name': u'打开技能',
            'source': 'INITIALIZING',
            'dest': 'LAUNCH',
        },
        {
            'intent': 'start',
            'name': u'开始游戏',
            'source': 'LAUNCH',
            'dest': 'PLAYING'
        },
        {
            'intent': 'yes',
            'name': u'是的',
            'source': 'PLAYING',
            'dest': '='
        },
        {
            'intent': 'no',
            'name': u'不是',
            'source': 'PLAYING',
            'dest': '='
        },
        {
            'intent': 'uncertainty',
            'name': u'不知道',
            'source': 'PLAYING',
            'dest': '='
        },
        {
            'intent': 'again',
            'name': u'重新开始',
            'source': '*',
            'dest': 'PLAYING'
        },
        {
            'intent': 'replay',
            'name': u'重播问题',
            'source': 'PLAYING',
            'dest': '='
        },
        {
            'intent': 'ended',
            'handler': 'ended_handler'
        },

    ]

    def __init__(self, data):
        super(CoreBot, self).__init__(data)

    def init_game(self):
        ai_user = self.get_session_attribute('ai_user', '')
        ai_session_id = self.get_session_attribute('ai_session_id', '')
        sender_id = self.get_session_attribute('sender_id', '')
        cookieid = self.get_session_attribute('cookieid', '')
        dialog_index = self.get_session_attribute('dialog_index', -1)
        last_question = self.get_session_attribute('last_question',{})
        self.game = MindReader(ai_user, ai_session_id, sender_id, cookieid, dialog_index,last_question)

    def commit_game(self):
        self.set_session('ai_user', self.game.ai_user)
        self.set_session('ai_session_id', self.game.ai_session_id)
        self.set_session('sender_id', self.game.sender_id)
        self.set_session('cookieid', self.game.cookieid)
        self.set_session('dialog_index', self.game.dialog_index)
        self.set_session('last_question', self.game.last_question)

    def clear_game_session(self):
        self.del_session('ai_user')
        self.del_session('ai_session_id')
        self.del_session('sender_id')
        self.del_session('cookieid')
        self.del_session('dialog_index')
        self.del_session('last_question')

    def launch(self):
        self.wait_answer()
        self.init_game()
        text = u'读心术封印已被开启，首先请你心里默想一位名人、古人、家人或动漫人物，然后回答我15个问题，我就能猜到你想的是谁。现在请对我说 开始游戏!'
        self.commit_game()
        return {
            'directives': [launch_schema(), Hint('开始游戏')],
            'outputSpeech': text,
            'reprompt': u'读心术已经准备好了，快对我说：开始游戏 呢'
        }

    def gen_directives(self, title, data={}):
        text = data.get('text', '')
        image = data.get('image', '')

        # 根据状态给予响应的指令提示 和 修饰表述
        if self.game.dialog_index >= 0:
            if self.game.dialog_index >= 15:
                hint = Hint('再猜一次')
                modify_text = u'现在可以对我说：再猜一次，我们重新开始呢'
            else:
                hint = Hint('是/不是/不知道')
                modify_text = u'我没理解你的回答，请回答我是、不是或不知道呢'
        else:
            hint = Hint('开始游戏')
            modify_text = u'我已经准备好了，快对我说：开始游戏 呢'

        if text == '':
            text = modify_text

        if not image:
            image = self.image_gif[random.randint(0, 14)]

        template = question_schema(title=title, image=image, content=text)

        return [template, hint]

    def start(self):
        self.wait_answer()
        self.init_game()
        data = self.game.start()
        self.commit_game()
        directives = self.gen_directives(title=u'请回答', data=data)
        return {
            'directives': directives,
            'outputSpeech': data.get('text'),
            'reprompt': u'请回答我是、不是或不知道呢'
        }

    def yes(self):
        self.wait_answer()
        self.init_game()
        data = self.game.choice_yes()
        self.commit_game()
        directives = self.gen_directives(title=u'请回答', data=data)
        return {
            'directives': directives,
            'outputSpeech': data.get('text'),
            'reprompt': u'请回答我是、不是或不知道呢'
        }

    def no(self):
        self.wait_answer()
        self.init_game()
        data = self.game.choice_no()
        self.commit_game()
        directives = self.gen_directives(title=u'请回答', data=data)
        return {
            'directives': directives,
            'outputSpeech': data.get('text'),
            'reprompt': u'请回答我是、不是或不知道呢'
        }

    def uncertainty(self):
        self.wait_answer()
        self.init_game()
        data = self.game.choice_uncertainty()
        self.commit_game()
        directives = self.gen_directives(title=u'请回答', data=data)
        return {
            'directives': directives,
            'outputSpeech': data.get('text'),
            'reprompt': u'请回答我是、不是或不知道呢'
        }
    def replay(self):
        self.wait_answer()
        self.init_game()
        self.get_session('')
        data = self.game.last_question
        directives = self.gen_directives(title=u'请回答', data=data)
        return {
            'directives': directives,
            'outputSpeech': data.get('text'),
            'reprompt': u'请回答我是、不是或不知道呢'
        }

    def again(self):

        self.wait_answer()
        self.init_game()
        self.game.refresh_client()
        self.commit_game()

        data = self.game.start()
        self.commit_game()

        directives = self.gen_directives(title=u'请回答', data=data)
        return {
            'directives': directives,
            'outputSpeech': u'好的,现在我们重新开始了,%s' % (data.get('text')),
            'reprompt': u'请回答我是、不是或不知道呢'
        }


priKey = '''-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQC9K7Dxf9lUsqud7Ecx6cNLPjWLBywoLlkXrK2ZlNvsV92+egw+
4ut8//48u0WL7IcAyKSW/aJgUdq9zHWB0FffchNb9JJlbsg+WrlOY5jwDL5PsE6L
5dh+PfytH236cGOHe5uwG0IltZZO9m2+H5chCwd/zhju6w7eRkP8je/UtBQIDAQAB
AoGATOGT4SJvpk+TFfSwHqX9u/fFdQJuPMpRZSDF0RRBqTUwprgdf/VjdYLoxa/q
nOp9F6Fz2vWr52988gRFgYO2IiLKICtXgsPpSCkSNNoLCgTjT9dJC6rGq4AVjvP6g
ua2K1r7bizWg6zdnU0OAcSUW1q4NTyhkxhEut5LG6eRaf0UCQQD2bdl2CdKjY8Om
VKvQ8zw3ZU5pZgeylVMcMHrMxQLkd/KoFPQPMnKHOMQJ/8TCoWjPKZMLgLYB0YyS
au/4FPlrAkEAxISLAWfX7lvQU7n72oCGlGRZjkGdWQKyt7p4LNUKv2Jn+BGJ8djr
C4sEEzZz6jk4ktHG6T5EgqXbJrYkbqjfTwJAHqYk8Mhh+U5ULCDFydQmviEMcpFt
DaoCzzO8YjFynaXJeVw5ypYUXXXpnrJ7xBvkWFv3qwmDL0yZeGBIUjJlcpOBwJBAIvs
L6ldjfLKbsfeqcOHNcucs+NFNsq00BlfbMfHHPLuF0ca/dQ0dg7u+YTQhbIk8fIf
6XgTfOZlP2gN0lz0YqMCQG9y2uKgyNt1weu8v7IA4iHai3VQjgzBiNiF5/y16ibD
jaADJq4TiOzxPDB/HYXN8GBOEPLUsfYJVTk5Dg4cFQg=
-----END RSA PRIVATE KEY-----'''


def handler(event, context):
    # logging.info('REQUEST:%s' % event)
    bot = SkillBot(event)
    bot.set_private_key(priKey)
    result = bot.run()
    # logging.info('RESPONSE:%s' % event)
    return result
