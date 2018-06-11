# -*- coding:utf-8 -*-
from django.urls import path, re_path

from blog import views

urlpatterns = [
    # 评论
    path('comment/', views.comment),
    # 评论树
    re_path('get_comment_tree/(\d+)', views.get_comment_tree),

    # 点赞 踩灭
    path('poll/',views.poll),

    # 文章详细页
    re_path(r'(?P<username>\w+)/articles/(?P<article_id>\d+)/$', views.article_detail),

    # 个人站点
    re_path(r'(?P<username>\w+)/(?P<condition>tag|cate|archive)/(?P<param>.*)', views.homesite),
    re_path(r'(?P<username>\w+)/$', views.homesite)
]