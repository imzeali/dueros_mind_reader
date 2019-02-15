# -*- coding: utf-8 -*-
# © 2018 WE Technology
# Authored by: Zhi Li (zealiemai@gmail.com)
import json
import logging
from pprint import pprint

from index import SkillBot


class Testing(object):
    __session__ = {

    }
    __test_event_queue__ = [

    ]
    __bot__ = None

    private_key = '''-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQC9K7Dxf9lUsqud7Ecx6cNLPjWLBywoLlkXrK2ZlNvsV92+egw+
4ut8//48u0WL7IcAyKSW/aJgUdq9zHWB0FffchNb9JJlbsg+WrlOY5jwDL5PsE6L
5dh+PfytH236cGOH5uwG0IltZZO9m2+H5chCwd/zhju6w7eRkP8je/UtBQIDAQAB
AoGATOGT4SJvpk+TFfSwHqX9u/fFdQJuPMpRZSDF0RRBqTUwprgdf/VjdYLoxa/q
nOp9F6Fz2vWr52988gRFgYO2IiLKICtXgPpSCkSNNoLCgTjT9dJC6rGq4AVjvP6g
ua2K1r7bizWg6zdnU0OAcSUW1q4NTyhkxhEut5LG6eRaf0UCQQD2bdl2CdKjY8Om
VKvQ8zw3ZU5pZgeylVMcMHrMxQLkd/KoFPQPMnKHOMQJ/8TCoWjPKZMLgLYB0YyS
au/4FPlrAkEAxISLAWfX7lvQU7n72oCGlGRZjkGdWQKyt7p4LNUKv2Jn+BGJ8djr
C4sEEzZz6jk4ktHG6T5EgqXbJrYkbqjfTwJAHqYk8Mhh+U5ULCDFydQmviEMcpFt
DaoCzzO8YjFynaXJeVw5ypYUpnrJ7xBvkWFv3qwmDL0yZeGBIUjJlcpOBwJBAIvs
L6ldjfLKbsfeqcOHNcucs+NFNsq00BlfbMfHHPLuF0ca/dQ0dg7u+YTQhbIk8fIf
6XgTfOZlP2gN0lz0YqMCQG9y2uKgyNt1weu8v7IA4iHai3VQjgzBiNiF5/y16ibD
jaADJq4TiOzxPDB/HYXN8GBOEPLUsfYJVTk5Dg4cFQg=
-----END RSA PRIVATE KEY-----'''

    def __init__(self, bot, test_event_queue):
        self.__bot__ = bot
        self.__test_event_queue__ = test_event_queue

    def build_intent_request(self, event):
        with open('./data.json', 'r') as load_f:
            data = json.loads(load_f.read())
            load_f.close()
            if event == 'LaunchRequest':
                data['request']['type'] = event
                data['session']['new'] = 'true'
            else:
                data['session']['new'] = 'false'
                data['request']['type'] = 'IntentRequest'

                intent_name = event
                slots = {}
                intents = [
                    {
                        "name": intent_name,
                        "score": 100,
                        "confirmationStatus": "NONE",
                        "slots": slots
                    }
                ]

                if isinstance(event, dict):
                    intents = event['intents']

                data['request']['intents'] = intents

            data['session'] = self.__session__
            return data

    def set_session_by_bot_result(self, bot_result):
        dict_result = json.loads(bot_result)
        if dict_result['response']['shouldEndSession'] == False:
            self.__session__ = json.loads(bot_result)['session']

    def run(self):
        for event in self.__test_event_queue__:
            context = self.build_intent_request(event)
            logging.info('REQUEST:%s' % context)
            bot = self.__bot__(context)
            bot.set_private_key(self.private_key)
            result = bot.run()
            self.set_session_by_bot_result(result)
            logging.getLogger().setLevel(logging.INFO)
            logging.info('RESPONSE:%s' % result)


if __name__ == "__main__":
    testing_queue = [
        'LaunchRequest',
        # {"intents": [
        #     {
        #         "name": "ai.dueros.common.default_intent",
        #         "confirmationStatus": "NONE",
        #         "slots": []
        #     }
        # ]},
        {"intents": [
            {
                "name": "start",
                "confirmationStatus": "NONE",
                "slots": {
                }
            }
        ]},
        {"intents": [
            {
                "name": "yes",
                "confirmationStatus": "NONE",
                "slots": {
                }
            }
        ]},
        {"intents": [
            {
                "name": "replay",
                "confirmationStatus": "NONE",
                "slots": {
                }
            }
        ]},
        # {"intents": [
        #     {
        #         "name": "click_points",
        #         "confirmationStatus": "NONE",
        #         "slots": {
        #             "sys.number": {
        #                 "name": "sys.number",
        #                 "value": "100",
        #                 "values": [
        #                     "100"
        #                 ],
        #                 "confirmationStatus": "NONE"
        #             },
        #             "action": {
        #                 "values": [
        #                     "打开"
        #                 ],
        #                 "name": "action",
        #                 "value": "打开",
        #                 "confirmationStatus": "NONE"
        #             },
        #         }
        #     }
        # ]},
        # {"intents": [
        #     {
        #         "name": "click_points",
        #         "confirmationStatus": "NONE",
        #         "slots": {
        #             "sys.number": {
        #                 "name": "sys.number",
        #                 "value": "44",
        #                 "values": [
        #                     "44"
        #                 ],
        #                 "confirmationStatus": "NONE"
        #             },
        #             "action": {
        #                 "values": [
        #                     "标记"
        #                 ],
        #                 "name": "action",
        #                 "value": "标记",
        #                 "confirmationStatus": "NONE"
        #             },
        #         }
        #     }
        # ]},
        # 'next_checkpoint',

    ]
    testing = Testing(SkillBot, testing_queue)
    testing.run()
