# -*- coding: utf-8 -*-
# © 2018 WE Technology
# Authored by: Zhi Li (zealiemai@gmail.com)
import logging

from dueros.Intercept import Intercept


class CoreIntercept(Intercept):
    def preprocess(self, bot):
        '''

        :param bot:
        :return:
        如果返回非null，跳过后面addHandler，addEventListener添加的回调
        '''
        pass

    def postprocess(self, bot, result):
        '''
        在调用response->build 之前统一对handler的输出结果进行修改
        :param bot:
        :param result:  []
        :return:[]
        '''
        # result = bot.return_data()
        return  result
