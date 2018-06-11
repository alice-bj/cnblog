# -*- coding:utf-8 -*-
from django import template
from django.db.models import Count

from blog.models import *

register = template.Library()


@register.inclusion_tag('menu.html')
def get_menu(username):
    """
    获取个人站点 (分类 标签 归档)的list以及数量（分组）；最后inclusion_tag 渲染 menu.html
    :param username: 当前站点用户名称
    :return:
    """
    user = UserInfo.objects.filter(username=username).first()
    blog = user.blog

    # 每一个分类以及对应的文章数
    cate_list = Category.objects.filter(blog=blog).annotate(count = Count('article')).values('title', 'count')

    # 每一个标签以及对应的文章数
    tag_list = Tag.objects.filter(blog=blog).annotate(count = Count('article')).values_list('title', 'count')

    # 归档，单表分组 extra插入sql语句
    date_list = Article.objects.filter(user=user).extra(select={"create_ym": "DATE_FORMAT(create_time,'%%Y-%%m')"}).values(
        'create_ym').annotate(c = Count('nid')).values_list('create_ym', 'c')

    return {'username': username, 'cate_list': cate_list, 'tag_list': tag_list, 'date_list': date_list}
