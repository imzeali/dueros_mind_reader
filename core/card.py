# -*- coding: utf-8 -*-
# @Time    : 2018/11/24 5:23 PM
# @Author  : zeali
# @Email   : zealiemai@gmail.com
from core.template import gen_token
from dueros.card.ImageCard import ImageCard
from dueros.card.ListCard import ListCard
from dueros.card.ListCardItem import ListCardItem


def gen_image_card(items=[], hints=[]):
    card = ImageCard()
    card.set_token(gen_token())
    for item in items:
        card.add_item(item.get('src'), item.get('thumbnail'))

    card.add_cue_words(hints)
    return card


def gen_list_card(items=[], hints=[]):
    card = ListCard()
    for item in items:
        card_item = ListCardItem()

        card_item.set_title(item.get('title'))
        card_item.set_url(item.get('url'))
        card_item.set_image(item.get('image'))
        card_item.set_content(item.get('content'))

        card.add_item(card_item)

    card.add_cue_words(hints)

    return card
