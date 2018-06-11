from django.shortcuts import render, HttpResponse, redirect, reverse
from django.contrib import auth
from django.http import JsonResponse
from django.db import transaction
from django.db.models import F
import json
import logging

from blog import valid_img
from blog.myforms import RegForm
from blog.models import *

logger = logging.getLogger(__name__)
collect_logger = logging.getLogger('collect')


def login(request):
    """
    登录
    request.session.get('valid_str') 可以得到本次的实时验证码。
    :param request:
    :return:
    """
    if request.is_ajax():
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        valid_code = request.POST.get('valid_code')

        valid_str = request.session.get('valid_str')

        next_url = request.GET.get('next', '/index/')
        res = {"state": False, "msg": None, "next_url": next_url}

        if valid_str.upper() == valid_code.upper():
            user = auth.authenticate(username = user, password = pwd)
            if user:
                res['state'] = True
                auth.login(request, user)

                logger.info(user.username+"登录")

            else:
                res['msg'] = '用户名或密码错误'
        else:
            res['msg'] = '验证码错误'

        return JsonResponse(res)

    return render(request, 'login.html')


def logout(request):
    """
    注销
    :param request:
    :return:
    """
    auth.logout(request)
    return redirect(reverse('login'))


def get_valid_img(request):
    """
    得到验证码的图片
    :param request:
    :return:
    """
    valid_str, data = valid_img.get_valid_img()
    print(valid_str)
    request.session['valid_str'] = valid_str
    return HttpResponse(data)


def reg(request):
    """
    注册
    :param request:
    :return:
    """
    if request.method == 'POST':
        res = {'user': None, 'error_dict': None}
        form = RegForm(request.POST)

        if form.is_valid():
            user = form.cleaned_data.get('user')
            pwd = form.cleaned_data.get('pwd')
            email = form.cleaned_data.get('email')
            avatar = request.FILES.get('avatar')
            if avatar:
                # 接收文件对象，将avatar文件对象下载到avatar字段对应的upload_to指定路径下没指定在根目录下
                user = UserInfo.objects.create_user(username=user, password=pwd, email=email, avatar=avatar)
            else:
                user = UserInfo.objects.create_user(username=user, password=pwd, email=email)

            res['user'] = user.username

            collect_logger.info(user.username+"注册")

        else:
            res['error_dict'] = form.errors

        return JsonResponse(res)

    form = RegForm()
    return render(request, 'reg.html', locals())


def index(request):
    """
    首页
    :param request:
    :return:
    """
    article_list = Article.objects.all()
    return render(request, 'index.html',{"article_list":article_list})


def homesite(request, username, **kwargs):
    """
    个人站点
    :param request:
    :param username: 当前站点的用户名
    :param kwargs: /(?P<condition>tag|cate|archive)/(?P<param>.*) 分类 标签 归档  参数
    :return:
    """
    user = UserInfo.objects.filter(username=username).first()
    if not user:
        return HttpResponse('404')
    # 当前站点对象
    blog = user.blog
    if not kwargs:
        article_list = Article.objects.filter(user=user)
    else:
        condition = kwargs.get('condition')
        param = kwargs.get('param')
        if condition == 'cate':
            article_list = Article.objects.filter(user=user, category__title=param)
        elif condition == 'tag':
            article_list = Article.objects.filter(user=user, tags__title=param)
        else:
            year, month = param.split('-')
            article_list = Article.objects.filter(user=user).filter(create_time__year=year, create_time__month=month)

    return render(request, 'homesite.html', locals())


def article_detail(request, username, article_id):
    """
    文章详细页
    :param request:
    :return:
    """
    user = UserInfo.objects.filter(username=username).first()
    blog = user.blog

    article = Article.objects.filter(pk=article_id).first()

    comment_list = Comment.objects.filter(article_id=article_id)

    return render(request, 'article_detail.html', locals())


def poll(request):
    """
    点赞 踩灭 多条sql，事务。
    :param request:
    :return:
    """
    is_up = json.loads(request.POST.get('is_up'))
    article_id = request.POST.get('article_id')
    user_id = request.user.pk
    res = {'state': True}

    try:
        with transaction.atomic():
            ArticleUpDown.objects.create(is_up=is_up, article_id=article_id, user_id=user_id)
            if is_up:
                Article.objects.filter(pk=article_id).update(up_count=F('up_count')+1)
            else:
                Article.objects.filter(pk=article_id).update(down_count=F('down_count')+1)

    except Exception as e:
        res['state'] = False
        res['first_operate'] = ArticleUpDown.objects.filter(article_id=article_id, user_id=user_id).first().is_up

    return JsonResponse(res)


def comment(request):
    """
    对文章评论
    :param request:
    :return:
    """
    article_id = request.POST.get('article_id')
    content = request.POST.get('content')
    pid = request.POST.get('pid')
    user_id = request.user.pk

    res = {'state': True}

    with transaction.atomic():
        if not pid:  # 提交根评论
            obj = Comment.objects.create(user_id=user_id, article_id=article_id, content=content)
        else:
            obj = Comment.objects.create(user_id=user_id, article_id=article_id, content=content, parent_comment_id=pid)

        Article.objects.filter(pk=article_id).update(comment_count=F("comment_count")+1)

    res['time'] = obj.create_time.strftime('%Y-%m-%d %H:%M')
    res['content'] = obj.content
    if obj.parent_comment_id:
        res['pid'] = obj.parent_comment_id
        res['pidname'] = obj.parent_comment.user.username

    return JsonResponse(res)


def get_comment_tree(request, article_id):
    ret = list(Comment.objects.filter(article_id=article_id).values('pk', 'content', 'parent_comment_id', 'user__username').order_by('nid'))

    return JsonResponse(ret, safe=False)
