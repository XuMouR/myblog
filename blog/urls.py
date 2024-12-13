# -*- coding: UTF-8 -*-
'''
=================================================
@Project -> File   ：myblog -> urls.py
@IDE    ：PyCharm
@Author ：XuMou
@Date   ：2020/7/6 16:21
==================================================
'''

from django.urls import path, re_path
from blog import views
from django.views.static import serve
from myblog import settings

urlpatterns = [
    path("", views.index),
    path("login/", views.login),
    path("index/", views.index),
    re_path('^$', views.index),  #
    path("register/", views.register),
    # 修改密码
    path('change_pwd/', views.change_pwd),

    # 账户注销
    path("logout/", views.logout),

    # media 配置
    re_path(r"media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),

    # 个人站点url
    # ?P<value1>为组名，可根据组名定位匹配值的位置， 注意：是在.group()中的标记
    #  ?P<value>的意思就是命名一个名字为value的组，匹配规则符合后面的/w+
    # re_path(r'^test/$',views.test),
    # re_path(r'^(?P<username>\w+)/$', views.home_site),
    # 个人站点基于 当前用户的 的站点
    re_path(r'^(?P<username>\w+)/(?P<condition>tag|category|archive>)/(?P<param>.*)/$', views.home_site),
    # 文章详情页面的实现 ，登陆用户
    re_path(r'^(?P<username>\w+)/articles/(?P<article_id>\d+)/$', views.user_article_detail),
    # 未登录用户
    re_path(r'^articles/(?P<article_id>\d+)/$', views.article_detail),

    # 点赞视图url
    path(r'digg/', views.digg),
    # 评论url
    path(r'comment/', views.comment),
    # 评论树url
    path("get_comment_tree/", views.get_coment_tree),

    # 后台管理界面
    # 注册时，上传图片走的路由
    path('upload/', views.upload),
    # 后台管理界面
    re_path(r'cn_backend/$', views.cn_backend),

    # 增
    re_path(r"cn_backend/add_article/$", views.add_article),
    # ajax删除
    path(r"delete_article/", views.delete_article),
    # 编辑
    re_path(r"edit_article/(\d+)/", views.edit_article),
    re_path(r"test/", views.test),

    # 显示当前全网有多少条博客
    path('blog/dashboard/', views.dashboard, name='dashboard')

]
