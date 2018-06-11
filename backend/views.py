from django.shortcuts import render, HttpResponse, redirect, reverse
from django.db import transaction
from django.contrib.auth.decorators import login_required
import os
import json

from bs4 import BeautifulSoup

from cnblog import settings
from blog.models import *
from blog.views import logger


@login_required
def index(request):
    """
    后台文章列表页
    :param request:
    :return:
    """
    article_list = Article.objects.filter(user=request.user).values('nid', 'title', 'create_time')
    return render(request, 'backend.html', {'article_list': article_list})


@login_required
def add_article(request):
    """
    发布文章 利用BeautifulSoup可以对script标签过滤，对网页解析数据。
    :param request:
    :return:
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        title = title if title else "默认标题"

        article_con = request.POST.get('article_con')

        soup = BeautifulSoup(article_con, 'html.parser')

        # 过滤script, 删除了所有的script标签
        for tag in soup.find_all():
            if tag.name == 'script':
                tag.decompose()

        # 摘要 截取150个字符，防止含有这样的文本<script>alert(555)</script> 需转化成 &lt;script&gt;alert(555)&lt;/script&gt;
        desc = soup.text[0:150].replace('<', '&lt;').replace('>', '&gt')

        with transaction.atomic():
            article_obj = Article.objects.create(title=title, desc=desc, user=request.user)
            # soup.prettify() == str(soup)
            ArticleDetail.objects.create(content=soup.prettify(), article=article_obj)

        logger.info(request.user.username+"发布了一篇文章("+title+")")

        return redirect(reverse('backend:index'))

    else:
        return render(request, 'add_article.html')


@login_required
def upload_img(request):
    """
    发布文章时， 携带图片的处理。
    :param request:
    :return:
    """
    img_obj = request.FILES.get('img')

    media_path = settings.MEDIA_ROOT
    path = os.path.join(media_path, 'article_imgs', img_obj.name)

    with open(path, 'wb') as f:
        for line in img_obj:
            f.write(line)

    res = {
        "url": "/media/article_imgs/"+img_obj.name,
        "error": 0
    }

    return HttpResponse(json.dumps(res))
