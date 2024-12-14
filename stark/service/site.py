from django.conf.urls import url
from django.shortcuts import HttpResponse, render


class ModelStark(object):
    list_display = []

    def __init__(self, mode, site):
        self.mode = mode
        self.site = site

    def add(self, request):
        return HttpResponse("add")

    def delete(self, request):
        return HttpResponse("delete")

    def change(self, request):
        return HttpResponse("change")

    def list_view(self, request):
        return HttpResponse("list_view")

    def get_urls_2(self):
        temp = []
        temp.append(url(r"^add/", self.add))
        temp.append(url(r"^(\d+)/delete/", self.delete))
        temp.append(url(r"^(\d+)/change/", self.change))
        temp.append(url(r"^$", self.list_view))
        return temp

    def urls_2(self, request):
        return self.get_urls_2(), None, None


class StarkSite(object):
    def __init__(self):
        self._registry = {}

    def register(self, model, stark_class=None, **options):
        print(model,stark_class)
        if not stark_class:
            # 如果注册时没自定义配置，执行
            stark_class = ModelStark
        self._registry[model] = stark_class(model, self)

    def get_urls(self):
        temp = []
        # model 模型表名称
        # stark_class_obj 模型类对应的配置类对象
        for model, stark_class_obj in self._registry.items():
            model_name = model._meta.model_name
            app_label = model._meta.app_label
            temp.append(url(r"^%s/%s/" % (app_label, model_name), stark_class_obj.urls_2))

        return temp

    @property
    def urls(self):
        return self.get_urls(), None, None


site = StarkSite()
