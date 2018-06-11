# -*- coding:utf-8 -*-
from django.urls import path, re_path

from backend import views

urlpatterns = [

    re_path(r'^$', views.index),
    path('index/', views.index, name='index'),

    # 添加文章
    path('add_article/', views.add_article),

    # 上传文件
    re_path(r'upload_img/', views.upload_img)
]