#!/usr/bin/env python2
# -*- encoding=utf-8 -*-

# description:
# author:jack
# create_time: 2017/12/30

"""
卡片基类
"""


class BaseCard(object):

    def __init__(self, field=[]):
        self.data = {}
        self.support_set_field = field

    def add_cue_words(self, arr):
        """
		为卡片添加cue words 提示用户输入
		:param arr:
		:return:
		"""
        if arr:
            if isinstance(arr, str):
                arr = [arr]

            if 'cueWords' in self.data:
                self.data['cueWords'] = self.data['cueWords']
            else:
                self.data['cueWords'] = []

            self.data['cueWords'].extend(arr)
        return self

    def set_anchor(self, url, anchor_text):
        """
		设置卡片链接
		:param url: 比如:http(s)://....
		:param anchor_text: 链接显示的文字
		:return:
		"""
        if url:
            self.data['url'] = url
            if (anchor_text):
                self.data['anchorText'] = anchor_text
        return self

    def get_data(self):
        return self.data

    def __getattr__(self, item):
        '''
		添加魔术方法
		:param item:
		:return:
		'''
        # 获取操作类型 set
        operation = item[0:3]
        # 获取被操作的属性
        field = item[4:]
        if operation == 'set' and field and (field.lower() in self.support_set_field):
            def function(*args):
                self.data[field.lower()] = args[0]

            return function
        else:
            def function(*args):
                print('不支持', operation, field)

            return function


if __name__ == '__main__':
    pass
