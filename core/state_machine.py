# -*- coding: utf-8 -*-
# © 2018 WE Technology
# Authored by: Zhi Li (zealiemai@gmail.com)
from core.template import gen_text, gen_hint
from dueros.Bot import Bot


class StateMachine(Bot):
    status = 0
    state = 'INITIALIZING'
    __intent__ = None
    __states__ = []
    __transitions__ = [
        {
            'intent': 'launch',
            'handler': 'launch_handler'
        },
        {
            'intent': 'ended',
            'handler': 'ended_handler'
        },
    ]

    def __init__(self, data):
        super(StateMachine, self).__init__(data)
        self.status = self.get_session_attribute(field='status', default=0)
        self.state = self.get_session_attribute(field='state', default='INITIALIZING')
        self.__intent_handler_process()

    def launch(self):

        return {
            'outputSpeech': 'hello world!'
        }

    def ended(self):

        return {
            'outputSpeech': 'goodbye world!'
        }

    def intent_map(self, intent):
        maps = {
            'default_intent': 'ai.dueros.common.default_intent'
        }

        return maps.get(intent) if maps.get(intent, False) else intent

    def default_intent(self):
        self.wait_answer()
        current_can_do_intents_name = self.get_current_can_do_intents_name()
        text = u'当前你可对我说的指令有: %s' % (current_can_do_intents_name)

        return {
            'outputSpeech': text,
            'reprompt': text
        }

    def default_intent_handler(self):
        self.__transitions__ = self.__transitions__ + [{
            'intent': 'ai.dueros.common.default_intent',
            'name': u'默认意图',
            'source': '*',
            'dest': '=',
            'hide': True
        }]
        self.add_intent_handler('ai.dueros.common.default_intent', self.default_intent)

    def __intent_handler_process(self):

        for transition in self.__transitions__:
            intent = transition.get('intent')

            if intent == 'launch':
                self.add_launch_handler(getattr(self, intent))

            elif intent == 'ended':
                self.add_session_ended_handler(getattr(self, intent))

            else:
                self.add_intent_handler(intent, getattr(self, intent))

        self.default_intent_handler()

    def before_intent_event_handler(self, event):
        transition = self.get_current_transition()
        if transition:
            before_handler = transition.get('before')
            if before_handler:
                self.call_func(before_handler, event)

    def after_intent_event_handler(self, event):
        transition = self.get_current_transition()
        if transition:
            after_handler = transition.get('after')
            if after_handler:
                self.call_func(after_handler, event)

    def __check_transfer(self, transition):
        current_state = self.state
        source = transition.get('source')
        if isinstance(source, list):
            if current_state in source:
                return True
            else:
                return False
        elif isinstance(source, str):
            if current_state == source or source == '*':
                return True
            else:
                return False
        else:
            return False

    def transfer_state(self, transition=None):
        if transition is None:
            transition = self.get_current_transition()

        if self.__check_transfer(transition):
            dest_state = transition.get('dest')

            if dest_state == '=' and transition.get('source') == '*':
                self.state = self.state
            elif dest_state == '=':
                self.state = transition.get('source')
            else:
                self.state = transition.get('dest')

            self.status = self.get_status_by_state(self.state)
            self.set_session_attribute('state', self.state, None)
            self.set_session_attribute('status', self.status, None)
        else:
            if self.__intent__ != self.default_intent.__name__:
                self.wait_answer()
                current_can_do_intents_name = self.get_current_can_do_intents_name()
                text = u'你现在还无法 %s,你可以试着对我说:%s' % (transition['name'], current_can_do_intents_name)
                return {
                    'outputSpeech': text,
                    'reprompt': text
                }
            else:
                return False

    def intent_event_handler(self, ret, event_handler):
        if not ret:
            if event_handler:

                self.__intent__ = event_handler.__name__

                self.botMonitor.set_device_event_start()
                event = self.request.get_event_data()

                self.before_intent_event_handler(event)

                ret = self.call_func(event_handler, event)
                self.after_intent_event_handler(event)

                self.botMonitor.set_device_event_end()

            else:

                self.botMonitor.set_event_start()
                event_handler = self.dispatch()
                self.__intent__ = event_handler.__name__

                self.before_intent_event_handler(None)

                ret = self.transfer_state()

                if not ret:
                    ret = self.call_func(event_handler, None)

                self.after_intent_event_handler(None)

                self.botMonitor.set_event_end()

            if ret:
                if not self.is_support_display():
                    return {
                        'outputSpeech': ret.get('outputSpeech'),
                        'reprompt': ret.get('reprompt'),
                    }

                return ret

    def get_current_transition(self):
        for transition in self.__transitions__:
            if transition.get('intent') == self.intent_map(self.__intent__):
                return transition

    def get_status_by_state(self, state):
        for k, v in dict(self.__states__).items():
            if v == state:
                return k

    def get_transition_by_intent(self, intent):
        for transition in self.__transitions__:
            if transition.get('intent') == intent:
                return transition

    def get_current_can_do_intents_transition(self):
        can_do_transitions = []
        for transition in self.__transitions__:
            source = transition.get('source')
            if isinstance(source, list):
                if self.state in source:
                    can_do_transitions.append(transition)
            else:
                if self.state == source or source == '*':
                    can_do_transitions.append(transition)

        return can_do_transitions

    def get_current_can_do_intents_name(self):
        current_can_do_intents_name = ''
        for this_transition in self.get_current_can_do_intents_transition():
            if this_transition.get('hide') is not True:
                current_can_do_intents_name += (this_transition.get('name')) + u'、'
        return current_can_do_intents_name[:-1]
