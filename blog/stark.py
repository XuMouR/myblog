# 将stark组件引入  ，与stark组件联系起来
print("引入stark组件")
from stark.service.site import site,ModelStark
from .models import *
from django.urls import path,re_path
from django.shortcuts import render,redirect,HttpResponse


class UserinfoConfig(ModelStark):
    def display_class_list(self, obj=None, is_header=False):
        if is_header:
            return "用户名称"
        else:
            userinfo = ["{}{}{".format(obj.nid,obj.telephone) for obj in obj.objects.all()]

            return "<br>".join(userinfo)



site.register(UserInfo,UserinfoConfig)
site.register(Blog)
site.register(Category)
site.register(Tag)
site.register(Article)
site.register(Article2Tag)
site.register(ArticleUpDown)
site.register(Comment)