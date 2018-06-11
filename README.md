### BBS+BLOG系统
#### 一、简介：
1. 博客系统开发：
1. 注册，登录，首页
1. 个人站点，分组：（分类，标签，归档）
1. 文章详细页
1. 点赞，踩灭
1. 评论楼，评论树
1. 后台管理，发布文章，文件上传
1. BeautifulSoup
1. 日志

#### 二、功能：
  
```
数据库          models.py

注册            /reg/
    上传头像    request.FILES.get('avatar')

登录            /login/
    随机验证码  /get_valid_img/

首页            /index/

个人站点
    分类，标签，归档 /blog/egon/

文章详细页       /blog/egon/articles/2/

点赞，踩灭       /blog/poll/
    ajax的post 事务

评论楼，评论树   /blog/comment/
    根评论，子评论
    render显示，ajax显示

后台管理，发布文章  /backend/index/
    新建APP
    认证装饰器
    编辑器（KindEditor）
    文件上传      /media/article_imgs/...

防止XSS攻击
    BeautifulSoup
```

#### 三、结构

```
cnblog
├── backend
│   ├── static
│   │   ├── css
│   │   │   ├── backend.css
│   │   ├── js
│   │   │   ├── add_article.js
│   │   │   ├── jquery-3.2.1.js
│   │   │   └── jquery-3.2.1.min.js
│   │   └── kindeditor
│   │       ├── kindeditor-all.js
│   │       ├── kindeditor-all-min.js
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── blog
│   ├── admin.py
│   ├── apps.py
│   ├── media
│   │   ├── article_imgs
│   │   │   ├── girl.jpg
│   │   │   ├── jiqimao.gif
│   │   │   ├── jiqimao.jpg
│   │   │   └── lufei.jpg
│   │   ├── avatars
│   │   │   ├── girl.jpg
│   │   │   ├── lufei.jpg
│   ├── models.py
│   ├── myforms.py
│   ├── settings.py
│   ├── static
│   │   ├── bootstrap-3.3.7
│   │   │   ├── css
│   │   │   │   ├── bootstrap.css
│   │   │   ├── fonts
│   │   │   └── js
│   │   │       ├── bootstrap.js
│   │   │       ├── bootstrap.min.js
│   │   ├── css
│   │   │   ├── article_detail.css
│   │   │   ├── login.css
│   │   │   └── reg.css
│   │   ├── font
│   │   │   └── kumo.ttf
│   │   ├── img
│   │   │   ├── default.png
│   │   │   ├── downdown.gif
│   │   │   ├── icon_form.gif
│   │   │   └── upup.gif
│   │   ├── js
│   │   │   ├── article_detail.js
│   │   │   ├── jquery-3.2.1.js
│   │   │   ├── jquery-3.2.1.min.js
│   │   │   ├── login.js
│   │   │   └── reg.js
│   │   └── theme
│   │       ├── egon.css
│   │       └── yuan.css
│   ├── templatetags
│   │   ├── my_tags.py
│   ├── tests.py
│   ├── urls.py
│   ├── valid_img.py
│   └── views.py
├── cnblog
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── log
│   ├── cnblog_collect.log
│   ├── cnblog_err.log
│   ├── cnblog_info.log
├── manage.py
└── templates
    ├── add_article.html
    ├── article_detail.html
    ├── backend.html
    ├── base.html
    ├── homesite.html
    ├── index.html
    ├── login.html
    ├── menu.html
    └── reg.html
```

#### 四、账号：
   
```
egon egon1234 
yuan yuan1234 
alex alex1234
```
