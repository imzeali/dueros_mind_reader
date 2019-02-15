# -*- coding: utf-8 -*-
# © 2018 WE Technology
# Authored by: Zhi Li (zealiemai@gmail.com)
from dueros.Utils import gen_token
from dueros.card.ImageCard import ImageCard
from dueros.directive.Display.Hint import Hint
from dueros.directive.Display.RenderTemplate import RenderTemplate
from dueros.directive.Display.tag.CustomTag import CustomTag
from dueros.directive.Display.template.BodyTemplate1 import BodyTemplate1
from dueros.directive.Display.template.BodyTemplate2 import BodyTemplate2
from dueros.directive.Display.template.BodyTemplate5 import BodyTemplate5
from dueros.directive.Display.template.ListTemplate1 import ListTemplate1
from dueros.directive.Display.template.ListTemplate2 import ListTemplate2
from dueros.directive.Display.template.ListTemplateItem import ListTemplateItem


def launch_schema():
    src = 'http://dbp-resource.gz.bcebos.com/8a4c3c25-b6a7-d08d-8cf8-35a0f5fb6bc7/launch.gif?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2019-01-10T11%3A02%3A06Z%2F-1%2F%2F3ce83ebad84c05d69b5137095f692efd39542c408eceef2e342be286d7decfda'
    bodyTemplate = BodyTemplate5()
    bodyTemplate.set_token(gen_token())
    bodyTemplate.set_title(u' ')
    bodyTemplate.set_background_image(src)
    bodyTemplate.add_images(url=src)
    return RenderTemplate(bodyTemplate)


def question_schema(title, image, content, background=None):
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
