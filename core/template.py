# -*- coding: utf-8 -*-
# © 2018 WE Technology
# Authored by: Zhi Li (zealiemai@gmail.com)
import hashlib
import random
import time

from dueros.directive.Display.template.BodyTemplate5 import BodyTemplate5

from dueros.directive.Display.template.ListTemplateItem import ListTemplateItem

from dueros.directive.Display.Hint import Hint
from dueros.directive.Display.RenderTemplate import RenderTemplate
from dueros.directive.Display.template.BodyTemplate1 import BodyTemplate1
from dueros.directive.Display.template.BodyTemplate2 import BodyTemplate2
from dueros.directive.Display.template.ListTemplate3 import ListTemplate3
from dueros.directive.Display.template.ListTemplate2 import ListTemplate2


def gen_token():
    '''
    生成Token md5(9位随机数+时间戳) 再截取md5后的字符串
    :return: uuid
    '''
    # 生成随机数
    rand = str(random.randint(0, 9999999999))
    t = str(round(time.time() * 1000))
    md5Str = rand + t
    md5 = hashlib.md5()
    md5.update(md5Str.encode('utf-8'))
    token = md5.hexdigest()
    uuid = token[0:8] + '-'
    uuid = uuid + token[8:12] + '-'
    uuid = uuid + token[12:16] + '-'
    uuid = uuid + token[16:20] + '-'
    uuid = uuid + token[20:]
    return uuid


def gen_text(title, content):
    """生成一个文本展现模板"""

    bodyTemplate = BodyTemplate1()
    bodyTemplate.set_token(gen_token())
    # 设置模版标题
    bodyTemplate.set_title(title)
    # 设置模版plain类型的文本
    bodyTemplate.set_plaintext_content(content)
    # 定义RenderTemplate指令
    return RenderTemplate(bodyTemplate)


def gen_text_image(title, image, content, background=None):
    """生成一个上图下文本展现模板"""

    bodyTemplate = BodyTemplate2()
    # 设置模版token
    bodyTemplate.set_token(gen_token())
    # 设置模版标题
    bodyTemplate.set_title(title)
    # 设置模版plain类型的文本结构
    bodyTemplate.set_plain_content(content)

    # 设置模版展示图片
    bodyTemplate.set_image(url=image)
    # 设置模版背景图片
    if background:
        bodyTemplate.set_background_image(background)
    # 定义RenderTemplate指令
    return RenderTemplate(bodyTemplate)


def gen_template5(title, images, background_image):
    bodyTemplate = BodyTemplate5()
    bodyTemplate.set_token(gen_token())
    bodyTemplate.set_title(title)
    if background_image:
        bodyTemplate.set_background_image(background_image)

    if isinstance(images, list):
        for image in images:
            bodyTemplate.add_images(url=image)
    else:
        bodyTemplate.add_images(url=images)

    return RenderTemplate(bodyTemplate)


def gen_list_template3(title, background_image, items):
    listTemplate3 = ListTemplate3()
    listTemplate3.set_token(gen_token())
    listTemplate3.set_title(title)

    if background_image:
        listTemplate3.set_background_image(background_image)

    for item in items:
        listTemplateItem = ListTemplateItem()
        listTemplateItem.set_token(gen_token())
        listTemplateItem.set_image(item.get('image'))
        listTemplateItem.set_content(item.get('content'))
        listTemplate3.add_item(listTemplateItem)

    return RenderTemplate(listTemplate3)


def gen_list_template2(title, background_image, items):
    listTemplate2 = ListTemplate2()
    listTemplate2.set_token(gen_token())
    listTemplate2.set_title(title)

    if background_image:
        listTemplate2.set_background_image(background_image)

    for item in items:
        listTemplateItem = ListTemplateItem()
        listTemplateItem.set_token(gen_token())
        listTemplateItem.set_image(item.get('image'))
        listTemplateItem.set_plain_primary_text(item.get('primary'))
        listTemplateItem.set_plain_secondary_text(item.get('secondary'))
        listTemplateItem.set_tertiary_text(item.get('tertiary'))
        listTemplate2.add_item(listTemplateItem)

    return RenderTemplate(listTemplate2)


def gen_hint(content):
    return Hint(text=content)


def gen_ssml_background_output_speech(content, background=None, is_repeat=False, first_silence=0, last_silence=0):
    is_repeat = 'yes' if is_repeat else 'no'
    if first_silence > 0:
        first_silence = '<silence time="%ss"></silence>' % (first_silence)
        content = '%s%s' % (first_silence, content)

    if last_silence > 0:
        first_silence = '<silence time="%ss"></silence>' % (last_silence)
        content = '%s%s' % (content, first_silence)

    if background:
        content = '<background src="%s" repeat="%s">%s</background>' % (background, is_repeat, content)

    return '<speak>%s</speak>' % (content)


if __name__ == "__main__":
    print gen_list_template3('title', None, [{"image": "imagexxxx", "content": "contentxxx"}]).get_data()
