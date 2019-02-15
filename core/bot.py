# -*- coding: utf-8 -*-
# © 2018 WE Technology
# Authored by: Zhi Li (zealiemai@gmail.com)
import logging

from core.state_machine import StateMachine


class CoreBot(StateMachine):

    def __init__(self, data):
        logging.info(data)
        super(CoreBot, self).__init__(data)

    # def get_output_speech_from_directives(self, directives):
    #
    #     text_content = directives[0].data.get('template').get('textContent')
    #     content = directives[0].data.get('template').get('content')
    #     title = directives[0].data.get('template').get('title')
    #     outputSpeech = directives[0].outputSpeech
    #
    #     if outputSpeech:
    #         return outputSpeech
    #
    #     elif text_content:
    #         return text_content.get('text').get('text')
    #     elif content:
    #         return content.get('text')
    #     elif title:
    #         return title
    #
    # def return_data(self):
    #     speech_text = self.get_output_speech_from_directives(self.directives)
    #     print speech_text
    #     if self.is_support_display():
    #         return {
    #             'directives': self.directives,
    #             'outputSpeech': speech_text,
    #             'reprompt': speech_text
    #         }
    #     else:
    #         return {
    #             'outputSpeech': speech_text,
    #             'reprompt': speech_text
    #         }

    def set_session(self, key, value):
        return self.set_session_attribute(field=key, value=value, default=None)

    def get_session(self, key):
        return self.get_session_attribute(field=key, default=None)

    def del_session(self, key):
        return self.del_session_attribute(field=key)

    def clear_session(self):
        return self.clear_session_attribute()
