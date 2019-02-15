# -*- coding: utf-8 -*-
# @Time    : 2018/7/11 下午8:46
# @Author  : zeali
# @Email   : zealiemai@gmail.com
import logging

from flask import request, jsonify, Blueprint

import config

class CoreApi(object):
    name = 'api'
    version = config.version
    bot = None
    verify_sign = False
    statistical = False
    methods = ['POST', 'HEAD', 'GET']
    path = '/'

    def __init__(self):
        pass

    @classmethod
    def get_private_key(cls):

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
        return private_key

    @classmethod
    def get_bot(cls, data):
        return cls.bot(data)

    @classmethod
    def index(cls):
        if request.data:
            # print request.data
            bot = cls.get_bot(request.data)

            # 验证签名
            if cls.verify_sign:
                bot.init_certificate(request.environ, cls.get_private_key()).enable_verify_request_sign()
            else:
                bot.init_certificate(request.environ).disable_verify_request_sign()

            #开启数据统计
            if cls.statistical:
                bot.botMonitor.set_monitor_enabled(True)
                bot.botMonitor.set_environment_info(cls.get_private_key(),0)

            # 日志
            bot.set_callback(cls.callback)
            data =  bot.run()
            # print '-'*30
            # print data
            # print '=' * 30
            return data

        else:
            return jsonify({})

    @classmethod
    def callback(cls, data):
        logging.info(data)

    @classmethod
    def register_to(cls, app):
        blueprint = Blueprint(cls.name, __name__, url_prefix='/%s/%s' % (cls.name, cls.version))
        blueprint.add_url_rule(cls.path, endpoint=cls.index.__name__, view_func=cls.index, methods=cls.methods)
        app.register_blueprint(blueprint)
