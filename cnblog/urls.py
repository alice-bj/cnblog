"""cnblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve

from cnblog import settings
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('reg/', views.reg),
    path('login/', views.login, name='login'),
    path('logout/', views.logout),
    path('get_valid_img/', views.get_valid_img),

    path('index/', views.index),
    re_path(r'^$', views.index),

    re_path(r'blog/', include(('blog.urls', 'blog'))),

    re_path(r'backend/', include(('backend.urls', 'backend'))),

    # media配置
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

]
